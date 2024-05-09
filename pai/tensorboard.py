#  Copyright 2023 Alibaba, Inc. or its affiliates.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import posixpath
import time
from typing import Optional

import requests

from .common.oss_utils import is_oss_uri
from .exception import UnexpectedStatusException
from .session import Session, get_default_session


class TensorBoardStatus(object):
    Pending = "Pending"
    Creating = "Creating"
    Running = "Running"
    Creating_Failed = "Creating_Failed"
    Deleting = "Deleting"
    Deleted = "Deleted"
    Stopping = "Stopping"
    Stopped = "Stopped"

    @classmethod
    def is_terminated(cls, status):
        return status in [
            cls.Creating_Failed,
            cls.Stopped,
            cls.Deleted,
        ]

    @classmethod
    def is_running(cls, status):
        return status in [
            cls.Running,
        ]


class TensorBoard(object):
    def __init__(self, tensorboard_id: str, session: Optional[Session] = None):
        self.session = session or get_default_session()
        self.tensorboard_id = tensorboard_id
        self._api_object = self.session.tensorboard_api.get(tensorboard_id)

    def __repr__(self):
        return "TensorBoard(tensorboard_id={}, name={}, status={})".format(
            self.tensorboard_id,
            self.display_name,
            self._status(),
        )

    @property
    def status(self):
        self._refresh()
        return self._status()

    def _status(self):
        return self._api_object.get("Status")

    @property
    def app_uri(self):
        """Get the TensorBoard application URI."""
        return self._api_object.get("TensorboardUrl")

    @property
    def summary_uri(self):
        return self._api_object.get("SummaryUri")

    @property
    def display_name(self):
        return self._api_object.get("DisplayName")

    def _refresh(self):
        self._api_object = self.session.tensorboard_api.get(self.tensorboard_id)

    @classmethod
    def create(
        cls,
        uri: str,
        wait: bool = True,
        display_name: Optional[str] = None,
        max_runtime_in_minutes: Optional[int] = None,
        source_id: Optional[str] = None,
        source_type: Optional[str] = None,
        session: Optional[Session] = None,
    ) -> "TensorBoard":
        """Launch a TensorBoard Application.

        Args:
            uri (str): A OSS URI to the directory containing the TensorBoard logs.
            wait (bool): Whether to wait for the TensorBoard application to be ready.
            display_name (str, optional): Display name of the TensorBoard application.
                Defaults to None.
            max_runtime_in_minutes: Maximum running time in minutes.
            source_type (str, optional): The type of the source object. Defaults to None.
            source_id (str, optional): The ID of the source object. Defaults to None.
            session: A Session object to use in interacting with PAI.
        Returns:
            TensorBoard: A TensorBoard object.

        Examples:
            Create a TensorBoard application from a OSS URI:
            >>> from pai.tensorboard import TensorBoard
            >>> tb = TensorBoard.create("oss://my-bucket/path/to/logs_dir/")
            >>> # Get TensorBoard Application URL.
            >>> print(tb.app_uri)
        """
        session = session or get_default_session()

        if not is_oss_uri(uri):
            raise RuntimeError("Currently only support OSS uri to create TensorBoard.")
        oss_uri = session.patch_oss_endpoint(uri)
        data_source_type = "OSS"

        if not display_name:
            # Use the last part of the OSS URI as the display name.
            display_name = posixpath.basename(uri.rstrip("/"))
            if not display_name:
                raise RuntimeError("Failed to infer display name from OSS URI.")

        tb_id = session.tensorboard_api.create(
            uri=oss_uri,
            display_name=display_name,
            data_source_type=data_source_type,
            max_running_time_minutes=max_runtime_in_minutes,
            # hack: summary_relative_path is required for CreateTensorBoard API.
            summary_relative_path="/",
            source_id=source_id,
            source_type=source_type,
        )
        tensorboard = TensorBoard(tensorboard_id=tb_id, session=session)
        if wait:
            tensorboard.wait()
        return tensorboard

    def wait(self):
        """Wait for the TensorBoard application to be ready.

        Raises:
            UnExpectedStatusException: If the TensorBoard application is terminated
                unexpectedly.

        """
        while True:
            status = self.status
            if TensorBoardStatus.is_terminated(status):
                raise UnexpectedStatusException(
                    "TensorBoard terminated unexpectedly in status: %s" % status,
                    status,
                )
            elif TensorBoardStatus.is_running(status):
                self._wait_app_available()
                return
            else:
                time.sleep(5)
                self._refresh()

    def start(self, wait: bool = True):
        """Start the TensorBoard application."""
        self._refresh()
        if TensorBoardStatus.is_running(self.status):
            return

        self.session.tensorboard_api.start(self.tensorboard_id)
        if wait:
            self.wait()

    def stop(self):
        """Stop the TensorBoard application."""
        self._refresh()
        if not TensorBoardStatus.is_running(self.status):
            return

        self.session.tensorboard_api.stop(self.tensorboard_id)

    def _wait_app_available(self):
        """Wait until the TensorBoard application is available."""
        if not self.app_uri:
            raise RuntimeError("TensorBoard application URL is not available.")

        while True:
            resp = requests.get(self.app_uri)
            # Status code not equals 5xx means the TensorBoard application is available.
            if resp.status_code // 100 != 5:
                break
            time.sleep(5)

    def delete(self):
        """Delete the TensorBoard Application."""
        self.session.tensorboard_api.delete(self.tensorboard_id)

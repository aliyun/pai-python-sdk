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

from __future__ import absolute_import

import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Callable, Optional

from ..api.base import PaginatedResult
from ..common.logging import get_logger
from ..exception import PAIException
from ..session import Session, get_default_session
from .artifact import ArchivedArtifact

logger = get_logger(__name__)


# TODO: review the status names of the PipelineRun.
class PipelineRunStatus(object):
    Initialized = "Initialized"
    ReadyToSchedule = "ReadyToSchedule"
    Starting = "Starting"
    Running = "Running"
    WorkflowServiceStarting = "WorkflowServiceStarting"
    Suspended = "Suspended"
    Succeeded = "Succeeded"
    Terminated = "Terminated"
    Unknown = "Unknown"
    Skipped = "Skipped"
    Failed = "Failed"

    @classmethod
    def completed_status(cls):
        return [
            cls.Suspended,
            cls.Terminated,
            cls.Skipped,
            cls.Failed,
        ]

    @classmethod
    def is_running(cls, status):
        if status in (
            cls.Starting,
            cls.Running,
            cls.WorkflowServiceStarting,
            cls.ReadyToSchedule,
        ):
            return True
        return False


class PipelineRun(object):
    """Class represent a pipeline run resource."""

    def __init__(
        self,
        run_id,
        name=None,
        workspace_id=None,
        status=None,
        node_id=None,
        duration=None,
        started_at=None,
        finished_at=None,
        source=None,
        user_id=None,
        parent_user_id=None,
        session=None,
    ):
        self.run_id = run_id
        self.name = name
        self.workspace_id = workspace_id
        self.status = status
        self.node_id = node_id
        self.duration = duration
        self.started_at = started_at
        self.finished_at = finished_at
        self.source = source
        self.user_id = user_id
        self.parent_user_id = parent_user_id
        self.session = session or get_default_session()

    @classmethod
    def get(cls, run_id, session=None) -> "PipelineRun":
        session = session or get_default_session()
        return cls.deserialize(session.pipeline_run_api.get(run_id=run_id))

    @classmethod
    def run(
        cls,
        name,
        arguments,
        env=None,
        pipeline_id: Optional[str] = None,
        manifest: Optional[str] = None,
        no_confirm_required: bool = True,
        session: Optional[Session] = None,
    ):
        """Submit a pipeline run with pipeline operator and run arguments.

        If pipeline_id is supplied, remote pipeline manifest is used as workflow template.


        Args:
            name (str): PipelineRun instance name of the submitted job.
            arguments (dict): Run arguments required by pipeline manifest.
            env (list): Environment arguments of run.
            pipeline_id (str): Pipeline
            manifest (str or dict): Pipeline manifest of the run workflow.
            no_confirm_required (bool): Run workflow start immediately if true
                else start_run service call if required to start the workflow.
            session (:class:`pai.session.Session`): A PAI session instance used for
                communicating with PAI service.

        Returns:
            str:run id if run workflow init success.

        """
        session = session or get_default_session()
        run_id = session.pipeline_run_api.create(
            name=name,
            arguments=arguments,
            env=env,
            manifest=manifest,
            pipeline_id=pipeline_id,
            no_confirm_required=no_confirm_required,
        )

        run = PipelineRun.get(run_id)
        logger.info(
            "Create pipeline run succeeded (run_id: {run_id}), please visit the link"
            " below to view the run details.".format(run_id=run_id)
        )
        logger.info(run.console_uri)
        return run_id

    @classmethod
    def list(
        cls,
        name=None,
        run_id=None,
        pipeline_id=None,
        status=None,
        sort_by=None,
        order=None,
        page_size=20,
        page_number=1,
        session=None,
        **kwargs,
    ):
        session = session or get_default_session()
        result = session.pipeline_run_api.list(
            name=name,
            run_id=run_id,
            pipeline_id=pipeline_id,
            status=status,
            sort_by=sort_by,
            order=order,
            workspace_id=None,
            page_size=page_size,
            page_number=page_number,
            **kwargs,
        )

        return [cls.deserialize(run) for run in result.items]

    @classmethod
    def deserialize(cls, d):
        return cls(
            run_id=d["RunId"],
            node_id=d["NodeId"],
            name=d["Name"],
            workspace_id=d["WorkspaceId"],
            user_id=d.get("UserId"),
            parent_user_id=d.get("ParentUserId"),
            source=d.get("Source"),
            started_at=d.get("StartedAt"),
            status=d.get("Status"),
        )

    def __repr__(self):
        return "PipelineRun:%s" % self.run_id

    def travel_node_status_info(self, node_id, max_depth=10):
        node_status_info = dict()

        def pipelines_travel(curr_node_id, parent=None, cur_depth=1):
            if cur_depth > max_depth:
                return
            run_node_detail_info = self.session.pipeline_run_api.get_node(
                self.run_id,
                curr_node_id,
                depth=2,
            )

            if (
                not run_node_detail_info
                or "StartedAt" not in run_node_detail_info["StatusInfo"]
            ):
                return

            if parent is None:
                curr_root_name = self.name
            else:
                curr_root_name = "{0}.{1}".format(
                    run_node_detail_info["Metadata"]["Name"], parent
                )
            node_status_info[curr_root_name] = self._pipeline_node_info(
                run_node_detail_info
            )

            pipelines = run_node_detail_info["Spec"].get("Pipelines", [])
            if not pipelines:
                return
            for sub_pipeline in pipelines:
                node_name = "{0}.{1}".format(
                    curr_root_name, sub_pipeline["Metadata"]["Name"]
                )
                node_status_info[node_name] = self._pipeline_node_info(sub_pipeline)
                next_node_id = sub_pipeline["Metadata"]["NodeId"]
                if sub_pipeline["Metadata"]["NodeType"] == "Dag" and next_node_id:
                    pipelines_travel(next_node_id, curr_root_name, cur_depth + 1)

        pipelines_travel(curr_node_id=node_id)
        return node_status_info

    @staticmethod
    def _pipeline_node_info(pipeline_info):
        return {
            "name": pipeline_info["Metadata"]["Name"],
            "nodeId": pipeline_info["Metadata"]["NodeId"],
            "status": pipeline_info["StatusInfo"]["Status"],
            "startedAt": pipeline_info["StatusInfo"]["StartedAt"],
            "finishedAt": pipeline_info["StatusInfo"].get("FinishedAt", None),
        }

    @property
    def console_uri(self):
        if not self.session.is_inner:
            return "{console_host}?regionId={region_id}#/studio/task/detail/{run_id}".format(
                console_host=self.session.console_uri,
                region_id=self.session.region_id,
                run_id=self.run_id,
            )
        return "{console_host}/#/studio/task/detail/{run_id}".format(
            console_host=self.session.console_uri, run_id=self.run_id
        )

    def get_run_info(self):
        return self.session.pipeline_run_api.get(self.run_id)

    def get_run_node_detail(self, node_id, depth=2):
        return self.session.pipeline_run_api.get_node(
            self.run_id, node_id=node_id, depth=depth
        )

    def get_outputs(self, name=None, node_id=None, depth=1, type=None):
        if not node_id:
            run_info = self.get_run_info()
            node_id = run_info["NodeId"]

        if not node_id:
            return

        result = self.session.pipeline_run_api.list_node_outputs(
            name=name,
            node_id=node_id,
            run_id=self.run_id,
            depth=depth,
            type=type,
        )
        return [ArchivedArtifact.deserialize(output) for output in result.items]

    def get_status(self):
        return self.get_run_info()["Status"]

    def start(self):
        self.session.pipeline_run_api.start(self.run_id)

    def terminate(self):
        self.session.pipeline_run_api.terminate(self.run_id)

    def _wait_for_init(self, retry_interval=1):
        """Wait for "NodeId" allocated to pipeline run."""
        datetime.now()
        run_info = self.get_run_info()
        while (
            PipelineRunStatus.is_running(run_info["Status"]) and not run_info["NodeId"]
        ):
            time.sleep(retry_interval)
            run_info = self.get_run_info()

        if run_info.get("NodeId", None):
            return run_info["NodeId"]
        else:
            raise ValueError("Failed in acquire root node_id of pipeline run.")

    def wait_for_completion(self, show_outputs=True):
        """Wait until the pipeline run stop."""
        run_info = self.get_run_info()
        node_id = run_info["NodeId"]
        if not node_id:
            raise ValueError("Expect NodeId in GetRun response")

        run_status = run_info["Status"]
        if run_status == PipelineRunStatus.Initialized:
            raise ValueError(
                'Pipeline run instance is in status "Init", please start the run instance.'
            )
        elif run_status in (PipelineRunStatus.Terminated, PipelineRunStatus.Suspended):
            raise ValueError(
                "Pipeline run instance is stopped(status:%s), please resume/retry the run."
                % run_status
            )
        elif run_status == PipelineRunStatus.Failed:
            raise ValueError("Pipeline run is failed.")
        elif run_status in (PipelineRunStatus.Skipped, PipelineRunStatus.Unknown):
            raise ValueError(
                "Pipeline run in unexpected status(%s:%s)" % (self.run_id, run_status)
            )
        elif run_status == PipelineRunStatus.Succeeded:
            return

        # Wait for Workflow init.
        print("Wait for run workflow init")

        if show_outputs:
            run_logger = _RunLogger(
                run_instance=self, node_id=node_id, session=self.session
            )
        else:
            run_logger = _MockRunLogger(run_instance=self, node_id=node_id)

        try:
            prev_status_infos = {}
            root_node_status = run_status
            log_runners = []
            while PipelineRunStatus.is_running(root_node_status):
                curr_status_infos = self.travel_node_status_info(node_id)
                for node_fullname, status_info in curr_status_infos.items():
                    if (
                        node_fullname not in prev_status_infos
                        and status_info["status"] != PipelineRunStatus.Skipped
                    ):
                        log_runner = run_logger.submit(
                            node_id=status_info["nodeId"], node_name=node_fullname
                        )
                        if log_runner:
                            log_runners.append(log_runner)
                prev_status_infos = curr_status_infos
                root_node_status = (
                    curr_status_infos[self.name]["status"]
                    if self.name in curr_status_infos
                    else root_node_status
                )

                if root_node_status == PipelineRunStatus.Failed:
                    raise PAIException(
                        "PipelineRun failed: run_id={}, run_status_info={}".format(
                            self.run_id, curr_status_infos
                        )
                    )
                failed_nodes = {
                    name: status_info
                    for name, status_info in curr_status_infos.items()
                    if PipelineRunStatus.Failed == status_info["status"]
                }
                if failed_nodes:
                    raise PAIException(
                        "PipelineRun failed: run_id={}, failed_nodes={}".format(
                            self.run_id, failed_nodes
                        )
                    )

                time.sleep(2)
        except (KeyboardInterrupt, PAIException) as e:
            run_logger.stop_tail()
            raise e

        for log_runner in log_runners:
            _ = log_runner.result()

        return self

    def _wait_with_progress(self):
        pass

    def _wait_with_logger(self, node_id):
        pass


def make_log_iterator(method: Callable, **kwargs):
    """Make an iterator from resource list API.

    Args:
        method: Resource List API.
        **kwargs: arguments for the method.

    Returns:
        A resource iterator.
    """

    page_offset = kwargs.get("page_offset", 0)
    page_size = kwargs.get("page_size", 20)

    while True:
        kwargs.update(page_offset=page_offset, page_size=page_size)
        result: PaginatedResult = method(**kwargs)

        for item in result.items:
            yield item

        if len(result.items) == 0 or len(result.items) <= page_size:
            return
        page_offset += page_size


class _RunLogger(object):
    executor = ThreadPoolExecutor(5)

    def __init__(self, run_instance, node_id, session):
        super(_RunLogger, self).__init__()
        self.run_instance = run_instance
        self.node_id = node_id
        self.running_nodes = set()
        self.session = session
        self._tail = True

    def tail(
        self,
        node_id,
        node_name,
        page_size=100,
        page_offset=0,
    ):
        if node_id in self.running_nodes:
            return
        self.running_nodes.add(node_id)

        while True and self._tail:
            logs = make_log_iterator(
                self.session.pipeline_run_api.list_node_logs,
                run_id=self.run_instance.run_id,
                node_id=node_id,
                page_size=page_size,
                page_offset=page_offset,
            )

            count = 0
            for log in logs:
                print("%s: %s" % (node_name, log))
                page_offset += 1
                count += 1
                if count % page_size == 0:
                    time.sleep(0.5)

            if count == 0:
                status = self.run_instance.get_status()
                if PipelineRunStatus.is_running(status):
                    time.sleep(2)
                else:
                    break

    def submit(
        self,
        node_id,
        node_name,
        page_size=100,
        page_offset=0,
    ):
        print("Add Node Logger: {}, {}".format(node_name, node_id))
        if node_id in self.running_nodes:
            return
        return self.executor.submit(
            self.tail,
            node_id=node_id,
            node_name=node_name,
            page_size=page_size,
            page_offset=page_offset,
        )

    def stop_tail(self):
        self._tail = False


class _MockRunLogger(object):
    def __init__(self, run_instance, node_id):
        super(_MockRunLogger, self).__init__()
        self.run_instance = run_instance
        self.node_id = node_id

    def tail(self, **kwargs):
        pass

    def submit(self, *args, **kwargs):
        pass

    def stop_tail(self):
        pass

import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional

from Tea.exceptions import TeaException

from pai.api.base import PaginatedResult
from pai.api.entity_base import EntityBaseMixin
from pai.common import ProviderAlibabaPAI
from pai.common.utils import retry
from pai.exception import UnexpectedStatusException
from pai.schema.training_job_schema import TrainingJobSchema
from pai.session import Session, get_default_session


class _TrainingJob(EntityBaseMixin):
    _schema_cls = TrainingJobSchema

    def __init__(
        self,
        algorithm_name=None,
        algorithm_version="1.0.0",
        algorithm_provider=ProviderAlibabaPAI,
        hyperparameters: Dict[str, Any] = None,
        training_job_name: str = None,
        instance_type: str = None,
        instance_count: int = None,
        output_channels: List[Dict[str, str]] = None,
        input_channels: List[Dict[str, str]] = None,
        labels: Dict[str, str] = None,
        max_running_time_in_seconds: int = None,
        experiment_config: Dict[str, str] = None,
        description: str = None,
        session: Session = None,
        **kwargs,
    ):
        super(_TrainingJob, self).__init__(session=session, **kwargs)
        session = session or get_default_session()
        self.algorithm_name = algorithm_name
        self.algorithm_version = algorithm_version
        self.algorithm_provider = algorithm_provider
        self.training_job_name = training_job_name
        self.description = description
        self.labels = labels
        self.hyperparameters = hyperparameters
        self.input_channels = input_channels
        self.output_channels = output_channels
        self.instance_type = instance_type
        self.instance_count = instance_count
        self.max_running_time_in_seconds = max_running_time_in_seconds
        self.experiment_config = experiment_config

        # Load only fields
        self.create_time = kwargs.pop("create_time", None)
        self.modified_time = kwargs.pop("modified_time", None)
        self.reason_code = kwargs.pop("reason_code", None)
        self.reason_message = kwargs.pop("reason_message", None)
        self.status = kwargs.pop("status", None)
        self.status_transitions = kwargs.pop("status_transitions", None)
        self.training_job_id = kwargs.pop("training_job_id", None)
        self.training_job_url = kwargs.pop("training_job_url", None)

    def __repr__(self):
        return "TrainingJob(id={})".format(self.training_job_id)

    def __str__(self):
        return self.__repr__()

    @classmethod
    def from_api_object(cls, obj_dict: Dict[str, Any], session: Session = None):
        pass

    @property
    def id(self):
        return self.training_job_id

    @classmethod
    def get(cls, training_job_id, session: Session = None) -> "_TrainingJob":
        session = session or get_default_session()
        res = session.training_job_api.get(training_job_id=training_job_id)
        return cls.from_api_object(res, session=session)

    @classmethod
    def list(
        cls,
        status=None,
        session: Session = None,
        page_size=50,
        page_number=1,
    ):
        session = session or get_default_session()
        res = session.training_job_api.list(
            status=status, page_size=page_size, page_number=page_number
        )
        return [cls.from_api_object(item, session=session) for item in res.items]

    def output_path(self, channel_name="model"):
        for output_channel in self.output_channels:
            if output_channel["Name"] == channel_name:
                return output_channel["OutputUri"]
        raise RuntimeError(
            f"Output channel is not specified: channel_name={channel_name}"
        )

    @property
    def console_uri(self):
        if not self.training_job_id:
            raise ValueError("The TrainingJob is not submitted")

        return self.training_job_url

    def wait(self, interval=2, show_logs: bool = True):
        self.session.training_job_api.refresh_entity(self.training_job_id, self)

        if show_logs:
            job_log_printer = _TrainingJobLogPrinter(
                training_job_id=self.training_job_id, page_size=20, session=self.session
            )
            job_log_printer.start()
        else:
            job_log_printer = None
        try:
            while not self.is_completed():
                time.sleep(interval)
        finally:
            if job_log_printer:
                job_log_printer.stop(wait=True)

        self._on_job_completed()

    def _on_job_completed(self):
        # Print an empty line to separate the training job logs and the following logs
        print()
        if self.status == TrainingJobStatus.Succeed:
            print(
                f"Training job ({self.training_job_id}) succeeded, you can check the"
                f" logs/metrics/output in  the console:\n{self.console_uri}"
            )
        elif self.status == TrainingJobStatus.Terminated:
            print(
                f"Training job is ended with status {self.status}: "
                f"reason_code={self.reason_code}, reason_message={self.reason_message}."
                f"Check the training job in the console:\n{self.console_uri}"
            )
        elif self.status in TrainingJobStatus.failed_status():
            print(
                f"Training job ({self.training_job_id}) failed, please check the logs"
                f" in the console: \n{self.console_uri}"
            )

            message = f"TrainingJob failed: name={self.training_job_name}, "
            f"training_job_id={self.training_job_id}, "
            f"reason_code={self.reason_code}, status={self.status}, "
            f"reason_message={self.reason_message}"

            raise UnexpectedStatusException(message=message, status=self.status)

    def _reload(self):
        """Reload the training job from the PAI Service,"""
        self.session.training_job_api.refresh_entity(self.training_job_id, self)

    def is_succeeded(self):
        """Return True if the training job is succeeded"""
        self._reload()
        return self.status == TrainingJobStatus.Succeed

    @retry(wait_secs=10)
    def is_completed(self):
        """Return True if the training job is completed, including failed status"""
        if self.status in TrainingJobStatus.completed_status():
            return True
        self._reload()

        return self.status in TrainingJobStatus.completed_status()


class _TrainingJobLogPrinter(object):
    """A class used to print logs for a training job"""

    executor = ThreadPoolExecutor(5)

    def __init__(
        self, training_job_id: str, page_size=10, session: Optional[Session] = None
    ):
        self.training_job_id = training_job_id
        self.session = session
        self.page_size = page_size
        self._future = None
        self._stop = False

    def _list_logs_api(self, page_number: int = 1):
        try:
            res = self.session.training_job_api.list_logs(
                self.training_job_id,
                page_number=page_number,
                page_size=self.page_size,
            )
            return res
        except TeaException as e:
            # hack: Backend service may raise an exception when the training job
            # instance is not found.
            if e.code == "TRAINING_JOB_INSTANCE_NOT_FOUND":
                return PaginatedResult(items=[], total_count=0)
            else:
                raise e

    def _list_logs(self):
        page_number, page_offset = 1, 0
        # print training job logs.
        while not self._stop:
            res = self._list_logs_api(page_number=page_number)
            # 1. move to next page
            if len(res.items) == self.page_size:
                # print new logs starting from page_offset
                self._print_logs(logs=res.items[page_offset:])
                page_number += 1
                page_offset = 0
            # 2. stay at the current page.
            else:
                if len(res.items) > page_offset:
                    # print new logs starting from page_offset
                    self._print_logs(logs=res.items[page_offset:])
                    page_offset = len(res.items)
                time.sleep(1)

        # When _stop is True, wait and print remaining logs.
        time.sleep(10)
        while True:
            res = self._list_logs_api(page_number=page_number)
            # There maybe more logs in the next page
            if len(res.items) == self.page_size:
                self._print_logs(logs=res.items[page_offset:])
                page_number += 1
                page_offset = 0
            # No more logs in the next page.
            else:
                if len(res.items) > page_offset:
                    self._print_logs(logs=res.items[page_offset:])
                break

    def _print_logs(self, logs: List[str]):
        for log in logs:
            print(log)

    def start(self):
        if self._future:
            raise ValueError("The training job log printer is already started")
        self._stop = False
        self._future = self.executor.submit(self._list_logs)

    def stop(self, wait: bool = True):
        self._stop = True
        if self._future:
            self._future.result()


class TrainingJobStatus(object):
    CreateFailed = "CreateFailed"
    InitializeFailed = "InitializeFailed"
    Succeed = "Succeed"
    Failed = "Failed"
    Terminated = "Terminated"
    Creating = "Creating"
    Created = "Created"
    Initializing = "Initializing"
    Submitted = "Submitted"
    Running = "Running"

    @classmethod
    def completed_status(cls):
        return [
            cls.InitializeFailed,
            cls.Succeed,
            cls.Failed,
            cls.Terminated,
        ]

    @classmethod
    def failed_status(cls):
        return [
            cls.InitializeFailed,
            cls.Failed,
            cls.CreateFailed,
        ]

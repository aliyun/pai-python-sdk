from __future__ import absolute_import

from abc import ABCMeta
from enum import Enum

from six import with_metaclass

from ..pipeline.run import PipelineRunStatus


class JobStatus(Enum):
    Init = "Init"
    Running = "Running"
    Suspended = "Suspended"
    Succeeded = "Succeeded"
    Terminated = "Terminated"
    Unknown = "Unknown"
    Skipped = "Skipped"
    Failed = "Failed"


class RunJob(with_metaclass(ABCMeta, object)):
    def __init__(self, run_instance):
        self.run_instance = run_instance

    @property
    def session(self):
        return self.run_instance._session

    @property
    def name(self):
        return self.run_instance.name

    @property
    def run_id(self):
        return self.run_instance.run_id

    def get_outputs(self, output_name=None):
        job_status = self.run_instance.get_status()
        if job_status != PipelineRunStatus.Succeeded:
            raise ValueError("Succeeded Run job is required, Current job status:%s" % job_status)
        run_outputs = self.run_instance.get_outputs(name=output_name)
        return run_outputs

    def terminate(self):
        self.run_instance.terminate()

    def suspend(self):
        self.run_instance.suspend()

    def resume(self):
        self.run_instance.resume()

    def wait_for_completion(self, show_outputs=True, timeout=None):
        self.run_instance.wait_for_completion(show_outputs=show_outputs, timeout=timeout)

    def get_status(self):
        return JobStatus(self.run_instance.get_status())

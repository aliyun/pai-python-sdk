from __future__ import absolute_import

from abc import ABCMeta

from enum import Enum
from six import with_metaclass

from pai.pipeline import RunStatus


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
        return self.run_instance.session

    @property
    def name(self):
        return self.run_instance.name

    @property
    def run_id(self):
        return self.run_instance.run_id

    # TODO: return self-defined class but not json
    def get_outputs(self):
        if self.run_instance.get_status() != RunStatus.Succeeded:
            raise ValueError("Succeeded Run job is required!")
        run_outputs = self.run_instance.get_outputs()
        return run_outputs

    def terminate(self):
        self.run_instance.terminate()

    def suspend(self):
        self.run_instance.suspend()

    def resume(self):
        self.run_instance.resume()

    def attach(self):
        self.run_instance.wait()

    def get_status(self):
        return JobStatus(self.run_instance.get_status())

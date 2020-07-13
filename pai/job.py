from __future__ import absolute_import

from six import with_metaclass
from abc import ABCMeta, abstractproperty

from pai.pipeline.run import RunStatus


class RunJob(with_metaclass(ABCMeta, object)):
    def __init__(self, run_instance):
        self.run_instance = run_instance

    @abstractproperty
    def session(self):
        pass

    def get_outputs(self):
        if self.run_instance.get_status() != RunStatus.Succeeded:
            raise ValueError("Succeeded Run job is required!")
        return self.run_instance.get_outputs()

    def terminate(self):
        self.run_instance.terminate()

    def suspend(self):
        self.run_instance.suspend()

    def resume(self):
        self.run_instance.resume()

    def attach(self):
        self.run_instance.wait()



from __future__ import absolute_import

from abc import abstractmethod


class PipelineBase(object):

    def __init__(self, inputs, outputs):
        self._inputs = inputs
        self._outputs = outputs

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self._outputs

    def translate_arguments(self, arguments):
        pass

    @abstractmethod
    def run(self, job_name, arguments, **kwargs):
        pass

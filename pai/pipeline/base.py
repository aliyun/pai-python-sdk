from __future__ import absolute_import

from abc import abstractmethod, ABCMeta

import six

from pai.core.session import get_default_session
from pai.pipeline.consts import DEFAULT_PIPELINE_API_VERSION
from pai.pipeline.types import InputsSpec, OutputsSpec


class TemplateSpecBase(six.with_metaclass(ABCMeta, object)):
    def __init__(
        self,
        inputs,
        outputs,
        identifier=None,
        version=None,
        provider=None,
    ):

        session = get_default_session()
        self._identifier = identifier
        self._version = version
        self._provider = provider or session.provider
        self._inputs = (
            inputs if isinstance(inputs, InputsSpec) else InputsSpec(inputs or [])
        )
        self._outputs = (
            outputs if isinstance(outputs, OutputsSpec) else OutputsSpec(outputs or [])
        )

    def __repr__(self):
        return "%s:{Identifier:%s, Provider:%s, Version:%s}" % (
            type(self).__name__,
            self.identifier,
            self.provider,
            self.version,
        )

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self._outputs

    @classmethod
    def current_provider(cls):
        return get_default_session().provider

    @property
    def metadata(self):
        return {
            "identifier": self.identifier,
            "provider": self.provider,
            "version": self.version,
        }

    @property
    def identifier(self):
        return self._identifier

    @property
    def provider(self):
        return self._provider

    @property
    def version(self):
        return self._version

    @property
    def _template(self):
        from .template import PipelineTemplate

        manifest = self.to_dict()
        return PipelineTemplate(manifest=manifest)

    def save(self, identifier, version):
        templ = self._template.save(identifier=identifier, version=version)
        return templ

    def run(self, job_name, arguments=None, **kwargs):
        return self._template.run(job_name=job_name, arguments=arguments, **kwargs)

    def _spec_to_dict(self):
        spec = {"inputs": self.inputs.to_dict(), "outputs": self.outputs.to_dict()}
        return spec

    @abstractmethod
    def to_dict(self):
        data = {
            "apiVersion": DEFAULT_PIPELINE_API_VERSION,
            "metadata": self.metadata,
            "spec": self._spec_to_dict(),
        }
        return data

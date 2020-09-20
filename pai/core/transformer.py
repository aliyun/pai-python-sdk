from __future__ import absolute_import

from abc import ABCMeta, abstractmethod

import logging
import six
import yaml

from .job import RunJob
from .session import get_default_session
from ..pipeline.template import PipelineTemplate

logger = logging.getLogger(__name__)


class Transformer(six.with_metaclass(ABCMeta, object)):

    def __init__(self, parameters=None):
        self._parameters = parameters
        self._jobs = []

    def transform(self, wait=True, job_name=None, show_outputs=False, args=None, **kwargs):
        run_instance = self._run(job_name=job_name, arguments=args,
                                 **kwargs)
        run_job = TransformJob(transformer=self, run_instance=run_instance)
        self._jobs.append(run_job)
        if wait:
            run_job.wait_for_completion(show_outputs=show_outputs)
        return run_job

    @abstractmethod
    def _run(self, job_name, arguments, **kwargs):
        raise NotImplementedError

    @property
    def parameters(self):
        return self._parameters

    @property
    def last_job(self):
        if self._jobs:
            return self._jobs[-1]


class PipelineTransformer(Transformer):

    def __init__(self, parameters=None, manifest=None, _compiled_args=False,
                 pipeline_id=None):
        self._session = get_default_session()
        self._compiled_args = _compiled_args
        self._template = PipelineTemplate(manifest=manifest, pipeline_id=pipeline_id)
        super(PipelineTransformer, self).__init__(parameters=parameters)

    def transform(self, wait=True, job_name=None, show_outputs=True, args=None, **kwargs):
        args = args or dict()
        if not self._compiled_args:
            run_args = self.parameters.copy()
            run_args.update(args)
        else:
            run_args = args
        return super(PipelineTransformer, self).transform(wait=wait, job_name=job_name,
                                                          args=run_args,
                                                          show_outputs=show_outputs,
                                                          **kwargs)

    def _run(self, job_name=None, arguments=None, **kwargs):
        run = self._template.run(job_name=job_name, arguments=arguments, wait=False)
        logger.info("PaiFlow CreateRun Job, RunId:%s" % run.run_id)
        return run

    @property
    def identifier(self):
        return self._template.identifier

    @property
    def provider(self):
        return self._template.provider

    @property
    def version(self):
        return self._template.version

    @property
    def pipeline_id(self):
        return self._template.pipeline_id


# TODO: extract common method/attribute from AlgoBaseEstimator, AlgoBaseTransformer
class AlgoBaseTransformer(PipelineTransformer):
    """Base class for PAI Transformer algorithm class """

    _identifier_default = None
    _provider_default = None
    _version_default = None

    def __init__(self, **kwargs):
        session = get_default_session()
        manifest, pipeline_id = self.get_base_info(session)
        super(AlgoBaseTransformer, self).__init__(parameters=kwargs,
                                                  _compiled_args=True,
                                                  manifest=manifest, pipeline_id=pipeline_id)

    def get_base_info(self, session):
        assert self._identifier_default is not None
        assert self._provider_default is not None
        assert self._version_default is not None
        pipeline_info = session.get_pipeline(identifier=self._identifier_default,
                                             provider=self._provider_default,
                                             version=self._version_default)

        return yaml.load(pipeline_info["Manifest"], yaml.FullLoader), pipeline_info["PipelineId"]

    def transform(self, *inputs, **kwargs):
        wait = kwargs.pop("wait", True)
        job_name = kwargs.pop("job_name", None)
        fit_args = self.parameters.copy()
        fit_args.update(kwargs)

        fit_args = {k: v for k, v in self._compile_args(*inputs, **fit_args).items()}
        return super(AlgoBaseTransformer, self).transform(wait=wait, job_name=job_name,
                                                          args=fit_args)


class TransformJob(RunJob):
    """Transform job manager, used to get outputs of transform result, handle job run status"""

    def __init__(self, transformer, run_instance):
        super(TransformJob, self).__init__(run_instance=run_instance)
        self.transformer = transformer

    def get_outputs(self):
        """
        Returns:

        """
        outputs = super(TransformJob, self).get_outputs()
        return {output.name: output for output in outputs}

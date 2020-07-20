from abc import ABCMeta, abstractmethod

import six
import yaml

from pai.pipeline import PaiFlowBase
from pai.job import RunJob


class Transformer(six.with_metaclass(ABCMeta, object)):

    def __init__(self, session, parameters=None):
        self.session = session
        self._parameters = parameters
        self._jobs = []

    def transform(self, wait=True, job_name=None, args=None, **kwargs):
        run_instance = self._run(job_name=job_name, arguments=args,
                                 **kwargs)
        run_job = _TransformJob(transformer=self, run_instance=run_instance)
        self._jobs.append(run_job)
        if wait:
            run_job.attach()
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


class PipelineTransformer(PaiFlowBase, Transformer):

    def __init__(self, session, parameters=None, manifest=None, _compiled_args=False,
                 pipeline_id=None):
        Transformer.__init__(self, session=session, parameters=parameters)
        PaiFlowBase.__init__(self, session=session, manifest=manifest, pipeline_id=pipeline_id)
        self._compiled_args = _compiled_args

    @classmethod
    def from_manifest(cls, manifest, session, parameters=None):
        pe = PipelineTransformer(session=session, parameters=parameters, manifest=manifest)
        return pe

    @classmethod
    def from_pipeline_id(cls, pipeline_id, session, parameters=None):
        pipeline_info = session.get_pipeline_by_id(pipeline_id)
        manifest = yaml.load(pipeline_info["Manifest"], yaml.FullLoader)
        pe = PipelineTransformer(session=session, parameters=parameters, manifest=manifest,
                                 pipeline_id=pipeline_id)
        return pe

    def transform(self, wait=True, job_name=None, args=None, **kwargs):
        args = args or dict()
        if not self._compiled_args:
            run_args = self.parameters.copy()
            run_args.update(args)
        else:
            run_args = args
        return super(PipelineTransformer, self).transform(wait=wait, job_name=job_name,
                                                          args=run_args, **kwargs)


# TODO: extract common method/attribute from AlgoBaseEstimator, AlgoBaseTransformer
class AlgoBaseTransformer(PipelineTransformer):
    """Base class for PAI Transformer algorithm class """

    _identifier_default = None
    _provider_default = None
    _version_default = None

    def __init__(self, session, **kwargs):
        manifest, pipeline_id = self.get_base_info(session)
        super(AlgoBaseTransformer, self).__init__(session=session, parameters=kwargs,
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


class _TransformJob(RunJob):

    def __init__(self, transformer, run_instance):
        super(_TransformJob, self).__init__(run_instance=run_instance)
        self.transformer = transformer

    @property
    def session(self):
        return self.transformer.session

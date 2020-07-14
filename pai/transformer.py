from abc import ABCMeta
import six
import yaml

from pai.base import PaiFlowBase
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
            run_instance.attach()
        return run_job

    @property
    def parameters(self):
        return self._parameters


class PipelineTransformer(PaiFlowBase, Transformer):

    def __init__(self, session, parameters=None, _compile_args=False, manifest=None, pipeline_id=None):
        Transformer.__init__(self, session=session, parameters=parameters)
        PaiFlowBase.__init__(self, session=session, manifest=manifest, pipeline_id=pipeline_id)
        self._compile_args = _compile_args

    def set_manifest(self, manifest):
        metadata = manifest["metadata"]
        identifier, provider, version = metadata["identifier"], metadata["provider"], metadata["version"]
        self.set_identifier(identifier).set_version(version).set_provider(provider)
        self._manifest = manifest
        return self

    def rebuild_args(self, **kwargs):
        args = self.compile_args(**kwargs)
        return {k: v for k, v in args.items() if v is not None}

    def transform(self, *inputs, **kwargs):
        wait = kwargs.pop("wait", True)
        job_name = kwargs.pop("job_name", None)

        origin_args = self.parameters.copy()
        origin_args.update(kwargs)

        if self._compile_args:
            args = {k: v for k, v in self.compile_args(*inputs, **kwargs).items() if v is not None}
        return super(PipelineTransformer, self).transform(wait=wait, job_name=job_name, args=args)

    @classmethod
    def from_manifest(cls, manifest, session, parameters=None):
        pe = PipelineTransformer(session=session, parameters=parameters).set_manifest(manifest)
        return pe


# TODO: extract common method/attribute from AlgoBaseEstimator, AlgoBaseTransformer
class AlgoBaseTransformer(PipelineTransformer):
    """Base class for PAI Transformer algorithm class """

    _identifier_default = None
    _provider_default = None
    _version_default = None

    def __init__(self, session, **kwargs):
        manifest, pipeline_id = self.get_base_info(session)
        super(AlgoBaseTransformer, self).__init__(session=session, _compile_args=True, parameters=kwargs,
                                                  manifest=manifest, pipeline_id=pipeline_id)

    def get_base_info(self, session):
        assert self._identifier_default is not None
        assert self._provider_default is not None
        assert self._version_default is not None
        pipeline_info = session.get_pipeline(identifier=self._identifier_default,
                                             provider=self._provider_default,
                                             version=self._version_default)

        return yaml.load(pipeline_info["Manifest"], yaml.FullLoader), pipeline_info["PipelineId"]

    def compile_args(self, *inputs, **kwargs):
        return dict()


class _TransformJob(RunJob):

    def __init__(self, transformer, run_instance):
        super(_TransformJob, self).__init__(run_instance=run_instance)
        self.transformer = transformer

    @property
    def session(self):
        return self.transformer.session

    def get_outputs(self):
        pass

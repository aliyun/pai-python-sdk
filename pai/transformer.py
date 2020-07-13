from abc import ABCMeta
import six

from pai.base import PaiFlowBase
from pai.job import RunJob


class Transformer(six.with_metaclass(ABCMeta, object)):

    def __init__(self, session, **kwargs):
        self.session = session
        self._parameters = kwargs
        self._jobs = []

    def transform(self, wait=True, job_name=None, args=None, **kwargs):
        run_instance = self._run(wait=wait, job_name=job_name, arguments=args,
                                 **kwargs)
        run_job = _TransformJob(transformer=self, run_instance=run_instance)
        self._jobs.append(run_job)
        if wait:
            run_instance.attach()
        return run_job

    def parameters(self):
        return self._parameters


class PipelineTransformer(PaiFlowBase, Transformer):

    def __init__(self, session, **kwargs):
        PaiFlowBase.__init__(self, session=session)
        Transformer.__init__(self, session=session, **kwargs)

    def set_manifest(self, manifest):
        metadata = manifest["metadata"]
        identifier, provider, version = metadata["identifier"], metadata["provider"], metadata["version"]
        self.set_identifier(identifier).set_version(version).set_provider(provider)
        self._manifest = manifest
        return self

    def rebuild_args(self, **kwargs):
        args = self.compile_args(**kwargs)
        return {k: v for k, v in args.items() if v is not None}

    def transform(self, wait=True, job_name=None, args=None, **kwargs):
        args = args or dict()
        origin_args = self.parameters.copy()
        args.update(origin_args)

        if self._compile_args:
            args = self.compile_args(**args)
        return super(PipelineTransformer, self).transform(wait=wait, job_name=job_name, args=args, **kwargs)

    @classmethod
    def from_manifest(cls, manifest, session, parameters=None):
        pe = PipelineTransformer(session=session, parameters=parameters).set_manifest(manifest)
        return pe


class AlgoBaseTransformer(PipelineTransformer):

    def __init__(self, session, **kwargs):
        super(AlgoBaseTransformer, self).__init__(session=session, _compile_args=True, parameters=kwargs)

    def compile_args(self):
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

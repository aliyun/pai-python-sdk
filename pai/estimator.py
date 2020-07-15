from __future__ import absolute_import

import yaml

from .base import PaiFlowBase
from .job import RunJob


class Estimator(object):

    def __init__(self, session, parameters=None):
        self.session = session
        self._parameters = parameters
        self._jobs = []

    @property
    def parameters(self):
        return self._parameters

    def fit(self, wait=True, job_name=None, args=None, **kwargs):
        run_instance = self._run(job_name=job_name, arguments=args,
                                 **kwargs)
        run_job = _EstimatorJob(estimator=self, run_instance=run_instance)
        self._jobs.append(run_job)
        if wait:
            run_instance.attach()
        return run_job


class PipelineEstimator(PaiFlowBase, Estimator):

    def __init__(self, session, parameters=None, _compile_args=False, manifest=None,
                 pipeline_id=None):
        Estimator.__init__(self, session=session, parameters=parameters)
        PaiFlowBase.__init__(self, session=session, manifest=manifest, pipeline_id=pipeline_id)
        self._compile_args = _compile_args

    def rebuild_args(self, **kwargs):
        args = self.compile_args(**kwargs)
        return {k: v for k, v in args.items() if v is not None}

    def fit(self, *inputs, **kwargs):
        wait = kwargs.pop("wait", True)
        job_name = kwargs.pop("job_name", None)
        fit_args = self.parameters.copy()
        fit_args.update(kwargs)

        if self._compile_args:
            fit_args = {k: v for k, v in self.compile_args(*inputs, **fit_args).items()}
        return super(PipelineEstimator, self).fit(wait=wait, job_name=job_name, args=fit_args)

    @classmethod
    def from_manifest(cls, manifest, session, parameters=None):
        pe = PipelineEstimator(session=session, parameters=parameters, manifest=manifest,
                               _compile_args=False)
        return pe

    @classmethod
    def from_pipeline_id(cls, pipeline_id, session, parameters=None):
        pipeline_info = session.get_pipeline_by_id(pipeline_id)
        manifest = yaml.load(pipeline_info["Manifest"], yaml.FullLoader)
        pe = PipelineEstimator(session=session, parameters=parameters, manifest=manifest,
                               pipeline_id=pipeline_id,
                               _compile_args=False)
        return pe


# TODO: extract common method/attribute from AlgoBaseEstimator, AlgoBaseTransformer
class AlgoBaseEstimator(PipelineEstimator):
    """Base class for PAI Estimator algorithm class """

    _identifier_default = None
    _provider_default = None
    _version_default = None

    def __init__(self, session, **kwargs):
        manifest, pipeline_id = self.get_base_info(session)
        super(AlgoBaseEstimator, self).__init__(session=session, _compile_args=True,
                                                parameters=kwargs,
                                                manifest=manifest, pipeline_id=pipeline_id)

    def get_base_info(self, session):
        assert self._identifier_default is not None
        assert self._provider_default is not None
        assert self._version_default is not None
        pipeline_info = session.get_pipeline(identifier=self._identifier_default,
                                             provider=self._provider_default,
                                             version=self._version_default)

        return yaml.load(pipeline_info["Manifest"], yaml.FullLoader), pipeline_info["PipelineId"]


class _EstimatorJob(RunJob):

    def __init__(self, estimator, run_instance):
        super(_EstimatorJob, self).__init__(run_instance=run_instance)
        self.estimator = estimator

    @property
    def session(self):
        return self.estimator.session

    # def create_model(self, artifact=None):
    #     outputs = self.get_outputs()
    #     if not outputs:
    #         raise ValueError("No model artifact is available to create model")
    #
    #     model_data = None
    #     if name is None:
    #         model_data = outputs[0]
    #     else:
    #         for output in outputs:
    #             if output["Name"] == name:
    #                 model_data = output
    #
    #     if not model_data or model_data["Type"] != ArtifactDataType.DataSet:
    #         raise ValueError("No model artifact is available to create model")
    #
    #     if model_data["locationType"]["modelType"] == ArtifactModelType.OfflineModel:
    #         return XFlowOfflineModel(session=self.session, name=model_data["Name"],
    #                                  model_data=model_data)
    #     else:
    #         return PmmlModel(session=self.session, name=model_data["Name"], model_data=model_data)

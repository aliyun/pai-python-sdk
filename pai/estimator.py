from __future__ import absolute_import

from abc import ABCMeta, abstractmethod

import six
import yaml

from .model import XFlowOfflineModel, PmmlModel
from .pipeline import PaiFlowBase
from .job import RunJob
from .pipeline.artifact import ArtifactModelType


class Estimator(six.with_metaclass(ABCMeta, object)):

    def __init__(self, session, parameters=None):
        self.session = session
        self._parameters = parameters
        self._jobs = []

    @property
    def parameters(self):
        return self._parameters

    @abstractmethod
    def _run(self, job_name, arguments, **kwargs):
        raise NotImplementedError

    def fit(self, wait=True, job_name=None, args=None, **kwargs):
        run_instance = self._run(job_name=job_name, arguments=args, **kwargs)
        run_job = EstimatorJob(estimator=self, run_instance=run_instance)
        self._jobs.append(run_job)
        if wait:
            run_job.attach()
        return run_job

    @property
    def last_job(self):
        if self._jobs:
            return self._jobs[-1]


class PipelineEstimator(PaiFlowBase, Estimator):

    def __init__(self, session, parameters=None, manifest=None, _compiled_args=False,
                 pipeline_id=None):
        Estimator.__init__(self, session=session, parameters=parameters)
        PaiFlowBase.__init__(self, session=session, manifest=manifest, pipeline_id=pipeline_id)
        self._compiled_args = _compiled_args

    @classmethod
    def from_manifest(cls, manifest, session, parameters=None):
        pe = PipelineEstimator(session=session, parameters=parameters, manifest=manifest)
        return pe

    @classmethod
    def from_pipeline_id(cls, pipeline_id, session, parameters=None):
        pipeline_info = session.get_pipeline_by_id(pipeline_id)
        manifest = yaml.load(pipeline_info["Manifest"], yaml.FullLoader)
        pe = PipelineEstimator(session=session, parameters=parameters, manifest=manifest,
                               pipeline_id=pipeline_id)
        return pe

    def fit(self, wait=True, job_name=None, args=None, **kwargs):
        args = args or dict()
        if not self._compiled_args:
            run_args = self.parameters.copy()
            run_args.update(args)
        else:
            run_args = args
        return super(PipelineEstimator, self).fit(wait=wait, job_name=job_name, args=run_args,
                                                  **kwargs)


# TODO: extract common method/attribute from AlgoBaseEstimator, AlgoBaseTransformer
class AlgoBaseEstimator(PipelineEstimator):
    """Base class for PAI Estimator algorithm class """

    _identifier_default = None
    _provider_default = None
    _version_default = None

    def __init__(self, session, **kwargs):
        manifest, pipeline_id = self.get_base_info(session)
        super(AlgoBaseEstimator, self).__init__(session=session, parameters=kwargs,
                                                _compiled_args=True, manifest=manifest,
                                                pipeline_id=pipeline_id)

    def get_base_info(self, session):
        assert self._identifier_default is not None
        assert self._provider_default is not None
        assert self._version_default is not None
        pipeline_info = session.get_pipeline(identifier=self._identifier_default,
                                             provider=self._provider_default,
                                             version=self._version_default)

        return yaml.load(pipeline_info["Manifest"], yaml.FullLoader), pipeline_info["PipelineId"]

    def fit(self, *inputs, **kwargs):
        wait = kwargs.pop("wait", True)
        job_name = kwargs.pop("job_name", None)

        fit_args = self.parameters.copy()
        fit_args.update(kwargs)

        fit_args = {k: v for k, v in self._compile_args(*inputs, **fit_args).items()}
        return super(AlgoBaseEstimator, self).fit(wait=wait, job_name=job_name, args=fit_args)


class EstimatorJob(RunJob):

    def __init__(self, estimator, run_instance):
        super(EstimatorJob, self).__init__(run_instance=run_instance)
        self.estimator = estimator

    @property
    def session(self):
        return self.estimator.session

    def create_model(self, output_name=None):
        """Create :class:`~pai.model.Model`

        Args:
            output_name:

        Returns:

        """
        outputs = self.get_outputs()
        if not outputs:
            raise ValueError("No model artifact is available to create model")
        artifact_infos = [output for output in outputs if output.is_model and output.value]

        if len(artifact_infos) == 0:
            raise ValueError("No model data is available to create model")

        if output_name is None:
            if len(artifact_infos) > 1:
                raise ValueError("More than one model in Estimator outputs, please specific"
                                 " the output used to create model")
            artifact_info = artifact_infos[0]
        else:
            infos = [m for m in artifact_infos if m.name == output_name]
            if not infos:
                raise ValueError("No specific model data with name :%s" % output_name)
            elif len(infos) > 1:
                raise ValueError(
                    "Unexpected EstimatorJob outputs, more than one output has name:%s ",
                    output_name)
            artifact_info = infos[0]

        model_data = artifact_info.value
        metadata = artifact_info.metadata

        if metadata.model_type == ArtifactModelType.OfflineModel:
            return XFlowOfflineModel(session=self.session, name=model_data.offline_model,
                                     model_data=model_data)
        else:
            return PmmlModel(session=self.session, name=artifact_info.name,
                             model_data=model_data)

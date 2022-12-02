from typing import Any, Dict, List, Union

from pai.base import EntityBaseMixin
from pai.common.utils import make_list_resource_iterator
from pai.decorator import cached_property, config_default_session
from pai.schema.algorithm_schema import (
    AlgorithmSchema,
    AlgorithmSpecSchema,
    AlgorithmVersionSchema,
)
from pai.session import Session


class ChannelDefinition(object):
    def __init__(
        self,
        description: str = None,
        name: str = None,
        properties: List[Dict[str, Any]] = None,
        required: bool = None,
        supported_channel_types: List[str] = None,
    ):
        self.description = description
        self.name = name
        self.properties = properties
        self.required = required
        self.supported_channel_types = supported_channel_types


class MetricDefinition(object):
    def __init__(
        self,
        description: str = None,
        name: str = None,
        regex: str = None,
    ):
        self.description = description
        self.name = name
        self.regex = regex


class HyperparameterDefinition(object):
    def __init__(
        self,
        default_value: str = None,
        description: str = None,
        name: str = None,
        required: bool = None,
        type: str = None,
    ):
        self.default_value = default_value
        self.description = description
        self.name = name
        self.required = required
        self.type = type


class AlgorithmSpec(object):
    def __init__(
        self,
        command: List[str] = None,
        # compute_resource: AlgorithmSpecComputeResource = None,
        hyperparameters: List[HyperparameterDefinition] = None,
        image: str = None,
        input_channels: List[ChannelDefinition] = None,
        output_channels: List[ChannelDefinition] = None,
        job_type: str = None,
        metric_definitions: List[MetricDefinition] = None,
        supported_instance_types: List[str] = None,
        supports_distributed_training: bool = None,
    ):
        self.supports_distributed_training = supports_distributed_training
        self.supported_instance_types = supported_instance_types
        self.metric_definitions = metric_definitions
        self.job_type = job_type
        self.output_channels = output_channels
        self.input_channels = input_channels
        self.image = image
        self.hyperparameters = hyperparameters
        self.command = command


class Algorithm(EntityBaseMixin):
    _schema_cls = AlgorithmSchema

    @config_default_session
    def __init__(
        self,
        session,
        algorithm_id,
        algorithm_name,
        algorithm_provider=None,
        workspace_id=None,
        **kwargs,
    ):
        super(Algorithm, self).__init__(session=session, **kwargs)
        self.algorithm_id = algorithm_id
        self.algorithm_name = algorithm_name
        self.algorithm_provider = algorithm_provider
        self.workspace_id = workspace_id

    def __repr__(self):
        return "Algorithm:name={}".format(self.algorithm_name)

    @property
    def id(self):
        return self.algorithm_id

    @classmethod
    @config_default_session
    def get(cls, algorithm_id, session: Session = None):
        result = session.algorithm_api.get(algorithm_id)
        return cls.from_api_object(result, session=session)

    @classmethod
    @config_default_session
    def list(
        cls,
        algorithm_name=None,
        algorithm_id=None,
        algorithm_provider=None,
        page_size=10,
        page_number=1,
        session: Session = None,
    ):
        result = session.algorithm_api.list(
            algorithm_name=algorithm_name,
            algorithm_id=algorithm_id,
            algorithm_provider=algorithm_provider,
            page_size=page_size,
            page_number=page_number,
        )
        return [cls.from_api_object(item) for item in result.items]

    def list_versions(self, page_size=10, page_number=1):
        result = self.session.algorithm_api.list_versions(
            algorithm_id=self.algorithm_id,
            page_size=page_size,
            page_number=page_number,
        )

        return [AlgorithmVersion.from_api_object(item) for item in result.items]

    def get_version(self, algorithm_version) -> "AlgorithmVersion":
        return AlgorithmVersion.get(
            self.algorithm_id, algorithm_version=algorithm_version
        )

    def create_version(
        self,
        algorithm_version: str,
        algorithm_spec: Union[AlgorithmSpec, Dict[str, Any]],
    ):
        if isinstance(algorithm_spec, AlgorithmSpec):
            algorithm_spec = AlgorithmSpecSchema().dump(algorithm_spec)
        self.session.algorithm_api.create_version(
            algorithm_id=self.algorithm_id,
            version=algorithm_version,
            algorithm_spec=algorithm_spec,
        )

        return self.get_version(algorithm_version=algorithm_version)

    @classmethod
    @config_default_session
    def get_by_name(
        cls, algorithm_name, algorithm_provider, session: Session = None
    ) -> "Algorithm":
        iterator = make_list_resource_iterator(
            cls.list,
            algorithm_name=algorithm_name,
            algorithm_provider=algorithm_provider,
            session=session,
        )
        return next(
            (item for item in iterator if item.algorithm_name == algorithm_name), None
        )


class AlgorithmVersion(EntityBaseMixin):
    _schema_cls = AlgorithmVersionSchema

    @config_default_session
    def __init__(
        self,
        algorithm_version=None,
        algorithm_spec=None,
        session: Session = None,
        algorithm_id=None,
        **kwargs,
    ):
        super(AlgorithmVersion, self).__init__(session=session, **kwargs)
        self.algorithm_spec = algorithm_spec
        self.algorithm_id = algorithm_id
        self.algorithm_version = algorithm_version

    def __repr__(self):
        return "AlgorithmVersion:id={} version={}".format(
            self.algorithm_id, self.algorithm_version
        )

    @cached_property
    def algorithm(self):
        return Algorithm.get(self.algorithm_id)

    @classmethod
    @config_default_session
    def get(cls, algorithm_id, algorithm_version, session=None) -> "AlgorithmVersion":
        res = session.algorithm_api.get_version(
            algorithm_id,
            algorithm_version=algorithm_version,
        )
        return cls.from_api_object(res, session=session)

    def run(
        self,
        instance_count,
        instance_type,
        input_config,
        output_config,
        job_name=None,
        hyperparameters=None,
        labels=None,
        wait=False,
        **kwargs,
    ):
        from pai.job import TrainingJob

        job = TrainingJob(
            algorithm_name=self.algorithm.algorithm_name,
            algorithm_version=self.algorithm_version,
            algorithm_provider=self.algorithm.algorithm_provider,
            hyperparameters=hyperparameters,
            job_name=job_name,
            instance_type=instance_type,
            instance_count=instance_count,
            output_channels=output_config,
            input_channels=input_config,
            labels=labels,
            session=self.session,
            **kwargs,
        )

        job.run(
            wait=wait,
        )
        return job

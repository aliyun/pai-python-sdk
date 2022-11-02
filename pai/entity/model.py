from typing import List

from pai.common.consts import ModelFormat, PagingOrder, ResourceAccessibility
from pai.common.oss_utils import parse_oss_url
from pai.core import Session
from pai.decorator import config_default_session
from pai.entity.base import EntityBaseMixin, make_resource_iterator
from pai.entity.service import BuildInProcessor, Service, ServiceConfig
from pai.schema.model_schema import ModelSchema, ModelVersionSchema


class Model(EntityBaseMixin):

    FieldCreateTime = "gmt_create_time"

    _schema_cls = ModelSchema

    @config_default_session
    def __init__(self, name, accessibility, session=None, **kwargs):
        super(Model, self).__init__(session=session)

        self.name = name
        self.accessibility = accessibility

        # Read only fields from API response.
        self._model_id = kwargs.pop("model_id", None)
        self._create_time = kwargs.pop("create_time", None)

    @classmethod
    @config_default_session
    def get(cls, id, session=None) -> "Model":
        return cls.from_api_object(session.model_api.get(id), session=session)

    def delete(self):
        return self.session.model_api.delete(self.id)

    @classmethod
    @config_default_session
    def get_by_name(cls, name, session: Session = None):
        iter = make_resource_iterator(cls.list, name=name, session=session)
        return next((m for m in iter if m.name == name), None)

    @classmethod
    @config_default_session
    def list(
        cls,
        name=None,
        order=None,
        page_number=None,
        page_size=None,
        sort_by=None,
        session: Session = None,
    ) -> List["Model"]:
        res = session.model_api.list(
            name=name,
            order=order,
            page_number=page_number,
            page_size=page_size,
            sort_by=sort_by,
        )

        return [cls.from_api_object(item, session=session) for item in res.items]

    @property
    def id(self):
        return self._model_id

    @property
    def create_time(self):
        return self._create_time

    def latest_version(self) -> "ModelVersion":
        models = self.list_versions(
            sort_by=self.FieldCreateTime,
            order=PagingOrder.DESCENT,
        )

        return models[0] if models else None

    def list_versions(
        self, order=None, sort_by=None, page_size=None, page_number=None
    ) -> List["ModelVersion"]:
        res = self.session.model_api.list_versions(
            model_id=self.id,
            page_size=page_size,
            page_number=page_number,
            order=order,
            sort_by=sort_by,
        )

        return [
            ModelVersion.from_api_object(item, session=self.session)
            for item in res.items
        ]


class ModelVersion(EntityBaseMixin):

    _schema_cls = ModelVersionSchema

    def __init__(
        self,
        uri,
        model_format=None,
        framework=None,
        name=None,
        model_id=None,
        inference_spec=None,
        accessibility=ResourceAccessibility.PUBLIC,
        version="v1.0.0",
        workspace_id=None,
        session=None,
        description=None,
        labels=None,
        **kwargs,
    ):
        super(ModelVersion, self).__init__(session=session)
        self.name = name
        self.uri = uri
        self.version = version
        self.accessibility = accessibility
        self.model_format = model_format
        self.framework = framework
        self.workspace_id = workspace_id
        self.labels = labels
        self.description = description
        self.inference_spec = inference_spec or dict()

        # Read only fields
        self._model_id = model_id
        self._create_time = kwargs.pop("_create_time", None)
        self._modified_time = kwargs.pop("_modified_time", None)

    @classmethod
    @config_default_session
    def get_by_name_version(cls, model_name, version, session=None):
        model = Model.get_by_name(model_name, session=session)
        return cls.get_by_model_id_version(model.id, version, session=session)

    @classmethod
    @config_default_session
    def get(cls, model_id, version, session: Session = None) -> "ModelVersion":
        return cls.from_api_object(
            session.model_api.get_version(model_id=model_id, version=version),
            session=session,
        )

    @classmethod
    def get_latest_version(cls):
        pass

    @property
    def model(self):
        if not self._model_id:
            raise ValueError("Not registered model version.")
        return Model.get(self._model_id)

    @property
    def create_time(self):
        return self._create_time

    @property
    def modified_time(self):
        return self._modified_time

    def update(
        self,
        inference_spec,
    ):
        if not self._model_id:
            raise ValueError("Update method requires registered Model.")
        self.session.model_api.update_version(
            model_id=self.model_id, version=self.version, inference_spec=inference_spec
        )

    def delete(self):
        self.session.model_api.delete_version(
            model_id=self.model_id, version=self.version
        )

    def _update_inference_spec_by_model_property(self):
        """Config processor from model by ModelFormat."""

        # Check if inference_spec has been configured a processor.
        config = ServiceConfig.from_api_object(self.inference_spec or dict())
        if config.processor:
            return

        inference_spec = self.inference_spec or dict()

        # Get a default build-in processor for the model.
        build_in_processor = BuildInProcessor.from_model_format(self.model_format)
        if build_in_processor:
            inference_spec.update({"processor": build_in_processor})
        self.inference_spec = inference_spec

    def register(self):
        if (not self._model_id and not self.name) or (self._model_id and self.name):
            raise ValueError("Provide either model id or model name (not both).")

        if not self._model_id:
            model = Model.get_by_name(self.name, session=self.session)
            if not model:
                self._model_id = self.session.model_api.create(
                    name=self.name,
                    accessibility=self.accessibility,
                    workspace_id=self.workspace_id,
                )
            else:
                self._model_id = model.id
        # if self.session.model_api.get_version(self._model_id, version=self.version):
        #     raise ValueError(
        #         "Model version exists: name={} version={}".format(
        #             self.model.name, self.version
        #         )
        #     )

        self._update_inference_spec_by_model_property()

        self.session.model_api.create_version(
            model_id=self._model_id,
            version=self.version,
            uri=self.uri,
            model_format=self.model_format,
            framework=self.framework,
            labels=self.labels,
            description=self.description,
            inference_spec=self.inference_spec,
        )

        self.session.model_api.refresh_version(model_version=self)

    @classmethod
    @config_default_session
    def get_by_model_id_version(cls, model_id, version, session=None):
        """Get ModeVersion by model id and version.

        Args:
            model_id: Id for the model.
            version: Specific model version.

        Returns:
            ModelVersion:
        """
        return session.model_api.get_version(model_id=model_id, version=version)

    @classmethod
    @config_default_session
    def list(cls, name=None, session=None):
        # model = Model.get_by_name(name, session=session)
        pass

    @property
    def model_id(self):
        return self._model_id

    def _infer_processor_from_model_properties(self):
        if self.model_format == ModelFormat.PMML:
            pass

    def _make_service_config(
        self,
        service_name,
        compute_target,
        instance_count=1,
        service_group_name=None,
        inference_spec=None,
        blue_green_release=None,
    ):
        if inference_spec:
            config = ServiceConfig.from_api_object(inference_spec)
            config.name = service_name
        elif self.inference_spec:
            config = ServiceConfig.from_api_object(self.inference_spec)
            config.name = service_name
        else:
            config = ServiceConfig(name=service_name)

        if service_group_name:
            config.service_group_name = service_group_name

        config.compute_config = compute_target
        config.instance_count = instance_count
        parsed = parse_oss_url(self.uri)
        if parsed.endpoint:
            config.oss_endpoint = parsed.endpoint
        config.model_path = "oss://{}/{}".format(parsed.bucket_name, parsed.object_key)
        if blue_green_release is not None:
            config.blue_green_release = blue_green_release

        return config

    def deploy(
        self,
        service_name,
        service_group_name=None,
        instance_count=1,
        compute_target=None,
        wait_for_ready=False,
    ):

        self._update_inference_spec_by_model_property()
        config = self._make_service_config(
            service_name=service_name,
            compute_target=compute_target,
            service_group_name=service_group_name,
            instance_count=instance_count,
            inference_spec=self.inference_spec,
            blue_green_release=False,
        )

        self.session.service_api.create(config)
        eas_service: Service = Service.get(name=service_name)
        if wait_for_ready:
            eas_service.wait_for_ready()

        return eas_service

    def blue_green_deploy(
        self,
        service_name,
        compute_target=None,
        instance_count=1,
        wait_for_ready=False,
    ):

        self._update_inference_spec_by_model_property()
        config = self._make_service_config(
            service_name=service_name,
            compute_target=compute_target,
            instance_count=instance_count,
            inference_spec=self.inference_spec,
            blue_green_release=True,
        )

        green_service_name = self.session.service_api.create(config)
        eas_service: Service = Service.get(name=green_service_name)
        if wait_for_ready:
            eas_service.wait_for_ready()

        return eas_service

from __future__ import absolute_import

import logging
import six
import yaml

from .base import TemplateBase
from .core import Pipeline
from .step import PipelineStep
from .templates.container import ContainerTemplate
from .types.spec import load_input_output_spec
from ..core.session import get_default_session
from ..core.workspace import Workspace

logger = logging.getLogger(__name__)


def _load_pipeline_from_yaml(manifest):
    if isinstance(manifest, six.string_types):
        manifest = yaml.load(manifest, yaml.FullLoader)

    metadata = manifest["metadata"]
    (
        inputs,
        outputs,
    ) = load_input_output_spec(None, manifest["spec"])
    args_indexer = {ipt.enclosed_fullname: ipt for ipt in inputs}
    args_indexer.update({opt.enclosed_fullname: opt for opt in outputs})

    def set_variable_from(variable):
        if not variable.from_:
            return
        if not isinstance(variable.from_, six.string_types):
            raise ValueError(
                "Expected string type 'from' property, given type:%s",
                type(variable.from_),
            )
        if variable.from_ not in args_indexer:
            raise ValueError(
                "'from' value(%s) of variable(%s) not found in manifest.",
                (variable.from_, variable.name),
            )
        from_variable = args_indexer[variable.from_]
        variable._from = from_variable

        if variable.parent and from_variable.parent:
            variable.parent.after(from_variable.parent)

    if "pipelines" in manifest["spec"]:
        steps = []
        step_depends_by_name = {}

        pipeline_step_infos = manifest["spec"]["pipelines"]

        for step_info in pipeline_step_infos:
            step = PipelineStep(
                identifier=step_info["metadata"]["identifier"],
                provider=step_info["metadata"]["provider"],
                version=step_info["metadata"]["version"],
                name=step_info["metadata"]["name"],
            )
            steps.append(step)
            args_indexer.update({ipt.enclosed_fullname: ipt for ipt in step.inputs})
            args_indexer.update({opt.enclosed_fullname: opt for opt in step.outputs})
            step_depends_by_name[step_info["metadata"]["name"]] = step_info.get(
                "dependencies", []
            )

        step_naming_map = {step.name: step for step in steps}
        if len(step_naming_map) != len(steps):
            raise ValueError("Pipeline step name conflict")

        for idx, step_info in enumerate(pipeline_step_infos):
            step = steps[idx]
            step_args = step_info["spec"]["arguments"].get(
                "parameters", []
            ) + step_info["spec"]["arguments"].get("artifacts", [])
            step_inputs = {}
            for arg_dict in step_args:
                if arg_dict.get("from", None):
                    step_inputs[arg_dict["name"]] = args_indexer[arg_dict["from"]]
                elif "value" in arg_dict:
                    step_inputs[arg_dict["name"]] = arg_dict["value"]
                else:
                    raise ValueError(
                        "No 'from' or 'value' was given in pipeline step arguments."
                    )
            step.assign_inputs(step_inputs)

            depend_steps = [
                step_naming_map[depend_name]
                for depend_name in step_depends_by_name[step.name]
            ]

            for depend_step in depend_steps:
                if depend_step not in step.depends:
                    step.after(depend_step)

        for output in outputs:
            set_variable_from(output)

        p = Pipeline(
            identifier=metadata["identifier"],
            provider=metadata["provider"],
            version=metadata["version"],
            steps=steps,
            inputs=inputs,
            outputs=outputs,
        )
    elif "container" in manifest["spec"]:
        image_uri = manifest["spec"]["container"]["image"]
        command = manifest["spec"]["container"]["command"]
        image_pull_config = manifest["spec"]["container"].get("imageRegistryConfig")
        p = ContainerTemplate(
            identifier=metadata.get("identifier", None),
            provider=metadata.get("provider", None),
            version=metadata.get("version", None),
            image_uri=image_uri,
            command=command,
            image_registry_config=image_pull_config,
            inputs=inputs,
            outputs=outputs,
        )
    else:
        p = TemplateBase(
            identifier=metadata.get("identifier", None),
            provider=metadata.get("provider", None),
            version=metadata.get("version", None),
            inputs=inputs,
            outputs=outputs,
        )
    return p


class SavedTemplate(TemplateBase):
    """PipelineTemplate represent the pipeline schema from pipeline/component.

    PipelineTemplate object include the definition of "Workflow" use in PAI pipeline service.
     It could be fetch from remote pipeline service or construct from local Pipeline/Component.
     Saved pipeline template has unique `pipeline_id` which is generated by pipeline service.

    """

    def __init__(self, pipeline_id, workspace_id=None, manifest=None):
        """Template constructor.

        Args:
            manifest: "Workflow" definition of the pipeline.
            pipeline_id: Unique ID for pipeline in PAI service.
            workspace_id: ID of the workspace which the pipeline belongs to.
        """
        if not manifest or not workspace_id:
            session = get_default_session()
            manifest = session.get_pipeline_by_id(pipeline_id)["Manifest"]
        if isinstance(manifest, six.string_types):
            manifest = yaml.load(manifest, yaml.FullLoader)

        self._manifest = manifest
        self._pipeline_id = pipeline_id
        self._workspace_id = workspace_id

        inputs, outputs = load_input_output_spec(self, manifest["spec"])

        identifier = manifest["metadata"]["identifier"]
        provider = manifest["metadata"]["provider"]
        version = manifest["metadata"]["version"]
        super(SavedTemplate, self).__init__(
            inputs=inputs,
            outputs=outputs,
            identifier=identifier,
            provider=provider,
            version=version,
        )

    def __repr__(self):
        return "%s:Id=%s,Identifier=%s,Provider=%s,Version=%s" % (
            type(self).__name__,
            self._pipeline_id,
            self.identifier,
            self.provider,
            self.version,
        )

    @property
    def id(self):
        return self._pipeline_id

    @property
    def pipeline_id(self):
        """Unique ID of the pipeline in PAI pipeline service.

        Returns:
            str: Unique pipeline ID of the template instance.

        """
        return self._pipeline_id

    @property
    def manifest(self):
        """Pipeline manifest schema.

        Returns:
            dict: Pipeline manifest schema in dict.
        """
        return self._manifest

    @property
    def raw_manifest(self):
        """Pipeline manifest in YAML format

        Returns:
            str: Pipeline manifest.
        """
        return yaml.dump(self._manifest)

    @property
    def workspace(self):
        """Workspace of the pipeline template

        Pipeline template belongs to a specific workspace in PAI service. Workspace property reveal
         the workspace which the saved pipeline template belongs to.

        Returns:
            pai.core.workspace.Workspace: Workspace of the saved pipeline template.

        """
        return Workspace.get(self._workspace_id) if self._workspace_id else None

    @classmethod
    def get_by_identifier(cls, identifier, provider=None, version="v1"):
        """Get PipelineTemplate with identifier-provider-version tuple.

        Args:
            identifier (str): Pipeline identifier.
            provider (str): Provider of the Pipeline, account uid of the current session will be used as
              default.
            version (str): Version of the pipeline.

        Returns:
            pai.pipeline.template.SavedTemplate: PipelineTemplate instance

        """
        session = get_default_session()
        pipeline_info = session.get_pipeline(
            identifier=identifier, provider=provider, version=version
        )
        return cls(
            manifest=pipeline_info["Manifest"],
            pipeline_id=pipeline_info["PipelineId"],
            workspace_id=pipeline_info.get("WorkspaceId", None),
        )

    @classmethod
    def list(
        cls, identifier=None, provider=None, version=None, fuzzy=True, workspace=None
    ):
        """List the PipelineTemplate in PAI

        Search the pipeline templates available in remote PAI service. The method return a
        generator used to traverse the PipelineTemplate set match the query condition.

        Args:
            identifier (str): Pipeline identifier filter.
            provider (str): Pipeline provider filter.
            version (str): Pipeline version.
            fuzzy (bool): Fuzzy matching will be use to search pipeline template with the given
             `identifier` parameter if is True.
            workspace (pai.core.workspace.Workspace): Workspace filter.

        Yields:
              pai.pipeline.template.PipelineTemplate: PipelineTemplate match the query.
        """
        pl_gen = cls._get_service_client().list_pipeline(
            identifier=identifier,
            provider=provider,
            fuzzy=fuzzy,
            version=version,
            workspace_id=workspace.id if workspace else None,
        )

        for info in pl_gen:
            yield cls.deserialize(info)

    @classmethod
    def deserialize(cls, obj_dict):
        manifest, id, workspace_id = (
            obj_dict.get("Manifest"),
            obj_dict["PipelineId"],
            obj_dict["WorkspaceId"],
        )
        return cls(
            workspace_id=workspace_id,
            pipeline_id=id,
            manifest=manifest,
        )

    @classmethod
    def _has_impl(cls, manifest):
        if isinstance(manifest, six.string_types):
            manifest = yaml.load(manifest, yaml.FullLoader)

        if "spec" not in manifest:
            return False
        spec = manifest["spec"]
        if "pipelines" not in spec and "container" not in spec:
            return False
        return True

    def as_step(self, inputs=None, name=None):
        """Use the PipelineTemplate instance as a step in Pipeline workflow build.


        Args:
            inputs (dict): Inputs of the new step from the PipelineTemplate.
            name (str): Name of the new PipelineStep.

        Returns:
            pai.pipeline.step.PipelineStep: PipelineStep instance with the assigned inputs and name.

        """
        if not self.pipeline_id:
            raise ValueError(
                "Require saved pipeline/component to use as pipeline step."
            )
        return PipelineStep(
            identifier=self.identifier,
            provider=self.provider,
            version=self.version,
            inputs=inputs,
            name=name,
        )

    @classmethod
    def get(cls, pipeline_id):
        """Get PipelineTemplate with pipeline_id.

        Args:
            pipeline_id (str): Unique pipeline id.

        Returns:
            pai.pipeline.template.SavedTemplate: PipelineTemplate instance with the
             specific pipeline_id

        """
        client = cls._get_service_client()
        pipeline_info = client.get_pipeline(pipeline_id=pipeline_id)["Data"]
        return cls.deserialize(pipeline_info)

    def save(self, identifier=None, version=None):
        raise NotImplementedError("SaveTemplate is not savable.")

    def _submit(self, job_name, args):
        session = get_default_session()
        run_id = session.create_run(
            job_name,
            args,
            no_confirm_required=True,
            pipeline_id=self._pipeline_id,
            workspace=session.workspace,
        )
        return run_id

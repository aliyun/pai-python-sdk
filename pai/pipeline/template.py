from __future__ import absolute_import

import copy
import logging
import time
import uuid

import six
import yaml

from .core import Pipeline, ContainerComponent, PipelineBase
from .run import PipelineRun
from .step import PipelineStep
from .types.artifact import PipelineArtifact
from .types.parameter import PipelineParameter
from .types.spec import load_input_output_spec
from ..core.session import get_default_session
from ..core.workspace import Workspace
from ..decorator import cached_property

logger = logging.getLogger(__name__)


def _load_pipeline_from_yaml(manifest):
    if isinstance(manifest, six.string_types):
        manifest = yaml.load(manifest, yaml.FullLoader)

    metadata = manifest["metadata"]
    inputs, outputs, = load_input_output_spec(None, manifest["spec"])
    args_indexer = {ipt.enclosed_fullname: ipt for ipt in inputs}
    args_indexer.update({opt.enclosed_fullname: opt for opt in outputs})

    def set_variable_from(variable):
        if not variable.from_:
            return
        if not isinstance(variable.from_, six.string_types):
            raise ValueError("Expected string type 'from' property, given type:%s",
                             type(variable.from_))
        if variable.from_ not in args_indexer:
            raise ValueError("'from' value(%s) of variable(%s) not found in manifest.",
                             (variable.from_, variable.name))
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
            step_depends_by_name[step_info["metadata"]["name"]] = step_info.get("dependencies", [])

        step_naming_map = {step.name: step for step in steps}
        if len(step_naming_map) != len(steps):
            raise ValueError("Pipeline step name conflict")

        for idx, step_info in enumerate(pipeline_step_infos):
            step = steps[idx]
            step_args = step_info["spec"]["arguments"].get("parameters", []) + step_info["spec"][
                "arguments"].get("artifacts", [])
            step_inputs = {}
            for arg_dict in step_args:
                if arg_dict.get("from", None):
                    step_inputs[arg_dict["name"]] = args_indexer[arg_dict["from"]]
                elif "value" in arg_dict:
                    step_inputs[arg_dict["name"]] = arg_dict["value"]
                else:
                    raise ValueError("No 'from' or 'value' was given in pipeline step arguments.")
            step.assign_inputs(step_inputs)

            depend_steps = [step_naming_map[depend_name] for depend_name in
                            step_depends_by_name[step.name]]

            for depend_step in depend_steps:
                if depend_step not in step.depends:
                    step.after(depend_step)

        for output in outputs:
            set_variable_from(output)

        p = Pipeline(identifier=metadata["identifier"],
                     provider=metadata["provider"],
                     version=metadata["version"],
                     steps=steps,
                     inputs=inputs,
                     outputs=outputs)
    elif "execution" in manifest["spec"]:
        image_uri = manifest["spec"]["execution"]["image"]
        command = manifest["spec"]["execution"]["command"]
        image_pull_config = manifest["spec"]["execution"].get("imagePullConfig")
        p = ContainerComponent(
            identifier=metadata.get("identifier", None),
            provider=metadata.get("provider", None),
            version=metadata.get("version", None),
            image_uri=image_uri,
            command=command,
            image_pull_config=image_pull_config,
            inputs=inputs,
            outputs=outputs,
        )
    else:
        p = PipelineBase(
            identifier=metadata.get("identifier", None),
            provider=metadata.get("provider", None),
            version=metadata.get("version", None),
            inputs=inputs,
            outputs=outputs,
        )
    return p


class PipelineTemplate(object):
    """PipelineTemplate represent the pipeline schema build by user or fetched from PAI service.

    PipelineTemplate

    PipelineTemplate is used as runnable pipeline template communicate with PAI service.
    PipelineTemplate instance may be fetched from PAI service or extract from user build
    Pipeline, either is runnable with required arguments.

    """

    def __init__(self, manifest=None, pipeline_id=None, workspace_id=None):
        if not pipeline_id and not manifest:
            raise ValueError("Neither pipeline_id and manifest are given.")

        self._session = get_default_session()
        if not manifest:
            pipeline_info = self._session.get_pipeline_by_id(pipeline_id)
            manifest = pipeline_info["Manifest"]
        if isinstance(manifest, six.string_types):
            manifest = yaml.load(manifest, yaml.FullLoader)

        self._manifest = manifest
        self._pipeline_id = pipeline_id
        self._workspace_id = workspace_id
        self._inputs, self._outputs, = load_input_output_spec(self, manifest["spec"])

    def __repr__(self):
        return "%s: {PipelineId:%s, Identifier:%s, Provider:%s, Version:%s}" % (
            type(self).__name__, self._pipeline_id, self.identifier, self.provider, self.version)

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self._outputs

    @property
    def pipeline_id(self):
        return self._pipeline_id

    @property
    def manifest(self):
        return self._manifest

    @property
    def identifier(self):
        return self._manifest["metadata"]["identifier"]

    @property
    def provider(self):
        return self._manifest["metadata"]["provider"]

    @property
    def version(self):
        return self._manifest["metadata"]["version"]

    @cached_property
    def workspace(self):
        return Workspace.get(self._workspace_id) if self._workspace_id else None

    @classmethod
    def _get_pipeline_client(cls):
        return get_default_session().paiflow_client

    @classmethod
    def get_by_identifier(cls, identifier, provider=None, version="v1"):
        session = get_default_session()
        pipeline_info = session.get_pipeline(identifier=identifier, provider=provider,
                                             version=version)
        return cls(manifest=pipeline_info["Manifest"], pipeline_id=pipeline_info["PipelineId"],
                   workspace_id=pipeline_info.get("WorkspaceId", None))

    @classmethod
    def list(cls, identifier=None, provider=None, fuzzy=True, version=None, workspace=None):
        pl_gen = cls._get_pipeline_client().list_pipeline(
            identifier=identifier,
            provider=provider,
            fuzzy=fuzzy,
            version=version,
            workspace_id=workspace.id if workspace else None)

        for info in pl_gen:
            yield cls(pipeline_id=info["PipelineId"], workspace_id=info.get("WorkspaceId", None))

    @classmethod
    def load_by_identifier(cls, identifier, provider=None, version="v1", with_impl=False):
        session = get_default_session()
        pipeline_info = session.get_pipeline(identifier=identifier, provider=provider,
                                             version=version)
        if with_impl:
            pipeline_id = pipeline_info["PipelineId"]
            manifest = yaml.load(session.describe_pipeline(pipeline_id)["Manifest"],
                                 yaml.FullLoader)
        else:
            manifest = yaml.load(pipeline_info["Manifest"], yaml.FullLoader)
        component = _load_pipeline_from_yaml(manifest)
        component._pipeline_id = pipeline_info["PipelineId"]
        return component

    @classmethod
    def load(cls, pipeline_id, with_impl=False):
        client = cls._get_pipeline_client()

        if with_impl:
            manifest = yaml.load(client.describe_pipeline(pipeline_id)["Data"]["Manifest"],
                                 yaml.FullLoader)
        else:
            manifest = yaml.load(client.get_pipeline(pipeline_id)["Data"]["Manifest"],
                                 yaml.FullLoader)
        component = _load_pipeline_from_yaml(manifest)
        component._pipeline_id = pipeline_id
        return component

    def _have_impl(self):
        if "spec" not in self._manifest:
            return False
        spec = self._manifest["spec"]
        if "pipelines" not in spec and "execution" not in spec:
            return False
        return True

    def to_pipeline(self, with_impl=True):
        if not self._have_impl() and with_impl:
            if not self._pipeline_id:
                raise ValueError("Pipeline Template do not have implementation and is not saved.")
            client = self._get_pipeline_client()
            self._manifest = yaml.load(
                client.describe_pipeline(self._pipeline_id)["Data"]["Manifest"],
                yaml.FullLoader)

        component = _load_pipeline_from_yaml(self._manifest)
        if self._pipeline_id:
            component._pipeline_id = self._pipeline_id
        return component

    def as_step(self, inputs=None, name=None):
        if not self.pipeline_id:
            raise ValueError("Require saved pipeline/component to use as pipeline step.")
        return PipelineStep(identifier=self.identifier,
                            provider=self.provider,
                            version=self.version,
                            inputs=inputs,
                            name=name)

    @classmethod
    def get(cls, pipeline_id):
        client = cls._get_pipeline_client()
        pipeline_info = client.get_pipeline(pipeline_id=pipeline_id)["Data"]
        return cls(manifest=pipeline_info["Manifest"], pipeline_id=pipeline_info["PipelineId"])

    def translate_arguments(self, args):
        parameters, artifacts = [], []
        if not args:
            return parameters, artifacts
        parameters_spec = {ipt.name: ipt.to_dict() for ipt in self.inputs if
                           ipt.variable_category == "parameters"}
        artifacts_spec = {ipt.name: ipt.to_dict() for ipt in self.inputs if
                          ipt.variable_category == "artifacts"}

        for name, arg in args.items():
            if arg is None:
                continue
            param_spec = parameters_spec.get(name, None)
            af_spec = artifacts_spec.get(name, None)
            if param_spec:
                param = PipelineParameter.to_argument_by_spec(arg, param_spec)
                parameters.append(param)
            elif af_spec:
                af = PipelineArtifact.to_argument_by_spec(arg, af_spec, kind="inputs")
                artifacts.append(af)
            else:
                logger.warning(
                    "Provider useless argument:%s, it is not require by the pipeline manifest spec."
                    % name)

        requires = set(
            [param_name for param_name, spec in parameters_spec.items() if spec.get("required")]
            + [af_name for af_name, spec in artifacts_spec.items() if spec.get("required")])
        not_supply = requires - set(args.keys())

        if len(not_supply) > 0:
            raise ValueError("Required arguments is not supplied:%s" % ",".join(not_supply))
        return parameters, artifacts

    def save(self, identifier=None, version=None):
        if self.pipeline_id:
            raise ValueError("Pipeline template has been saved")

        session = get_default_session()
        provider = session.provider

        if identifier is None and version is None and self.pipeline_id:
            raise ValueError("Pipeline Manifest has been saved.")

        if not self.identifier and not identifier:
            raise ValueError("Required pipeline identifier.")

        if not self.version and not version:
            raise ValueError("Required pipeline version")

        self._manifest["metadata"]["provider"] = provider
        if identifier is not None:
            self._manifest["metadata"]["identifier"] = identifier or self.identifier
        if version is not None:
            self._manifest["metadata"]["version"] = version or self.version
        if "uuid" in self._manifest["metadata"]:
            del self._manifest["metadata"]["uuid"]

        self._pipeline_id = session.create_pipeline(self._manifest, workspace=session.workspace)
        return self

    def run(self, job_name, arguments, wait=True, log_outputs=True):
        session = get_default_session()
        if job_name is None:
            job_name = "tmp-{0}".format(int(time.time() * 1000))
        parameters, artifacts = self.translate_arguments(arguments)
        pipeline_args = {
            "parameters": parameters,
            "artifacts": artifacts,
        }

        pipeline_id, manifest = None, None
        if self.pipeline_id:
            pipeline_id = self.pipeline_id
        else:
            manifest = copy.deepcopy(self._manifest)
            if not self.identifier:
                manifest["metadata"]["identifier"] = 'tmp-%s' % uuid.uuid4().hex
                manifest["metadata"]["version"] = "v0"
        run_id = session.create_run(job_name, pipeline_args,
                                    no_confirm_required=True,
                                    pipeline_id=pipeline_id, manifest=manifest,
                                    workspace=session.workspace)

        run_instance = PipelineRun(run_id=run_id, name=job_name,
                                   workspace_id=session.workspace.id if session.workspace else None)
        if not wait:
            return run_instance
        run_instance.wait_for_completion(log_outputs=log_outputs)
        return run_instance

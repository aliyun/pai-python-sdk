from __future__ import absolute_import

import copy
import logging
import time
import uuid

import six
import yaml

from pai.pipeline import PipelineParameter, PipelineRun, PipelineStep, Pipeline
from pai.pipeline.core import ContainerComponent
from pai.pipeline.types.artifact import PipelineArtifact
from pai.pipeline.types.spec import load_input_output_spec
from pai.session import get_current_pai_session

logger = logging.getLogger(__name__)


def load_pipeline_from_yaml(manifest):
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
        raise ValueError("Unknown manifest implementation.")
    return p


class PipelineTemplate(object):

    def __init__(self, manifest=None, pipeline_id=None):
        if not pipeline_id and not manifest:
            raise ValueError("Neither pipeline_id and manifest are given.")

        self._session = get_current_pai_session()
        if not manifest:
            pipeline_info = self._session.get_pipeline_by_id(pipeline_id)
            manifest = pipeline_info["Manifest"]
        if isinstance(manifest, six.string_types):
            manifest = yaml.load(manifest, yaml.FullLoader)

        self._manifest = manifest
        self._pipeline_id = pipeline_id
        self._inputs, self._outputs, = load_input_output_spec(self, manifest["spec"])

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

    @classmethod
    def get_by_identifier(cls, identifier, provider=None, version="v1"):
        session = get_current_pai_session()
        pipeline_info = session.get_pipeline(identifier=identifier, provider=provider,
                                             version=version)
        return cls(manifest=pipeline_info["Manifest"], pipeline_id=pipeline_info["PipelineId"])

    @classmethod
    def load_by_identifier(cls, identifier, provider=None, version="v1"):
        pass

    def load(self):
        return

    @classmethod
    def get(cls, pipeline_id):
        session = get_current_pai_session()
        pipeline_info = session.get_pipeline_by_id(pipeline_id)
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
        session = get_current_pai_session()
        provider = session.provider

        if identifier is None and version is None and self.pipeline_id:
            raise ValueError("Pipeline Manifest has been saved.")

        self._manifest["metadata"]["provider"] = provider
        if identifier is not None:
            self._manifest["metadata"]["identifier"] = identifier
        if version is not None:
            self._manifest["metadata"]["version"] = version
        if "uuid" in self._manifest["metadata"]:
            del self._manifest["metadata"]["uuid"]

        self._pipeline_id = self._session.create_pipeline(self._manifest)
        return self

    def run(self, job_name, arguments, wait=True, log_outputs=True):
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
        run_id = self._session.create_run(job_name, pipeline_args,
                                          no_confirm_required=True,
                                          pipeline_id=pipeline_id, manifest=manifest)

        run_instance = PipelineRun(run_id=run_id, session=self._session)
        if not wait:
            return run_instance
        run_instance.wait_for_completion(log_outputs=log_outputs)
        return run_instance

    def to_estimator(self, parameters):
        from pai.estimator import PipelineEstimator
        return PipelineEstimator(pipeline_id=self.pipeline_id,
                                 manifest=self.manifest,
                                 parameters=parameters)

    def to_transformer(self, parameters):
        from pai.transformer import PipelineTransformer
        return PipelineTransformer(pipeline_id=self.pipeline_id,
                                   manifest=self.manifest,
                                   parameters=parameters)

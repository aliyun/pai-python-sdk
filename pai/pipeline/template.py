from __future__ import absolute_import

import copy
import logging
import time

import six
import yaml

from pai.pipeline import PipelineParameter, PipelineRun
from pai.pipeline.types.artifact import PipelineArtifact
from pai.pipeline.types.spec import load_input_output_spec
from pai.session import get_current_pai_session

logger = logging.getLogger(__name__)


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
        if identifier is None and version is None and self.pipeline_id:
            raise ValueError("Pipeline Manifest has been saved.")
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
            manifest = self._manifest
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

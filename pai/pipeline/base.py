from __future__ import absolute_import

import itertools
import logging
import time
from abc import ABCMeta

import six
import yaml

from .artifact import PipelineArtifact
from .parameter import PipelineParameter
from .run import RunInstance

Logger = logging.getLogger(__file__)

PyParameterTypes = tuple(itertools.chain(six.integer_types, six.string_types, [dict, list, bool]))


class PaiFlowBase(six.with_metaclass(ABCMeta, object)):
    _identifier_default = None
    _provider_default = None
    _version_default = None

    _pipeline_id = None

    _xflow_project = "algo_public"

    def __init__(self, session, manifest=None, pipeline_id=None):
        self.session = session
        self._manifest = manifest
        self._pipeline_id = pipeline_id

    def _prepare_run(self, manifest, job_name=None, arguments=None):
        artifacts_spec = {af["name"]: af for af in
                          manifest["spec"]["inputs"].get("artifacts", [])}
        parameters_spec = {param["name"]: param for param in
                           manifest["spec"]["inputs"].get("parameters", [])}
        parameters, artifacts = self.translate_arguments(arguments, parameters_spec,
                                                         artifacts_spec) if arguments else ([], [])
        if job_name is None:
            job_name = "{0}-{1}".format(manifest["metadata"]["identifier"][:3],
                                        int(time.time() * 1000))
        run_args = dict()
        if parameters:
            run_args["parameters"] = parameters
        if artifacts:
            run_args["artifacts"] = artifacts

        return job_name, run_args

    def _run(self, job_name=None, arguments=None, env=None):
        manifest = self.get_pipeline_definition()
        job_name, run_args = self._prepare_run(job_name=job_name, arguments=arguments,
                                               manifest=manifest)
        print(run_args)

        if self.get_pipeline_id():
            run_id = self.session.create_pipeline_run(name=job_name, arguments=run_args, env=env,
                                                      pipeline_id=self.get_pipeline_id(),
                                                      no_confirm_required=True)
        else:
            run_id = self.session.create_pipeline_run(name=job_name, arguments=run_args, env=env,
                                                      manifest=manifest, no_confirm_required=True)
        logging.info("PaiFlow CreateRun JobName:%s, RunId :%s" % (job_name, run_id))
        run = RunInstance(run_id=run_id, session=self.session)
        return run

    def translate_arguments(self, args, parameters_spec, artifacts_spec):
        """Transform arguments to pipeline inputs format"""
        parameters, artifacts = [], []
        if not args:
            return parameters, artifacts

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
                pass
                # raise ValueError("Argument %s is not support by pipeline manifest" % name)

        requires = set(
            [param_name for param_name, spec in parameters_spec.items() if spec.get("required")]
            + [af_name for af_name, spec in artifacts_spec.items() if spec.get("required")])
        not_supply = requires - set(args.keys())

        if len(not_supply) > 0:
            raise ValueError("Required arguments is not supplied:%s" % ",".join(not_supply))
        return parameters, artifacts

    def get_pipeline_id(self):
        return self._pipeline_id

    def get_identifier(self):
        return self._manifest["metadata"]["identifier"]

    def get_provider(self):
        return self._manifest["metadata"]["provider"]

    def get_version(self):
        return self._manifest["metadata"]["version"]

    def get_pipeline_definition(self):
        if self._manifest:
            return self._manifest

        pipeline_info = self.session.get_pipeline_by_id(pipeline_id=self.get_pipeline_id())

        if not pipeline_info.get("Manifest"):
            raise ValueError("Specific pipeline is not found, pipeline_id:%s" % (
                self.get_pipeline_id()))
        self._manifest = yaml.load(pipeline_info["Manifest"], yaml.FullLoader)
        return self._manifest

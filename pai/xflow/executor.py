from __future__ import absolute_import

import logging
from abc import ABCMeta
from functools import wraps
from pprint import pprint
import time

import six
import yaml

from ..pipeline.parameter import PipelineParameter
from ..pipeline.artifact import PipelineArtifact
from ..pipeline.run import RunInstance

Logger = logging.getLogger(__file__)


def reset_pipeline(func):
    @wraps(func)
    def _(self, *args, **kwargs):
        self._manifest = None
        return func(self, *args, **kwargs)

    return _


class PaiFlowExecutor(six.with_metaclass(ABCMeta, object)):
    _identifier_cls = None
    _provider_cls = None
    _version_cls = None

    _xflow_project = "algo_public"

    def __init__(self, session):
        self.session = session
        self._manifest = None
        self._artifacts = dict()
        self._initialize()

    def _prepare_run(self, job_name=None, *inputs, **kwargs):
        manifest = yaml.load(self.get_pipeline_definition(), yaml.FullLoader)
        self._artifacts = {af["name"]: af for af in manifest["spec"]["inputs"].get("artifacts", [])}
        self._parameters = {param["name"]: param for param in manifest["spec"]["inputs"].get("parameters", [])}
        args = self._compile_args(*inputs, **kwargs)
        pipeline_args = self.translate_arguments(args)

        if job_name is None:
            job_name = "{0}-{1}".format(self.get_identifier(), int(time.time() * 1000))

        env = self.get_run_env()
        return job_name, pipeline_args, env

    def get_run_env(self):
        env = {
            "resource": {
                "compute": {
                    "max_compute": {
                        "__odpsInfoFile": "/share/base/odpsInfo.ini",
                        "endpoint": "http://service.{}.maxcompute.aliyun.com/api" .format(self.session.region_id),
                        "logViewHost": "http://logview.odps.aliyun.com",
                        "odpsProject": self.session.odps_project,
                    }
                }
            },
            "workflowService": {
                "config": {
                    "endpoint": "http://service.{}.argo.aliyun.com".format(self.session.region_id)
                },
                "name": "argo"
            }
        }
        return env

    def _initialize(self):
        workflow_config = {
            "config": {"endpoint": "http://service.%s.argo.aliyun.com" % self.session.region_id},
            "name": "argo"
        }
        self._workflow_config = workflow_config

    def _compile_args(self, *input, **kwargs):
        return dict()

    def get_xflow_project(self):
        return self._xflow_project

    # TODO: refactor using decorator setter, getter
    @reset_pipeline
    def set_identifier(self, identifier):
        self._identifier = identifier
        return self

    def get_identifier(self):
        if hasattr(self, "_identifier"):
            return self._identifier
        return self._identifier_cls

    @reset_pipeline
    def set_provider(self, provider):
        self._provider = provider
        return self

    def get_provider(self):
        if hasattr(self, "_provider"):
            return self._provider
        return self._provider_cls

    @reset_pipeline
    def set_version(self, version):
        self._version = version
        return self

    def get_version(self):
        if hasattr(self, "_version"):
            return self._version
        return self._version_cls

    def get_pipeline_definition(self):
        if self._manifest:
            return self._manifest

        identifier = self.get_identifier()
        provider = self.get_provider()
        version = self.get_version()

        pipeline_info = self.session.get_pipeline(identifier=identifier,
                                                  provider=provider,
                                                  version=version)

        if not pipeline_info.get("Manifest"):
            raise ValueError("Specific pipeline is not found, identifier:%s, provider:%s, version:%s" % (
                identifier, provider, version))

        self._manifest = pipeline_info["Manifest"]
        return self._manifest

    def get_arguments(self):
        pass

    def _run(self, job_name=None, *inputs, **kwargs):
        job_name, pipeline_args, env = self._prepare_run(job_name, *inputs, **kwargs)
        manifest = self.get_pipeline_definition()
        logging.info("PaiFlowExecutor Run Pipeline:JobName:%s, Metadata: %s:%s:%s" % (
            job_name, self.get_identifier(), self.get_provider(), self.get_version()))

        pprint(pipeline_args)
        logging.info("Arguments is :%s" % str(pipeline_args))

        run_id = self.session.create_pipeline_run(name=job_name, arguments=pipeline_args, env=env,
                                                  manifest=manifest)
        logging.info("PaiFlowRunnerId is :%s" % run_id)

        run = RunInstance(run_id=run_id, session=self.session)
        return run

    def translate_arguments(self, args):
        """Transform arguments to pipeline inputs format"""
        parameters, artifacts = [], []
        for name, arg in args.items():
            if arg is None:
                continue
            param_spec = self._parameters.get(name, None)
            af_spec = self._artifacts.get(name, None)
            if param_spec:
                param = PipelineParameter.to_argument_by_spec(arg, param_spec)
                parameters.append(param)
            elif af_spec:
                af = PipelineArtifact.to_argument_by_spec(arg, param_spec)
                artifacts.append(af)
            else:
                raise ValueError("Argument %s is not required by pipeline manifest" % name)

        requires = set([param_name for param_name, spec in self._parameters.items() if spec.get("required")] + \
                       [af_name for af_name, spec in self._artifacts.items() if spec.get("required")])
        not_supply = requires - set(args.keys())
        if len(not_supply) > 0:
            raise ValueError("Required arguments is not supplied:%s" % ",".join(not_supply))

        return parameters, artifacts


def _to_pipeline_argument(name, value=None, from_=None):
    d = {
        "name": name,
    }

    if value is not None:
        d["value"] = value
    elif from_ is not None:
        d["from"] = from_
    else:
        raise ValueError("Argument need either value or from_, both of them is None.")

    return d

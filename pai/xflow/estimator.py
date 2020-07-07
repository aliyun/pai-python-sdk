from __future__ import absolute_import

from .executor import PaiFlowExecutor


class Estimator(object):

    def __init__(self, session, **kwargs):
        self._session = session
        self._parameters = kwargs
        self._runs = []

    def fit(self, wait=True, job_name=None, **kwargs):
        for name, param in self._parameters.items():
            if name not in kwargs:
                kwargs[name] = param
        run_instance = self._run(wait=wait, job_name=job_name, **kwargs)

        self._runs.append(run_instance)

        if wait:
            run_instance.wait()


class XFlowEstimator(PaiFlowExecutor, Estimator):
    _default_xflow_project = "algo_public"

    def __init__(self, session, xflow_project=None, **kwargs):
        self.xflow_project = xflow_project or self._default_xflow_project
        Estimator.__init__(self, session=session, **kwargs)
        PaiFlowExecutor.__init__(self, session=session)

    def get_xflow_project(self):
        return self._xflow_project

    def get_execution(self):
        region_id = self.session.region_id
        odps_project = self.session.odps_project
        return {
            "__odpsInfoFile": "/share/base/odpsInfo.ini",
            "endpoint": "http://service.%s.maxcompute.aliyun.com/api" % region_id,
            "logViewHost": "http://logview.odps.aliyun.com",
            "odpsProject": "%s" % odps_project
        }

    def _compile_args(self, *inputs, **kwargs):
        args = super(XFlowEstimator, self)._compile_args(*inputs, **kwargs)
        args["__execution"] = self.get_execution()
        args["__xflowProject"] = self.get_xflow_project()
        return args


class XFlowModelTransferEstimator(XFlowEstimator):

    def __init__(self, **kwargs):
        super(XFlowModelTransferEstimator, self).__init__(**kwargs)

    def _compile_args(self, *inputs, **kwargs):
        args = super(XFlowModelTransferEstimator, self)._compile_args(*inputs, **kwargs)
        generate_pmml = kwargs.get("generate_pmml")
        if generate_pmml:
            args["__pmmlModelVolume"] = kwargs.get("pmml_model_volume")
            args["__pmmlModelPartition"] = kwargs.get("pmml_model_partition")
            args["__modelPartition"] = kwargs.get("model_partition")
            args["__pmmlModelPublicProject"] = kwargs.get("pmml_model_public_project")
            args["__pmmlModelPublicEndpoint"] = kwargs.get("pmml_model_public_endpoint")
        return args

    def create_model(self):
        raise NotImplementedError

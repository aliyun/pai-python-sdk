from pai.estimator import PipelineEstimator, AlgoBaseEstimator


class XFlowEstimator(AlgoBaseEstimator):
    _default_xflow_project = "algo_public"

    def __init__(self, session, xflow_project=None, odps_project=None, **kwargs):
        super(XFlowEstimator, self).__init__(session=session, **kwargs)
        self.xflow_project = xflow_project or self._default_xflow_project
        self.odps_project = odps_project or self.session.odps_project

    def fit(self, wait=True, job_name=None, **kwargs):
        return super(XFlowEstimator, self).fit(wait=True, job_name=job_name, args=kwargs)

    def get_xflow_project(self):
        return self._default_xflow_project

    def get_run_env(self):
        env = {
            "resource": {
                "compute": {
                    "max_compute": {
                        "__odpsInfoFile": "/share/base/odpsInfo.ini",
                        "endpoint": "http://service.{}.maxcompute.aliyun.com/api".format(self.session.region_id),
                        "logViewHost": "http://logview.odps.aliyun.com",
                        "odpsProject": self.odps_project,
                    }
                }
            }
        }
        return env

    def get_execution(self):
        region_id = self.session.region_id
        odps_project = self.session.odps_project
        return {
            "__odpsInfoFile": "/share/base/odpsInfo.ini",
            "endpoint": "http://service.%s.maxcompute.aliyun.com/api" % region_id,
            "logViewHost": "http://logview.odps.aliyun.com",
            "odpsProject": "%s" % odps_project
        }

    def compile_args(self, **kwargs):
        super(XFlowEstimator, self).compile_args()
        args = {
            "__execution": self.get_execution(),
            "__xflowProject": self.get_xflow_project(),
        }
        return args

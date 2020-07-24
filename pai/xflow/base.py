from __future__ import absolute_import

from pai.estimator import AlgoBaseEstimator
from pai.transformer import AlgoBaseTransformer


class _XFlowAlgoMixin(object):
    _enable_sparse = False
    XFlowProjectDefault = 'algo_public'

    def __init__(self, xflow_execution=None, xflow_project=None, core_num=None,
                 mem_size_per_core=None):
        self.xflow_project = xflow_project or self.XFlowProjectDefault
        self.xflow_execution = xflow_execution
        self.core_num = core_num
        self.mem_size_per_core = mem_size_per_core

    def get_xflow_execution(self):
        if self.xflow_execution:
            return self.xflow_execution
        return {
            "odpsInfoFile": "/share/base/odpsInfo.ini",
            "endpoint": str(self.session.odps_client.endpoint),
            "logViewHost": str(self.session.odps_client.logview_host),
            "odpsProject": str(self.session.odps_project),
        }

    def get_xflow_project(self):
        return self.xflow_project

    def get_xflow_args(self):
        return {
            "execution": self.get_xflow_execution(),
            "project": self.get_xflow_project(),
        }

    def _compile_args(self, *inputs, **kwargs):
        args = self.get_xflow_args()
        if type(self)._enable_sparse and kwargs.get("enable_sparse"):
            args["enableSparse"] = True
            sparse_delimiter = kwargs["sparse_delimiter"]
            item_delimiter, kv_delimiter = sparse_delimiter
            args["itemDelimiter"] = item_delimiter
            args["kvDelimiter"] = kv_delimiter
        args["coreNum"] = kwargs.get("coreNum")
        args["memSizePerCore"] = kwargs.get("mem_size_per_core")

        return args


class XFlowEstimator(AlgoBaseEstimator, _XFlowAlgoMixin):
    _pmml_model = False

    def __init__(self, session, xflow_project=None, xflow_execution=None, **kwargs):
        AlgoBaseEstimator.__init__(self, session=session, pmml_gen=False, pmml_oss_path=None,
                                   pmml_oss_endpoint=None, pmml_oss_rolearn=None,
                                   pmml_oss_bucket=None, **kwargs)
        _XFlowAlgoMixin.__init__(self, xflow_project=xflow_project, xflow_execution=xflow_execution)

    def _compile_args(self, *inputs, **kwargs):
        args = super(XFlowEstimator, self)._compile_args(*inputs, **kwargs)
        if type(self)._pmml_model and kwargs.get("generate_pmml"):
            args["path"] = kwargs.get("oss_path")
            args["endpoint"] = kwargs.get("oss_endpoint")
            args["rolearn"] = kwargs.get("rolearn")
            args["bucket"] = kwargs.get("oss_bucket")
            args["generatePmml"] = kwargs.get("generate_pmml")

        return args


class XFlowTransformer(AlgoBaseTransformer, _XFlowAlgoMixin):

    def __init__(self, session, xflow_execution=None, xflow_project=None, **kwargs):
        AlgoBaseTransformer.__init__(self, session=session, **kwargs)
        _XFlowAlgoMixin.__init__(self, xflow_project=xflow_project, xflow_execution=xflow_execution)

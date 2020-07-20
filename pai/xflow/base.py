from __future__ import absolute_import

from pai.estimator import AlgoBaseEstimator
from pai.transformer import AlgoBaseTransformer


class _XFlowAlgoMixin(object):
    _enable_sparse_input = False
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
            "__XFlow_execution": self.get_xflow_execution(),
            "__XFlow_project": self.get_xflow_project(),
        }

    def _compile_args(self, *inputs, **kwargs):
        args = self.get_xflow_args()
        if type(self)._enable_sparse_input and kwargs.get("enable_sparse"):
            args["enableSparse"] = True
            sparse_delimiter = kwargs["sparse_delimiter"]
            item_delimiter, kv_delimiter = sparse_delimiter
            args["itemDelimiter"] = item_delimiter
            args["kvDelimiter"] = kv_delimiter
        args["coreNum"] = kwargs.get("coreNum")
        args["memSizePerCore"] = kwargs.get("mem_size_per_core")

        return args


class XFlowEstimator(AlgoBaseEstimator, _XFlowAlgoMixin):

    def __init__(self, session, xflow_project=None, xflow_execution=None, **kwargs):
        AlgoBaseEstimator.__init__(self, session=session, **kwargs)
        _XFlowAlgoMixin.__init__(self, xflow_project=xflow_project, xflow_execution=xflow_execution)


class XFlowTransformer(AlgoBaseTransformer, _XFlowAlgoMixin):

    def __init__(self, session, xflow_execution=None, xflow_project=None, **kwargs):
        AlgoBaseTransformer.__init__(self, session=session, **kwargs)
        _XFlowAlgoMixin.__init__(self, xflow_project=xflow_project, xflow_execution=xflow_execution)

from __future__ import absolute_import

from pai.estimator import AlgoBaseEstimator
from pai.transformer import AlgoBaseTransformer


class _XFlowAlgoMixin(object):

    enable_sparse = False
    XFlowProjectDefault = 'algo_public'

    def __init__(self, xflow_execution=None, xflow_project=None):
        self.xflow_project = xflow_project or self.XFlowProjectDefault
        self.xflow_execution = xflow_execution

    def get_xflow_execution(self):
        if self.xflow_execution:
            return self.xflow_execution
        region_id = self.session.region_id
        odps_project = self.session.odps_project
        return {
            "__odpsInfoFile": "/share/base/odpsInfo.ini",
            "endpoint": "http://service.%s.maxcompute.aliyun.com/api" % region_id,
            "logViewHost": "http://logview.odps.aliyun.com",
            "odpsProject": "%s" % odps_project
        }

    def get_xflow_project(self):
        return self.xflow_project

    def get_xflow_args(self):
        return {
            "__XFlow_execution": self.get_xflow_execution(),
            "__XFlow_project": self.get_xflow_project(),
            # TODO: Remove after pipeline manifest upgraded.
            "__execution": self.get_xflow_execution(),
            "__xflowProject": self.get_xflow_project(),
        }

    def compile_args(self, *inputs, **kwargs):
        args = self.get_xflow_args()
        if self.enable_sparse and kwargs.pop("enable_sparse"):
            args["enableSparse"] = True
            sparse_delimiter = kwargs["sparse_delimiter"]
            item_delimiter, kv_delimiter = sparse_delimiter
            args["itemDelimiter"] = item_delimiter
            args["kvDelimiter"] = kv_delimiter
        return args


class XFlowEstimator(AlgoBaseEstimator, _XFlowAlgoMixin):

    def __init__(self, session, xflow_project=None, xflow_execution=None, **kwargs):
        AlgoBaseEstimator.__init__(self, session=session, **kwargs)
        _XFlowAlgoMixin.__init__(self, xflow_project=xflow_project, xflow_execution=xflow_execution)


class XFlowTransformer(AlgoBaseTransformer, _XFlowAlgoMixin):

    def __init__(self, session, xflow_execution=None, xflow_project=None, **kwargs):
        AlgoBaseTransformer.__init__(self, session=session, parameters=kwargs)
        _XFlowAlgoMixin.__init__(self, xflow_project=xflow_project, xflow_execution=xflow_execution)

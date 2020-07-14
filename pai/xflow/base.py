from __future__ import absolute_import

from pai.estimator import AlgoBaseEstimator
from pai.transformer import AlgoBaseTransformer


class _XFlowAlgoMixin(object):
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


class XFlowEstimator(AlgoBaseEstimator, _XFlowAlgoMixin):
    _default_xflow_project = "algo_public"

    def __init__(self, session, xflow_project=None, xflow_execution=None, **kwargs):
        AlgoBaseEstimator.__init__(self, session=session, _compile_args=True, **kwargs)
        _XFlowAlgoMixin.__init__(self, xflow_project=xflow_project, xflow_execution=xflow_execution)

    def compile_args(self, **kwargs):
        args = super(XFlowEstimator, self).compile_args()
        args.update(self.get_xflow_args())
        return args


class XFlowTransformer(AlgoBaseTransformer, _XFlowAlgoMixin):
    XFlowProjectDefault = 'algo_public'

    def __init__(self, session, xflow_execution=None, xflow_project=None, **kwargs):
        AlgoBaseTransformer.__init__(self, session=session, _compile_args=True, parameters=kwargs)
        _XFlowAlgoMixin.__init__(self, xflow_project=xflow_project, xflow_execution=xflow_execution)

    def compile_args(self, *inputs, **kwargs):
        args = super(XFlowTransformer, self).compile_args(*inputs, **kwargs)
        args.update(self.get_xflow_args())
        return args

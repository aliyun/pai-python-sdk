from abc import ABCMeta
import six

from pai.base import PaiFlowBase
from pai import ProviderAlibabaPAI
from pai.transformer import PipelineTransformer


class XFlowOfflineModelTransformer(PipelineTransformer):
    _identifier_default = "prediction-xflow-ODPS"

    _version_default = "v1"

    _provider_default = ProviderAlibabaPAI

    def __init__(self, session, model, **kwargs):
        super(XFlowOfflineModelTransformer, self).__init__(session=session, model=model, **kwargs)
        self.model = model

    def compare_args(self, **kwargs):
        pass

    def transform(self, input_data, wait=True, job_name=None, ):
        return super(XFlowOfflineModelTransformer, self).transform()

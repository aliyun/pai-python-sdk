from abc import ABCMeta, abstractmethod
import six

from .executor import PaiFlowExecutor
from .. import ProviderAlibabaPAI


class Transformer(six.with_metaclass(ABCMeta, object)):

    def __init__(self, session, **kwargs):
        self.session = session
        self._parameters = kwargs

    def transform(self, *inputs, **kwargs):
        pass

    @abstractmethod
    def _transform(self, *inputs, **kwargs):
        raise NotImplementedError

    def parameters(self):
        return self._parameters


class ModelTransformer(Transformer):

    def __init__(self, session, model, **kwargs):
        self._model = model
        super(ModelTransformer, self).__init__(session, **kwargs)


class XFlowOfflineModelTransformer(PaiFlowExecutor, ModelTransformer):

    _identifier_default = "prediction-xflow-ODPS"

    _version_default = "v1"

    _provider_default = ProviderAlibabaPAI

    def __init__(self, session, model, **kwargs):
        super(XFlowOfflineModelTransformer, self).__init__(session=session, model=model, **kwargs)

    def transform(self, *inputs, **kwargs):
        self._run()
        return self.get_outputs()

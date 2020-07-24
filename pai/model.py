from __future__ import absolute_import


class Model(object):

    def __init__(self, name, model_data, session):
        self.model_data = model_data
        self.name = name
        self.session = session

    def deploy(self):
        raise NotImplementedError

    def transformer(self):
        raise NotImplementedError

    def from_artifact(self, name, artifact):
        pass


class PmmlModel(Model):

    def __init__(self, name, model_data, session):
        super(PmmlModel, self).__init__(name=name, session=session, model_data=model_data)


class XFlowOfflineModel(Model):

    def __init__(self, session, name, model_data):
        super(XFlowOfflineModel, self).__init__(name=name, session=session, model_data=model_data)

    def transformer(self):
        from .xflow.transformer import OfflineModelTransformer
        return OfflineModelTransformer(session=self.session, model=self.model_data)

    # TODO:
    def deploy(self):
        pass

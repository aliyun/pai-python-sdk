class Model(object):

    def __init__(self, name, model_data, session):
        self.model_data = model_data
        self.name = name
        self.session = session

    def deploy(self):
        raise NotImplementedError

    def transformer(self):
        raise NotImplementedError


class PmmlModel(Model):

    def __init__(self, name, model_data, location_type, session):
        super(PmmlModel, self).__init__(name=name, session=session, model_data=model_data)


class XFlowOfflineModel(Model):

    def __init__(self, session, odps_project, name, model_data):
        super(XFlowOfflineModel, self).__init__(name=name, session=session, model_data=model_data)
        self.odps_project = odps_project

    def transformer(self):
        pass

    # TODO:
    def deploy(self):
        pass

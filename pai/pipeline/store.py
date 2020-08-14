import yaml

from pai.session import Session


class PAIFlowPipelineStore(object):

    def __init__(self, session=None):
        self._session = session or Session.get_current_session()

    def session(self):
        return self._session

    def get(self, identifier, provider=None, version="v1"):
        provider = provider or self._session.provider
        return yaml.load(
            self._session.get_pipeline(identifier=identifier, provider=provider, version=version)["Manifest"],
            yaml.FullLoader)

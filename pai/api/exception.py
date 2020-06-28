import inspect

from pai.exception import PAIException


class ServiceCallException(PAIException):

    def __init__(self, request_class, message):
        self._request_class = request_class
        super(ServiceCallException, self).__init__(message)

    def __str__(self):
        cls = self._request_class
        if not inspect.isclass(self._request_class):
            cls = type(self._request_class)
        return 'Failed to call PAI service. Error message: {1}. The request class is: {0},'.format(
            cls, self.message)

    @property
    def request_class(self):
        return self._request_class

    @property
    def message(self):
        return self._message

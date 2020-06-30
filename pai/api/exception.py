import inspect

from pai.exception import PAIException


class ServiceCallException(PAIException):

    def __init__(self, message):
        super(ServiceCallException, self).__init__(message)

    def __str__(self):
        return 'AlibabaCloud API Call Error.{0}'.format(self.message)

    @property
    def message(self):
        return self._message

from __future__ import absolute_import


class PAIException(Exception):
    def __init__(self, message):
        self._message = message

    @property
    def message(self):
        return self._message

    def __str__(self):
        return self.message


class NotSupportException(PAIException):
    def __init__(self, message):
        super(NotSupportException, self).__init__(message)


class TimeoutException(PAIException):
    def __init__(self, message):
        super(TimeoutException, self).__init__(message)


class ServiceCallException(PAIException):

    def __init__(self, message):
        super(ServiceCallException, self).__init__(message)

    def __str__(self):
        return 'AlibabaCloud API Call Error.{0}'.format(self.message)

    @property
    def message(self):
        return self._message
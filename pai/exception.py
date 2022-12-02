from __future__ import absolute_import


class PAIException(Exception):
    def __init__(self, message):
        self._message = message

    @property
    def message(self):
        return self._message

    def __str__(self):
        return self.message


class UnExpectedStatusException(PAIException):
    def __init__(self, message, status):
        super(UnExpectedStatusException, self).__init__(message)
        self.status = status

    def __str__(self):
        return "UnExpectedStatusException: {} status={}".format(
            self.message, self.status
        )

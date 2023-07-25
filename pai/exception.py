from __future__ import absolute_import


class PAIException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class PredictionException(PAIException):
    def __init__(self, code, message):
        super(PredictionException, self).__init__(message)
        self.code = code
        self.message = message

    def __str__(self):
        return f"PredictionException: Code={self.code}, Message={self.message}"


class UnexpectedStatusException(PAIException):
    """Raised when resource status is not expected."""

    def __init__(self, message, status):
        self.status = status
        super(UnexpectedStatusException, self).__init__(message)

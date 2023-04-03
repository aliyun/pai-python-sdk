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

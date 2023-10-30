from __future__ import absolute_import


class PAIException(Exception):
    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return "{}: {}".format(type(self).__name__, self.message)

    def __str__(self):
        return self.__repr__()


class PredictionException(PAIException):
    def __init__(self, code, message):
        super(PredictionException, self).__init__(message)
        self.code = code
        self.message = message

    def __repr__(self):
        return "{}: code={}, {}".format(type(self).__name__, self.code, self.message)


class UnexpectedStatusException(PAIException):
    """Raised when resource status is not expected."""

    def __init__(self, message, status):
        self.status = status
        super(UnexpectedStatusException, self).__init__(message)

    def __repr__(self):
        return "{}: status={}, {}".format(
            type(self).__name__, self.status, self.message
        )


class DuplicatedMountException(PAIException):
    """Raised if a OSS path is mounted twice."""


class MountPathIsOccupiedException(PAIException):
    """Raised if target mount path is already used."""

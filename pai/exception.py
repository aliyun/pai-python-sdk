#  Copyright 2023 Alibaba, Inc. or its affiliates.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


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

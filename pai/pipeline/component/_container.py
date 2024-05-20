# coding: utf-8

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

from __future__ import print_function

import uuid

import six
from deprecated import deprecated

from ...common.logging import get_logger
from ...common.yaml_utils import dump as yaml_dump
from ...session import get_default_session
from ..types.variable import PipelineVariable
from ._base import UnRegisteredComponent

PAI_MANIFEST_SPEC_INPUTS_ENV_KEY = "PAI_MANIFEST_SPEC_INPUTS"
PAI_MANIFEST_SPEC_OUTPUTS_ENV_KEY = "PAI_MANIFEST_SPEC_OUTPUTS"
PAI_INPUTS_PARAMETERS_ENV_KEY = "PAI_INPUTS_PARAMETERS"

_logger = get_logger(__name__)


@deprecated(
    reason="ContainerComponent is deprecated and will be removed in the future."
)
class ContainerComponent(UnRegisteredComponent):
    def __init__(
        self,
        image_uri,
        command,
        args=None,
        image_registry_config=None,
        inputs=None,
        outputs=None,
        env=None,
    ):
        self._image_uri = image_uri
        self._image_registry_config = image_registry_config
        self._command = command
        self._args = args
        self._env = env
        self._guid = uuid.uuid4().hex

        super(ContainerComponent, self).__init__(
            inputs=inputs,
            outputs=outputs,
        )

    @classmethod
    def _transform_env(cls, env):
        if not env:
            return dict()
        return {
            k: v.enclosed_fullname if isinstance(v, PipelineVariable) else str(v)
            for k, v in env.items()
        }

    @classmethod
    def _transform_commands(cls, commands):
        if isinstance(commands, six.string_types):
            return [commands]
        if not commands:
            return []

        return [
            c.enclosed_fullname if isinstance(c, PipelineVariable) else c
            for c in commands
        ]

    def to_dict(self, identifier=None, version=None):
        d = super(ContainerComponent, self).to_dict()

        if identifier is not None:
            d["metadata"]["identifier"] = identifier
        if version is not None:
            d["metadata"]["version"] = version

        if get_default_session():
            d["metadata"]["provider"] = get_default_session().provider

        d["spec"]["container"] = {
            "image": self._image_uri,
            "command": self._transform_commands(self._command),
        }
        d["spec"]["container"]["imageRegistryConfig"] = (
            self._image_registry_config or dict()
        )
        if self._env:
            d["spec"]["container"]["envs"] = self._transform_env(self._env or dict())

        if self._args:
            d["spec"]["container"]["args"] = self._transform_commands(self._args)
        return d

    def to_manifest(self, identifier, version):
        return yaml_dump(self.to_dict(identifier=identifier, version=version))

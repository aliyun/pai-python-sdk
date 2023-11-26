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

from typing import Any, Dict, List, Union

from ..libs.alibabacloud_aiworkspace20210204.models import (
    ListImageLabelsRequest,
    ListImageLabelsResponseBody,
    ListImagesRequest,
    ListImagesResponseBody,
)
from .base import PaginatedResult, ServiceName, WorkspaceScopedResourceAPI

SUPPORTED_IMAGE_FRAMEWORKS = [
    "DeepRec",
    "DeepSpeed",
    "Megatron-LM",
    "ModelScope",
    "Nemo",
    "OneFlow",
    "PyTorch",
    "TensorFlow",
    "Transformers",
    "XGBoost",
]

SUPPORTED_IMAGE_LANGUAGES = [
    "python",  # TODO: "Python"
]


class ImageLabel(object):
    """Image Label Class."""

    # Unofficial Image Label
    UNOFFICIAL_LABEL = "system.official=false"
    # Official Image Label
    OFFICIAL_LABEL = "system.official=true"

    # PAI Image Label
    PROVIDER_PAI_LABEL = "system.origin=PAI"
    # Community Image Label
    PROVIDER_COMMUNITY_LABEL = "system.origin=Community"

    # DLC Image Label: for training
    DLC_LABEL = "system.supported.dlc=true"
    # EAS Image Label: for inference
    EAS_LABEL = "system.supported.eas=true"
    # DSW Image Label: for develop
    DSW_LABEL = "system.supported.dsw=true"

    # Accelerator: Use GPU
    DEVICE_TYPE_GPU = "system.chipType=GPU"
    DEVICE_TYPE_CPU = "system.chipType=CPU"

    # Python Version
    # TODO: delete this label key
    PYTHON_VERSION = "system.pythonVersion"

    @staticmethod
    def framework_version(
        framework: str,
        version: str,
    ):
        """Create a label for filtering images that support specific framework version.

        Args:
            framework (str): framework name, which is case sensitive.
            version (str): framework version. If version is '*', it will match all
                versions.

        Returns:
            str: framework version label string.

        Raises:
            ValueError: If the framework is not supported.
        """
        if framework not in SUPPORTED_IMAGE_FRAMEWORKS:
            raise ValueError(
                f"Unsupported framework: {framework}. Current supported frameworks are:"
                f" {SUPPORTED_IMAGE_FRAMEWORKS}"
            )
        return f"system.framework.{framework}={version}"

    @staticmethod
    def language_version(
        language: str,
        version: str,
    ):
        """Create a label for filtering images that support specific language version.

        Args:
            language (str): language name, which is case sensitive.
            version (str): language version. If version is '*', it will match all
                versions.

        Returns:
            str: language version label string.

        Raises:
            ValueError: If the language is not supported.
        """
        if language not in SUPPORTED_IMAGE_LANGUAGES:
            raise ValueError(
                f"Unsupported language: {language}. Current supported languages are:"
                f" {SUPPORTED_IMAGE_LANGUAGES}"
            )
        # TODO: "system.language.{language}={version}"
        return f"system.{language}Version={version}"


class ImageAPI(WorkspaceScopedResourceAPI):
    """Class which provide API to operate CodeSource resource."""

    BACKEND_SERVICE_NAME = ServiceName.PAI_WORKSPACE

    _list_method = "list_images_with_options"
    _create_method = "create_image_with_options"
    _list_labels_method = "list_image_labels_with_options"

    def list(
        self,
        labels: Union[Dict[str, Any], List[str]] = None,
        name: str = None,
        order: str = "DESC",
        page_number: int = 1,
        page_size: int = 50,
        parent_user_id: str = None,
        query: str = None,
        sort_by: str = None,
        user_id: str = None,
        verbose: bool = False,
        **kwargs,
    ) -> PaginatedResult:
        """List image resources."""
        workspace_id = kwargs.pop("workspace_id", None)
        if isinstance(labels, dict):
            labels = ",".join(["{}={}".format(k, v) for k, v in labels.items()])
        elif isinstance(labels, list):
            labels = ",".join([item for item in labels])

        req = ListImagesRequest(
            labels=labels,
            name=name,
            order=order,
            page_number=page_number,
            page_size=page_size,
            parent_user_id=parent_user_id,
            query=query,
            sort_by=sort_by,
            user_id=user_id,
            verbose=verbose,
            workspace_id=workspace_id,
        )

        return self._list(request=req)

    def _list(self, request) -> PaginatedResult:
        resp: ListImagesResponseBody = self._do_request(
            self._list_method, request=request
        )

        return self.make_paginated_result(resp)

    def list_labels(
        self,
        image_id: str = None,
        label_filter: Union[Dict[str, Any], List[str]] = None,
        label_keys: str = None,
        region: str = None,
        **kwargs,
    ) -> dict:
        workspace_id = kwargs.pop("workspace_id", None)
        if isinstance(label_filter, dict):
            label_filter = ",".join(
                ["{}={}".format(k, v) for k, v in label_filter.items()]
            )
        elif isinstance(label_filter, list):
            label_filter = ",".join([item for item in label_filter])

        request = ListImageLabelsRequest(
            image_id=image_id,
            label_filter=label_filter,
            label_keys=label_keys,
            region=region,
            workspace_id=workspace_id,
        )
        resp: ListImageLabelsResponseBody = self._do_request(
            method_=self._list_labels_method, request=request
        )
        return resp.to_map()["Labels"]

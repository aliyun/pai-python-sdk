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

import re
from typing import Any, Dict, List, Optional

from .api.image import SUPPORTED_IMAGE_FRAMEWORKS, ImageLabel
from .common.logging import get_logger
from .common.utils import make_list_resource_iterator, to_semantic_version
from .session import Session, get_default_session

logger = get_logger(__name__)


_NORMALIZED_FRAMEWORK_NAMES = {
    name.lower(): name for name in SUPPORTED_IMAGE_FRAMEWORKS
}

# Regex expression pattern for PAI Docker Image Tag.
_PAI_IMAGE_TAG_PATTERN_TRAINING = re.compile(
    r"([\w._-]+)-(gpu|cpu|mkl-cpu)-(py\d+)(?:-(cu\d+))?-([\S]+)"
)

_PAI_IMAGE_TAG_PATTERN_INFERENCE = re.compile(
    r"([\w._-]+)-(py\d+)(?:-(gpu|cpu|mkl-cpu))?(?:-(cu\d+))?-([\S]+)"
)

# Regex expression pattern for PAI Docker Image URI.
_PAI_IMAGE_URI_PATTERN = re.compile(r"([\S]+)/([\S]+)/([\S]+):([\S]+)")


class ImageInfo(object):
    """This class represents information for an image provided by PAI.

    Args:
        image_name (str): The name of the image.
        image_uri (str): The URI of the image.
        framework_name (str): The name of the framework installed in the image.
        framework_version (str, optional): The version of the framework (Default None).
        image_scope (str): The scope of the image, could be 'training', 'inference' or
            'develop'.
        accelerator_type (str, optional): The type of accelerator. Defaults to None.
        python_version (str, optional): The version of Python. Defaults to None.
    """

    def __repr__(self):
        return (
            "{}(framework_name={}: framework_version={}: image_scope={}: "
            "accelerator_type={}: py_version={})".format(
                self.__class__.__name__,
                self.framework_name,
                self.framework_version,
                self.image_scope,
                self.accelerator_type,
                self.python_version,
            )
        )

    def __init__(
        self,
        image_name: str,
        image_uri: str,
        framework_name: str,
        image_scope: str,
        framework_version: str = None,
        accelerator_type: Optional[str] = None,
        python_version: Optional[str] = None,
    ):
        self.image_name = image_name
        self.image_uri = image_uri
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.accelerator_type = accelerator_type
        self.python_version = python_version
        self.image_scope = image_scope


class ImageScope(object):
    """Class containing constants that indicate the purpose of an image."""

    TRAINING = "training"
    """Indicates the image is used for submitting a training job."""

    INFERENCE = "inference"
    """Indicates the image is used for creating a prediction service."""

    DEVELOP = "develop"
    """Indicates the image is used for running in DSW."""

    _SCOPE_IMAGE_LABEL_MAPPING = {
        TRAINING: ImageLabel.DLC_LABEL,
        INFERENCE: ImageLabel.EAS_LABEL,
        DEVELOP: ImageLabel.DSW_LABEL,
    }

    @classmethod
    def to_image_label(cls, scope: str):
        cls._validate(scope)

        return cls._SCOPE_IMAGE_LABEL_MAPPING.get(scope.lower())

    @classmethod
    def _validate(cls, scope: str):
        items = cls._SCOPE_IMAGE_LABEL_MAPPING.keys()
        if scope.lower() not in items:
            raise ValueError(f"Not supported image scope:  {scope}")


def _make_image_info(
    image_obj: Dict[str, Any],
    image_scope: str,
) -> Optional[ImageInfo]:
    """Make a ImageProperties object by parsing the image_uri."""

    labels = {lb["Key"]: lb["Value"] for lb in image_obj["Labels"]}
    image_uri = image_obj["ImageUri"]
    match = _PAI_IMAGE_URI_PATTERN.match(image_uri)
    if not match:
        # ignore if image uri is not recognized
        logger.debug(
            "Could not recognize the given image uri, ignore the image:"
            f" image_uri={image_uri}"
        )
        return
    host, namespace, repo_name, tag = match.groups()

    tag_match = _PAI_IMAGE_TAG_PATTERN_TRAINING.match(
        tag
    ) or _PAI_IMAGE_TAG_PATTERN_INFERENCE.match(tag)
    if not tag_match:
        # ignore if image tag is not recognized
        logger.debug(
            f"Could not recognize the given image tag, ignore the image:"
            f" image_uri={image_uri}."
        )
        fw_version, cpu_or_gpu, _, cuda_version, os_version = [None] * 5
    else:
        (
            fw_version,
            cpu_or_gpu,
            _,
            cuda_version,
            os_version,
        ) = tag_match.groups()

    # use image label as ground truth to set the image property, python version, etc.
    labels = labels or dict()
    if labels.get("system.chipType") == "GPU":
        cpu_or_gpu = "GPU"
    elif labels.get("system.chipType") == "CPU":
        cpu_or_gpu = "CPU"
    py_version = labels.get(ImageLabel.PYTHON_VERSION)

    # TODO: get the framework name from Image Label
    # extract framework name from image repo
    if repo_name.endswith("-inference"):
        framework_name = repo_name[:-10]
    elif repo_name.endswith("-training"):
        framework_name = repo_name[:-9]
    else:
        framework_name = repo_name

    framework_name = _NORMALIZED_FRAMEWORK_NAMES.get(framework_name, framework_name)
    image_name = image_obj["Name"]

    return ImageInfo(
        image_name=image_name,
        image_uri=image_uri,
        framework_name=framework_name,
        framework_version=fw_version,
        accelerator_type=cpu_or_gpu,
        python_version=py_version,
        image_scope=image_scope,
    )


def _list_images(
    labels: List[str],
    session: Session,
    name: Optional[str] = None,
    page_number=1,
    page_size=50,
):
    gen = make_list_resource_iterator(
        session.image_api.list,
        name=name,
        labels=labels,
        verbose=True,
        # set the workspace_id manually, prevent using the default workspace of the
        # session.
        workspace_id=0,
        order="DESC",
        sort_by="GmtCreateTime",
        page_number=page_number,
        page_size=page_size,
    )
    return gen


def retrieve(
    framework_name: str,
    framework_version: str,
    accelerator_type: str = "CPU",
    image_scope: Optional[str] = ImageScope.TRAINING,
    session: Optional[Session] = None,
) -> ImageInfo:
    """Get a container image URI that satisfies the specified requirements.

    Examples::

        # get a TensorFlow image with specific version for training.
        retrieve(framework_name="TensorFlow", framework_version="2.3")

        # get the latest PyTorch image that supports GPU for inference.
        retrieve(
            framework_name="PyTorch",
            framework_version="latest",
            accelerator_type="GPU",
            scope=ImageScope.INFERENCE,
        )

    Args:
        framework_name (str): The name of the framework. Possible values include
            TensorFlow, XGBoost, PyTorch, OneFlow, and others.
        framework_version (str): The version of the framework to use. Get the latest
            version supported in PAI by set the parameters as 'latest'.
        image_scope (str, optional): The scope of the image to use. Possible values
            include 'training', 'inference', and 'develop'.
        accelerator_type (str, optional): The name of the accelerator to use. Possible
            values including 'CPU', and 'GPU', (Default CPU).
        session (:class:`pai.session.Session`, optional): A session object to interact
            with the PAI Service. If not provided, a default session will be used.

    Returns:
        ImageInfo: A object contains information of the image that satisfy the
            requirements.

    Raises:
        RuntimeError: A RuntimeErrors is raised if the specific image is not found.
    """
    session = session or get_default_session()
    framework_name = framework_name.lower()
    supports_fw = [fw.lower() for fw in SUPPORTED_IMAGE_FRAMEWORKS]
    if framework_name not in supports_fw:
        raise ValueError(
            f"The framework ({framework_name}) is not supported by the"
            f" retrieve method: supported frameworks"
            f" {', '.join(SUPPORTED_IMAGE_FRAMEWORKS)}",
        )

    # label filter used to list official images of specific scope.
    labels = [ImageLabel.OFFICIAL_LABEL, ImageScope.to_image_label(image_scope)]

    # if accelerator_type is not specified, use CPU image by default.
    if not accelerator_type or accelerator_type.lower() == "cpu":
        labels.append(ImageLabel.DEVICE_TYPE_CPU)
    elif accelerator_type.lower() == "gpu":
        labels.append(ImageLabel.DEVICE_TYPE_GPU)
    else:
        raise ValueError(
            f"Given accelerator type ({accelerator_type}) is not supported, only"
            f" CPU and GPU is supported."
        )

    resp = _list_images(name=framework_name, labels=labels, session=session)

    # extract image properties, such as framework version, py_version, os_version, etc,
    # from image tag.
    candidates = []
    for image_item in resp:
        image_info = _make_image_info(
            image_obj=image_item,
            image_scope=image_scope,
        )
        if image_info.framework_name.lower() != framework_name.lower():
            continue
        candidates.append(image_info)

    if not candidates:
        raise RuntimeError(
            f"Not found any image that satisfy the requirements: framework_name="
            f"{framework_name}, accelerator={accelerator_type}"
        )

    if framework_version.lower() == "latest":
        # select the latest framework version.
        candidates = sorted(
            candidates,
            key=lambda img: to_semantic_version(img.framework_version),
            reverse=True,
        )
        return candidates[0]
    else:
        # find the image with the specific framework version.
        img = next(
            (img for img in candidates if img.framework_version == framework_version),
            None,
        )
        if not img:
            supported_versions = [img.framework_version for img in candidates]
            raise RuntimeError(
                f"Not found the specific framework: framework_name={framework_name}, "
                f"framework_version={framework_version}, supported versions for the"
                f" framework are {','.join(supported_versions)} "
            )
        else:
            return img


def list_images(
    framework_name: str,
    session: Optional[Session] = None,
    image_scope: Optional[str] = ImageScope.TRAINING,
) -> List[ImageInfo]:
    """List available images provided by PAI.

    Args:
        framework_name (str): The name of the framework. Possible values include
            TensorFlow, XGBoost, PyTorch, OneFlow, and others.
        image_scope (str, optional): The scope of the image to use. Possible values
            include 'training', 'inference', and 'develop'.
        session (:class:`pai.session.Session`): A session object used to interact with
            the PAI Service. If not provided, a default session is used.

    Returns:
        List[ImageInfo]: A list of image URIs.

    """
    session = session or get_default_session()
    if not framework_name or not framework_name.strip():
        framework_name = None
    else:
        framework_name = framework_name.strip().lower()

    labels = [
        ImageScope.to_image_label(image_scope),
        ImageLabel.OFFICIAL_LABEL,
    ]
    images = _list_images(labels=labels, session=session)

    images = [
        _make_image_info(
            item,
            image_scope=image_scope,
        )
        for item in images
    ]
    if framework_name:
        return [img for img in images if img.framework_name.lower() == framework_name]
    else:
        return images

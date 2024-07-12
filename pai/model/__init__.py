#  Copyright 2024 Alibaba, Inc. or its affiliates.
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


from ._model import (
    InferenceSpec,
    Model,
    ModelFormat,
    NfsStorageConfig,
    NodeStorageConfig,
    OssStorageConfig,
    RawStorageConfig,
    RegisteredModel,
    ResourceConfig,
    SharedMemoryConfig,
    StorageConfigBase,
    container_serving_spec,
)
from ._model_recipe import ModelRecipe, ModelRecipeType, ModelTrainingRecipe

__all__ = [
    "RegisteredModel",
    "Model",
    "ModelFormat",
    "InferenceSpec",
    "ResourceConfig",
    "container_serving_spec",
    "ModelTrainingRecipe",
    "ModelRecipe",
    "ModelRecipeType",
    "StorageConfigBase",
    "NfsStorageConfig",
    "NodeStorageConfig",
    "SharedMemoryConfig",
    "OssStorageConfig",
    "RawStorageConfig",
]

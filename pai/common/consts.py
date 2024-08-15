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
import enum
import os

# Default path for pai config file
DEFAULT_CONFIG_PATH = os.environ.get(
    "PAI_CONFIG_PATH", os.path.join(os.path.expanduser("~"), ".pai", "config.json")
)

# Default network type used to connect to PAI services
DEFAULT_NETWORK_TYPE = os.environ.get("PAI_NETWORK_TYPE", None)

# PAI VPC endpoint
PAI_VPC_ENDPOINT = "pai-vpc.{}.aliyuncs.com"


class Network(enum.Enum):
    VPC = "VPC"
    PUBLIC = "PUBLIC"

    @classmethod
    def from_string(cls, s: str) -> "Network":
        try:
            return cls[s.upper()]
        except KeyError:
            raise ValueError(
                "Invalid network type: %s, supported types are: %s"
                % (s, ", ".join(cls.__members__.keys()))
            )


class JobType(object):
    """PAI DLCJob/TrainingJob type."""

    TFJob = "TFJob"
    PyTorchJob = "PyTorchJob"
    XGBoostJob = "XGBoostJob"
    MPIJob = "MPIJob"

    SUPPORTED_JOB_TYPEs = [TFJob, PyTorchJob, XGBoostJob, MPIJob]
    _JOB_TYPE_MAPPING = {job_type.lower(): job_type for job_type in SUPPORTED_JOB_TYPEs}

    @classmethod
    def normalize(cls, job_type):
        """Normalize given job_type.

        If given job_type is unknown, just returns the original data.
        """
        return cls._JOB_TYPE_MAPPING.get(job_type.lower(), job_type)


class ResourceAccessibility(object):
    PRIVATE = "PRIVATE"
    PUBLIC = "PUBLIC"


class DataSourceType(object):
    NAS = "NAS"
    OSS = "OSS"


class FileProperty(object):
    FILE = "FILE"
    DIRECTORY = "DIRECTORY"
    TABULAR = "TABULAR"


class DataType(object):
    COMMON = "COMMON"
    PIC = "PIC"
    TEXT = "TEXT"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"


class DatasetSourceType(object):
    USER = "USER"
    ITAG = "ITAG"
    PAI_PUBLIC_DATASET = "PAI_PUBLIC_DATASET"


class ModelFormat(object):
    SavedModel = "SavedModel"
    FrozenPb = "FrozenPb"
    KerasH5 = "KerasH5"
    CaffePrototxt = "Caffe"
    ONNX = "ONNX"
    BladeModel = "BladeModel"
    PMML = "PMML"
    TorchScript = "TorchScript"
    TFLite = "TFLite"


class FrameworkTypes(object):
    PyTorch = "PyTorch"
    TFLite = "TFLite"
    Keras = "Keras"
    Caffe = "Caffe"
    Blade = "Blade"
    Alink = "Alink"
    TensorFlow = "TensorFlow"


INSTANCE_TYPE_LOCAL = "local"
INSTANCE_TYPE_LOCAL_GPU = "local_gpu"


class FileSystemInputScheme(object):
    # Standard/Extreme/CPFS 1.0 file system type
    NAS = "nas"
    # CPFS2.0 file system type
    CPFS = "cpfs"
    # BMCPFS file system type
    BMCPFS = "bmcpfs"


class DefaultChannelName(object):
    MODEL = "model"
    CHECKPOINT = "checkpoints"
    TENSORBOARD = "tensorboard"


class StoragePathCategory(object):
    """PAI builtin remote storage path."""

    # For inference
    InferenceSrc = "inference_src"

    # For evaluation
    EvaluationSrc = "evaluation_src"

    # For training job
    TrainingSrc = "training_src"
    TrainingJob = "training_job"
    TrainData = "train_data"
    ModelData = "model_data"

    # For processing job
    ProcessingJob = "processing_job"
    ProcessingSrc = "processing_src"
    InputData = "input_data"

# Feature flag indicate whether user use AIWorkspace Integrated PAI DLC or legacy PAI DLC.
PAI_DLC_INTEGRATED_WITH_WORKSPACE_FEATURE = "PaiDLC:IntegrateWithWorkspace"

# Default Dataset mount path
DEFAULT_DATASET_MOUNT_PATH = "/mnt/data/"

# Default CodeSource mount path
DEFAULT_CODE_SOURCE_MOUNT_PATH = "/root/code/"


# Inner RegionId list
INNER_REGION_IDS = ["center"]


class JobType(object):
    """PAI DLC Job type."""

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


class WorkerType(object):
    """Supported worker types in PAI-DLC."""

    PS = "PS"
    WORKER = "Worker"
    MASTER = "Master"
    EVALUATOR = "Evaluator"
    CHIEF = "Chief"


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


class PAIServiceName(object):
    PAI_DLC = "PAI_DLC"
    PAI_EAS = "PAI_EAS"
    AIWORKSPACE = "AIWORKSPACE"
    PAIFLOW = "PAIFLOW"
    TRAINING_SERVICE = "TRAINING"


class PAIRestResourceTypes(object):
    """Resource types provided by PAI REST API."""

    Dataset = "Dataset"
    DlcJob = "DlcJob"
    CodeSource = "CodeSource"
    Image = "Image"
    EasService = "EasService"
    Model = "Model"
    Workspace = "Workspace"


class PagingOrder(object):
    DESCENT = "desc"
    ASCENT = "asc"


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
    ALinkModel = "AlinkModel"


class FrameworkTypes(object):
    PyTorch = "PyTorch"
    TFLite = "TFLite"
    Keras = "Keras"
    Caffe = "Caffe"
    Blade = "Blade"
    Alink = "Alink"
    TensorFlow = "TensorFlow"


DEFAULT_WORKER_ECS_SPEC = "ecs.c6.large"

DEFAULT_PAGE_SIZE = 10
DEFAULT_PAGE_NUMBER = 1

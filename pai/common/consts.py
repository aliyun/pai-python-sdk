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

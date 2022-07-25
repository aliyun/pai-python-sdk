# Feature flag indicate whether user use AIWorkspace Integrated PAI DLC or legacy PAI DLC.
from enum import Enum

PAI_DLC_INTEGRATED_WITH_WORKSPACE_FEATURE = "PaiDLC:IntegrateWithWorkspace"

DEFAULT_DATASET_MOUNT_PATH = "/mnt/data/"
DEFAULT_CODE_SOURCE_MOUNT_PATH = "/root/code/"


class ResourceAccessibility(object):
    PRIVATE = "PRIVATE"
    PUBLIC = "PUBLIC"


class DataSourceType(object):
    NAS = "nas"
    OSS = "oss"


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

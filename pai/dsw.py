import os
import posixpath
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .common.logging import get_logger
from .common.oss_utils import OssUriObj, is_oss_uri
from .common.utils import is_dataset_id
from .libs.alibabacloud_pai_dsw20220101.models import (
    GetInstanceResponse,
    GetInstanceResponseBody,
    UpdateInstanceRequest,
    UpdateInstanceRequestDatasets,
)
from .session import Session, get_default_session

logger = get_logger()


class OptionType(str, Enum):
    """
    The type of options for mounting data sources in DSW (Data Science Workshop).

    This enum defines different mounting modes for OSS (Object Storage Service)
    and custom datasets in DSW. Each mode has specific characteristics and use cases:

    Attributes:
        FastReadWrite: Allows fast read and write operations. Suitable for training
            data and models, but may have data consistency issues with concurrent
            read/write operations. Not recommended for work directories.

        IncrementalReadWrite: Ensures data consistency for incremental writes,
            but may have consistency issues when overwriting existing data.
            Slightly slower read speed. Suitable for saving training model weights.

        ConsistentReadWrite: Maintains data consistency during concurrent read/write
            operations. Suitable for scenarios requiring high data consistency
            but can tolerate slower read speeds. Ideal for saving code projects.

        ReadOnly: Allows only read operations, no writing permitted.
            Suitable for mounting public datasets.

    The choice of option type affects the underlying Jindo configuration for
    mounting OSS data in DSW. Users can select the appropriate mode based on
    their specific use case and performance requirements.

    """

    FastReadWrite = "FastReadWrite"
    IncrementalReadWrite = "IncrementalReadWrite"
    ConsistentReadWrite = "ConsistentReadWrite"
    ReadOnly = "ReadOnly"


def _default_instance() -> "DswInstance":
    """
    Get the default DSW Instance.

    Returns:
        DswInstance: The default DSW Instance.
    """
    instance_id = os.getenv("DSW_INSTANCE_ID")
    if not instance_id:
        raise RuntimeError(
            "Environment variable 'DSW_INSTANCE_ID' is not set, please check if you are running in DSW environment"
        )
    return DswInstance(instance_id)


def mount(
    source: str,
    mount_point: str = None,
    options: Optional[Dict[str, Any]] = None,
    option_type: Optional[OptionType] = None,
) -> str:
    """
    Dynamic mount a data source to the DSW Instance.

    Args:
        source (str): The source to be mounted, can be a dataset id or an OSS uri.
        mount_point (str): Target mount point in the instance, if not specified, the
            mount point be generate with given source under the default mount point.
        options (dict): Options that apply to when mount a data source, can not be
            specified with option_type.
        option_type(str): Preset data source mount options, can not be specified with
            options.

    Returns:
        str: The mount point of the data source.

    Examples:
        >>> mount_point = mount("oss://my-bucket/my-object/path/to/dir")
        >>> mount_point = mount("oss://my-bucket/my-object/path/to/dir", mount_point="/my-target", option_type=OptionType.FastReadWrite)
        >>> mount_point = mount("oss://my-bucket/my-object/path/to/dir", mount_point="/my-target", options={
            "fs.oss.download.thread.concurrency": "8", # CPU core count * 2
            "fs.oss.upload.thread.concurrency": "8", # CPU core count * 2
            # jindo args, refer to https://help.aliyun.com/zh/emr/emr-on-ecs/user-guide/user-guide-of-jindofuse
            "fs.jindo.args": "-oattr_timeout=3 -oentry_timeout=0 -onegative_timeout=0 -oauto_cache -ono_symlink" # jindo args
        })


    """
    instance = _default_instance()
    return instance.mount(
        source,
        mount_point,
        options=options,
        option_type=option_type,
    )


def list_dataset_configs() -> List[Dict[str, Any]]:
    """
    List all the datasets available in the DSW Instance.

    Returns:
        list: A list of dataset details.
    """
    instance = _default_instance()

    return [d.to_map() for d in instance._get_instance_info().datasets]


def default_dynamic_mount_point():
    """Get the default dynamic mount point of the DSW Instance.

    Returns:
        str: The default dynamic mount point of the DSW Instance.
    """
    instance = _default_instance()
    return instance.default_dynamic_mount_point()


def get_dynamic_mount_config() -> Dict[str, Any]:
    """
    Get the dynamic mount config of the DSW Instance.

    Returns:
        dict: The dynamic mount config of the DSW Instance.
    """
    instance = _default_instance()
    return instance.get_dynamic_mount_config()


class DswInstance:
    """A object representing a DSW notebook instance"""

    def __init__(self, instance_id: str):
        self.instance_id = instance_id
        self._instance_info: GetInstanceResponseBody = self._get_instance_info()

    def _get_instance_info(self):
        session = get_default_session()
        resp: GetInstanceResponse = session._acs_dsw_client.get_instance(
            self.instance_id
        )
        return resp.body

    def get_dynamic_mount_config(self):
        """Get the dynamic mount config of the DSW Instance.

        Returns:
            dict: The dynamic mount config of the DSW Instance.
        """
        return self._instance_info.dynamic_mount.to_map()

    def default_dynamic_mount_point(self) -> Optional[str]:
        """Get the default dynamic mount point of the DSW Instance.

        Returns:
            str: The default dynamic mount point of the DSW Instance.
        """
        if (
            not self._instance_info.dynamic_mount.enable
            or not self._instance_info.dynamic_mount.mount_points
        ):
            return
        return self._instance_info.dynamic_mount.mount_points[0].root_path

    def mount(
        self,
        source: str,
        mount_point: str = None,
        options: Union[str] = None,
        option_type: Union[OptionType] = None,
    ):
        """
        Dynamic mount a data source to the DSW Instance.

        Args:
            source (str): The source to be mounted, can be a dataset id or an OSS uri.
            mount_point (str): Target mount point in the instance, if not specified, the
                mount point be generate with given source under the default mount point.
            options (str): Options that apply to when mount a data source, can not be
                specified with option_type.
            option_type(str): Preset data source mount options, can not be specified with
                options.
        """
        if options and option_type:
            raise ValueError(
                "options and option_type cannot be specified at the same time"
            )
        if not self._instance_info.dynamic_mount.enable:
            raise RuntimeError(
                "Dynamic mount is not enabled for the DSW instance: {}".format(
                    self.instance_id
                )
            )
        if not self._instance_info.dynamic_mount.mount_points:
            raise RuntimeError(
                "No dynamic mount points found for the DSW instance: {}".format(
                    self.instance_id
                )
            )

        sess = get_default_session()
        default_root_path = self.default_dynamic_mount_point()

        if is_oss_uri(source):
            obj = OssUriObj(source)
            if not obj.endpoint:
                obj.endpoint = sess.oss_endpoint or sess._get_default_oss_endpoint()
            # ensure mount source OSS uri is a directory
            _, dir_path, _ = obj.parse_object_key()
            uri = f"oss://{obj.bucket_name}.{obj.endpoint}{dir_path}"
            dataset_id = None
        else:
            dataset_id = source
            uri = None

        if not is_oss_uri(source) and not is_dataset_id(source):
            raise ValueError("Source must be oss uri or dataset id")

        if not mount_point:
            if is_oss_uri(source):
                obj = OssUriObj(source)
                mount_point = f"{obj.bucket_name}/{obj.object_key}"
            else:
                mount_point = source
        if not posixpath.isabs(mount_point):
            mount_point = posixpath.join(default_root_path, mount_point)

        resp: GetInstanceResponse = sess._acs_dsw_client.get_instance(self.instance_id)
        datasets = [
            UpdateInstanceRequestDatasets().from_map(ds.to_map())
            for ds in resp.body.datasets
        ]
        datasets.append(
            UpdateInstanceRequestDatasets(
                dataset_id=dataset_id,
                dynamic=True,
                mount_path=mount_point,
                option_type=option_type,
                options=options,
                uri=uri,
            )
        )
        request = UpdateInstanceRequest(
            datasets=datasets,
        )
        sess._acs_dsw_client.update_instance(
            instance_id=self.instance_id, request=request
        )
        return mount_point

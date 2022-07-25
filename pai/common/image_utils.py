from pai.common.consts import INNER_REGION_IDS

_PAIFLOW_EXECUTOR_IMAGE_URI_PATTERN = (
    "registry.{region_id}.aliyuncs.com/{namespace}/{executor_type}:{version_tag}"
)

_PAIFLOW_INNER_EXECUTOR_IMAGE_URI_PATTERN = (
    "reg.docker.alibaba-inc.com/{namespace}/{executor_type}:{version_tag}"
)

_DEFAULT_PAIFLOW_EXECUTOR_NAMESPACE = "paiflow-core"
_INNER_PAIFLOW_EXECUTOR_NAMESPACE = "paiflow-executor"


def retrieve_executor_image(region_id, version, executor_type):
    """Retrieve a specific executor image.

    Args:
        region_id: The region id
        version: Version of the executor image.
        executor_type: Executor type.

    Returns:
        str: Image uri of the specific executor image.
    """
    # TODO(LiangQuan): Support group-inner Environment executor image uri

    if region_id not in INNER_REGION_IDS:
        return _PAIFLOW_EXECUTOR_IMAGE_URI_PATTERN.format(
            region_id=region_id,
            namespace=_DEFAULT_PAIFLOW_EXECUTOR_NAMESPACE,
            version_tag=version,
            executor_type=executor_type,
        )
    else:
        return _PAIFLOW_INNER_EXECUTOR_IMAGE_URI_PATTERN.format(
            executor_type=executor_type,
            namespace=_INNER_PAIFLOW_EXECUTOR_NAMESPACE,
            version_tag=version,
        )

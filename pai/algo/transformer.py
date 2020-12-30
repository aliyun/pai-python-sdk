from pai.common import ProviderAlibabaPAI
from pai.algo.base import MaxComputeTransformer
from pai.common.utils import gen_temp_table


class OfflineModelTransformer(MaxComputeTransformer):
    """XFlow based algorithm, transform data set from MaxCompute table use offlinemodel"""

    _enable_spare_input = True

    _identifier_default = "Prediction_1"
    _version_default = "v1"
    _provider_default = ProviderAlibabaPAI

    def __init__(self, model, **kwargs):
        """OfflineModelTransformer constructor.

        Args:
            model (str): OfflineModel data, offlinemodel resource url.
                Examples:
                    odps://project_name/offlinemodels/offline_model_name.
        """
        super(OfflineModelTransformer, self).__init__(model=model, **kwargs)

    def _compile_args(self, *inputs, **kwargs):
        args = super(OfflineModelTransformer, self)._compile_args(*inputs, **kwargs)
        args["inputTable"] = inputs[0]
        args["model"] = kwargs.get("model")
        args["outputTableName"] = kwargs.get("output_table") or gen_temp_table()
        args["outputTablePartition"] = kwargs.get("partitions")
        feature_cols = kwargs.get("feature_cols")
        if isinstance(feature_cols, (list, tuple)):
            feature_cols = ",".join(feature_cols)
        args["featureColNames"] = feature_cols
        append_cols = kwargs.get("append_cols")
        if isinstance(feature_cols, (list, tuple)):
            append_cols = ",".join(append_cols)
        args["appendColNames"] = append_cols

        args["resultColName"] = kwargs.get("result_col")
        args["lifecycle"] = kwargs.get("table_lifecycle")

        return args

    def transform(
        self,
        input_data,
        wait=True,
        job_name=None,
        feature_cols=None,
        label_col=None,
        result_col=None,
        score_col=None,
        detail_col=None,
        append_cols=None,
        output_table=None,
        output_partition=None,
        lifecycle=None,
        **kwargs
    ):
        return super(OfflineModelTransformer, self).transform(
            input_data,
            wait=wait,
            job_name=job_name,
            feature_cols=feature_cols,
            label_col=label_col,
            result_col=result_col,
            append_cols=append_cols,
            output_table=output_table,
            output_partition=output_partition,
            **kwargs
        )


class ModelTransferToOSS(MaxComputeTransformer):
    """Util component used for transfer offlinemodel from MaxCompute to user-owned OSS bucket.

    XFlow algorithm task produce offlinemodel store in MaxCompute. By transfer the offlinemodel to
     OSS service (component also has ability to convert the model format ), trained model could be
     use to deploy to Elastic Algorithm Service (EAS), or other utilities.
    """

    _identifier_default = "generalmodeltransfer2oss"
    _provider_default = ProviderAlibabaPAI
    _version_default = "v1"

    def __init__(
        self,
        oss_bucket,
        oss_endpoint,
        oss_path,
        rolearn,
        format="pmml",
        overwrite=True,
        **kwargs
    ):
        """

        Args:
            oss_bucket (str): Transfer target oss bucket name.
            oss_endpoint (str): Domain name that the service can use to access OSS.
            model_format (str): Convert to specific Model format  while transfer to target OSS,
                optional 'original', 'pmml', etc.
            rolearn (str): Alibaba Cloud Role ARN, used for access OSS service.
        """
        super(ModelTransferToOSS, self).__init__(
            oss_bucket=oss_bucket,
            oss_endpoint=oss_endpoint,
            oss_path=oss_path,
            rolearn=rolearn,
            overwrite=overwrite,
            format=format,
            **kwargs
        )

    def _compile_args(self, *inputs, **kwargs):
        args = super(ModelTransferToOSS, self)._compile_args(*inputs, **kwargs)

        assert len(inputs) > 0
        args["inputTable"] = inputs[0]
        args["arn"] = kwargs["rolearn"]
        args["format"] = kwargs["format"]
        args["overwrite"] = kwargs["overwrite"]

        oss_path_dir = kwargs["oss_path"]
        if not oss_path_dir.startswith("/"):
            oss_path_dir = "/" + oss_path_dir
        if not oss_path_dir.endswith("/"):
            oss_path_dir = oss_path_dir + "/"
        oss_path = "oss://{0}.{1}{2}".format(
            kwargs["oss_bucket"], kwargs["oss_endpoint"], oss_path_dir
        )
        args["ossPath"] = oss_path

        return args

    def transform(self, input_model, wait=True, job_name=None, **kwargs):
        """Transfer input offlinemodel to sepcific path of OSS bucket.

        Args:
            input_model (str): OfflineModel ready to transfer.
            path (str): Transfer target OSS path, should startswith '/' and endswith '/'.
            wait: Should transform job wait_for_completion until complete.
            job_name: Transform job name.
            **kwargs:
        Returns:
            _TransformJob: Job instance used as controller and get the outputs of transformer.
        """
        return super(ModelTransferToOSS, self).transform(
            input_model, job_name=job_name, wait=wait, **kwargs
        )


class FeatureNormalize(MaxComputeTransformer):
    """Normalize input dataset"""

    _identifier_default = "normalize_1"
    _version_default = "v1"
    _provider_default = ProviderAlibabaPAI

    def __init__(self, **kwargs):
        super(FeatureNormalize, self).__init__(**kwargs)

    def _compile_args(self, *inputs, **kwargs):
        args = super(FeatureNormalize, self)._compile_args(*inputs, **kwargs)
        args["inputTable"] = kwargs.get("input_table")
        args["inputParaTable"] = kwargs.get("input_para_table")
        args["outputTableName"] = kwargs.get("output_table")
        args["outputParaTableName"] = kwargs.get("output_para_table")
        args["selectedColNames"] = (
            ",".join(kwargs.get("selected_cols"))
            if isinstance(kwargs.get("selected_cols"), list)
            else kwargs.get("selected_cols")
        )
        args["keepOriginal"] = kwargs.get("keep_original")

    def transform(
        self,
        input_table,
        output_table,
        output_para_table,
        input_para_table=None,
        output_partition=None,
        selected_cols=None,
        keep_original=False,
        **kwargs
    ):
        super(FeatureNormalize, self).transform(
            input_table=input_table,
            output_table=output_table,
            output_para_table=output_para_table,
            output_partition=output_partition,
            selected_cols=selected_cols,
            keep_original=keep_original,
            **kwargs
        )


class MaxComputeDataSource(MaxComputeTransformer):
    """Transform plain odps table/partition info to ODPS Table Artifact

    :Example:

    >> tf = Transformer()
    >> job = tf.transform(table_name='pai_online_project.wumai_data', wait_for_completion=True,
     job_name='data_source_example_job')
    >> job.get_status()

    """

    _identifier_default = "data_source"
    _version_default = "v1"
    _provider_default = ProviderAlibabaPAI

    def __init__(self, **kwargs):
        super(MaxComputeDataSource, self).__init__(**kwargs)

    def _compile_args(self, *inputs, **kwargs):
        args = super(MaxComputeDataSource, self)._compile_args(*inputs, **kwargs)
        assert len(inputs) > 0
        args["inputTableName"] = inputs[0]
        args["inputTablePartitions"] = kwargs.pop("partition")
        return args

    def transform(self, table_name, partition=None, wait=True, job_name=None, **kwargs):
        """Transform odps table to ODPS table artifact.

        Args:
            table_name (str): Input MaxCompute table name.
            partition (str): MaxCompute table partition identifier, for example,
                             "seller=19283/dt=20200304", Default None.
            wait (bool):    Whether transform method wait_for_completion until the run job finished.
            job_name (str): Name of invoke transform job. If not specified, the estimator
                            generates a default job name based on the identifier and current
                            timestamp.
            **kwargs: base class keyword argument values.
        Returns:
            _TransformJob: Job instance used as controller and get the outputs of transformer.
        """
        return super(MaxComputeDataSource, self).transform(
            table_name, partition=partition, wait=wait, job_name=job_name, **kwargs
        )

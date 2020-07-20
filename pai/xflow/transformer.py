from pai import ProviderAlibabaPAI
from pai.xflow.base import XFlowTransformer
from pai.utils import gen_temp_table_name


class OfflineModelTransformer(XFlowTransformer):
    _enable_spare_input = True

    _identifier_default = "prediction-xflow-maxCompute"
    _version_default = "v1"
    _provider_default = ProviderAlibabaPAI

    def __init__(self, session, model, table_lifecycle=None, **kwargs):
        """

        Args:
            session: PAI Session instance.
            model (str): OfflineModel data, could be offlinemodel resource url, ODPS OfflineModel object,
                   or
            **kwargs:
        """
        super(OfflineModelTransformer, self).__init__(session=session,
                                                      model=model,
                                                      table_lifecycle=table_lifecycle,
                                                      **kwargs)

    def _compile_args(self, *inputs, **kwargs):
        args = super(OfflineModelTransformer, self)._compile_args(*inputs, **kwargs)
        assert len(inputs) > 0
        args["inputDataSetArtifact"] = inputs[0]
        args["inputModelArtifact"] = kwargs.get("model")
        args["outputTableName"] = kwargs.get("output_table") or gen_temp_table_name()
        args['outputPartition'] = kwargs.get("partitions")
        feature_cols = kwargs.get("feature_cols")
        if isinstance(feature_cols, (list, tuple)):
            feature_cols = ','.join(feature_cols)
        args["featureColNames"] = feature_cols
        args["appendColNames"] = kwargs.get("append_cols")
        args["resultColName"] = kwargs.get("result_col")

        return args

    def transform(self, input_data, wait=True, job_name=None, feature_cols=None, label_col=None,
                  result_col=None, score_col=None, detail_col=None, append_cols=None,
                  output_table=None, output_partition=None, **kwargs):
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


class ModelTransferToOSS(XFlowTransformer):
    """Util component used for transfer offlinemodel from MaxCompute to user-owned OSS bucket.

    XFlow algorithm task produce offlinemodel store in MaxCompute. By transfer the offlinemodel to
     OSS service (component also has ability to convert the model format ), trained model could be
     use to deploy to Elastic Algorithm Service (EAS), or other utilities.
    """

    _identifier_default = "modeltransfer2oss-xflow-maxCompute"
    _provider_default = ProviderAlibabaPAI
    _version_default = "v1"

    def __init__(self, session, bucket, endpoint, rolearn, model_format="pmml",
                 overwrite=True, **kwargs):
        """

        Args:
            session (~pai.session.Session): PAI session object.
            bucket (str): Transfer target oss bucket name.
            endpoint (str): Domain name that the service can use to access OSS.
            model_format (str): Convert to specific Model format  while transfer to target OSS,
                optional 'original', 'pmml', etc.
            rolearn (str): Alibaba Cloud Role ARN, used for access OSS service.
        """
        super(ModelTransferToOSS, self).__init__(
            session=session,
            bucket=bucket,
            endpoint=endpoint,
            rolearn=rolearn,
            model_format=model_format,
            overwrite=overwrite,
            **kwargs
        )

    def _compile_args(self, *inputs, **kwargs):
        args = super(ModelTransferToOSS, self)._compile_args(*inputs, **kwargs)

        assert len(inputs) > 0
        args["inputArtifact"] = inputs[0]
        args["rolearn"] = kwargs["rolearn"]
        args["host"] = kwargs["endpoint"]
        args["format"] = kwargs["model_format"]
        args["bucket"] = kwargs["bucket"]

        oss_path = kwargs["path"]
        if not oss_path.startswith("/"):
            oss_path = '/' + oss_path
        if not oss_path.endswith("/"):
            oss_path = oss_path + '/'

        args["key"] = oss_path

        return args

    def transform(self, input_model, path=None, wait=True, job_name=None, **kwargs):
        """Transfer input offlinemodel to sepcific path of OSS bucket.

        Args:
            input_model (str): OfflineModel ready to transfer.
            path (str): Transfer target OSS path, should startswith '/' and endswith '/'.
            wait: Should transform job wait until complete.
            job_name: Transform job name.
            **kwargs:
        Returns:
            _TransformJob: Job instance used as controller and get the outputs of transformer.
        """
        return super(ModelTransferToOSS, self).transform(
            input_model,
            job_name=job_name,
            wait=wait,
            path=path,
            **kwargs
        )


class FeatureNormalize(XFlowTransformer):
    pass


class MaxComputeDataSource(XFlowTransformer):
    """ Transform plain odps table/partition info to ODPS Table Artifact

    :Example:

    >> tf = Transformer(session=session)
    >> job = tf.transform(table_name='pai_online_project.wumai_data', wait=True,
     job_name='data_source_example_job')
    >> job.get_status()

    """

    _identifier_default = "dataSource-xflow-maxCompute"
    _version_default = "v1"
    _provider_default = ProviderAlibabaPAI

    def __init__(self, session, **kwargs):
        super(MaxComputeDataSource, self).__init__(session=session, **kwargs)

    def _compile_args(self, *inputs, **kwargs):
        args = super(MaxComputeDataSource, self)._compile_args(*inputs, **kwargs)
        assert len(inputs) > 0
        args["tableName"] = inputs[0]
        args["partition"] = kwargs.pop("partition")
        return args

    def transform(self, table_name, partition=None, wait=True, job_name=None, **kwargs):
        """Transform odps table to ODPS table artifact.

        Args:
            table_name (str): Input MaxCompute table name.
            partition (str): MaxCompute table partition identifier, for example,
                             "seller=19283/dt=20200304", Default None.
            wait (bool):    Whether transform method wait until the run job finished.
            job_name (str): Name of invoke transform job. If not specified, the estimator
                            generates a default job name based on the identifier and current
                            timestamp.
            **kwargs: base class keyword argument values.
        Returns:
            _TransformJob: Job instance used as controller and get the outputs of transformer.
        """
        return super(MaxComputeDataSource, self).transform(
            table_name,
            partition=partition,
            wait=wait,
            job_name=job_name,
            **kwargs
        )

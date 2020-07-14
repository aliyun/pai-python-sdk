from pai import ProviderAlibabaPAI
from pai.xflow.base import XFlowTransformer


class XFlowOfflineModelTransformer(XFlowTransformer):
    _identifier_default = "prediction-xflow-ODPS"
    _version_default = "v1"
    _provider_default = ProviderAlibabaPAI

    def __init__(self, session, model, **kwargs):
        super(XFlowOfflineModelTransformer, self).__init__(session=session, model=model, **kwargs)
        self.model = model

    def compare_args(self, **kwargs):
        pass

    def transform(self, input_data, wait=True, job_name=None, ):
        return super(XFlowOfflineModelTransformer, self).transform()


class FeatureNormalize(XFlowTransformer):
    pass


class ODPSDataSource(XFlowTransformer):
    """
    Transform plain odps table/partition info to ODPS Table Artifact
    """

    _identifier_default = "odps-data-source"
    _version_default = "v1"
    _provider_default = ProviderAlibabaPAI

    def __init__(self, session, **kwargs):
        super(ODPSDataSource, self).__init__(session=session, **kwargs)

    def compile_args(self, *inputs, **kwargs):
        args = super(ODPSDataSource, self).compile_args(*inputs, **kwargs)
        assert len(inputs) > 0
        args["tableName"] = inputs[0]
        args["partition"] = kwargs.pop("partition")
        return args

    def transform(self, table_name, partition=None, wait=True, job_name=None, **kwargs):
        """Transform odps table to ODPS table artifact.

        :Example:

        >> tf = Transformer(session=session)
        >> job = tf.transform(table_name='pai_online_project.wumai_data', wait=True, job_name='data_source_example_job')
        >> job.get_status()

        Args:
            table_name (str): Input MaxCompute table name.
            partition (str): MaxCompute table partition identifier, for example,
                             "seller=19283/dt=20200304", Default None.
            wait (bool):    Whether transform method wait until the run job finished.
            job_name (str): Name of invoke transform job. If not specified, the estimator
                            generates a default job name based on the identifier and current
                            timestamp.
            **kwargs: base class keyword argument values.
        """
        return super(ODPSDataSource, self).transform(
            table_name,
            partition=partition,
            wait=wait,
            job_name=job_name,
            **kwargs
        )

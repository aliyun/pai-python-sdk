from __future__ import absolute_import
from pai.common import ProviderAlibabaPAI
from .estimator import XFlowModelTransferEstimator


class LogisticRegression(XFlowModelTransferEstimator):
    _identifier_default = "logisticregression-binary-xflow-ODPS"

    _version_default = "v1"

    _provider_default = ProviderAlibabaPAI

    def __init__(self, session, regularized_level=1.0, regularized_type="l1", max_iter=100, epsilon=1e-6):
        super(LogisticRegression, self).__init__(session=session, regularized_level=regularized_level,
                                                 regularized_type=regularized_type, max_iter=max_iter,
                                                 epsilon=epsilon, pmml_config=None)

    def _compile_args(self, **kwargs):
        args = super(LogisticRegression, self)._compile_args(**kwargs)
        args["inputArtifact"] = kwargs.get("input_data")

        # args["regularizedType"] = kwargs.get("regularized_type")
        args["regularizedLevel"] = kwargs.get("regularized_level")
        args["maxIter"] = kwargs.get("max_iter")
        args["epsilon"] = kwargs.get("epsilon")
        args["goodValue"] = kwargs.get("good_value")
        args["featureColNames"] = kwargs.get("feature_cols")
        args["labelColName"] = kwargs.get("label_col")
        args["modelName"] = kwargs.get("modelName")

        enable_sparse = kwargs.get("enable_sparse")
        if enable_sparse:
            args["enableSparse"] = bool(enable_sparse)
            sparse_delimiter = kwargs["sparse_delimiter"]
            item_delimiter, kv_delimiter = sparse_delimiter
            args["itemDelimiter"] = item_delimiter
            args["kvDelimiter"] = kv_delimiter
        return args

    def fit(self, input_data, job_name=None, wait=False, feature_cols=None, label_col=None,
            model_name=None, sparse=None, sparse_delimiter=None, good_value=None):
        """

        Args:
            input_data: ODPS Table object or odps resource url or odps table name
            feature_cols:
            label_col:
            model_name:
            sparse:
            sparse_delimiter:
            good_value:
            generate_pmml:
            wait:
            **kwargs:

        Returns:

        """
        return super(LogisticRegression, self).fit(input_data, job_name=job_name, model_name=model_name,
                                                   feature_cols=feature_cols,
                                                   label_col=label_col, sparse=sparse,
                                                   sparse_delimiter=sparse_delimiter,
                                                   good_value=good_value)

    def create_model(self):
        pass


class RandomForestClassifier(XFlowModelTransferEstimator):
    _identifier_default = "random-forests-xflow-ODPS"

    _provider_default = ProviderAlibabaPAI

    _version_default = "1.0.0"

    def __init__(self, session, tree_num, random_col_num, max_tree_deep, min_num_obj=None, min_num_per=None,
                 max_record_size=None, xflow_project=None):
        super(RandomForestClassifier, self).__init__(session=session, tree_num=tree_num, random_col_num=random_col_num,
                                                     max_tree_deep=max_tree_deep, min_num_obj=min_num_obj,
                                                     min_num_per=min_num_per, max_record_size=max_record_size,
                                                     xflow_project=xflow_project)

    def fit(self, input_data, model_name, label_col, excluded_cols, tree_num=None, wait=True,
            feature_cols=None, algo_types=None, random_col_num=None):
        super(RandomForestClassifier, self).fit(wait=wait, input_data=input_data, model_name=model_name,
                                                tree_num=tree_num, excluded_cols=excluded_cols,
                                                feature_cols=feature_cols, algo_types=algo_types,
                                                random_col_num=random_col_num)
        return

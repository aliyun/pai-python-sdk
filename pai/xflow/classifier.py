from __future__ import absolute_import

from pai.common import ProviderAlibabaPAI
from pai.xflow.base import XFlowEstimator


class LogisticRegression(XFlowEstimator):
    _enable_sparse = True
    _pmml_model = True

    _identifier_default = "logisticregression-binary-xflow-maxCompute"

    _version_default = "v1"

    _provider_default = ProviderAlibabaPAI

    def __init__(self, regularized_level=1.0, regularized_type="l1", max_iter=100,
                 epsilon=1e-6, **kwargs):
        super(LogisticRegression, self).__init__(
            regularized_level=regularized_level,
            regularized_type=regularized_type,
            max_iter=max_iter,
            epsilon=epsilon, **kwargs)

    def _compile_args(self, *inputs, **kwargs):
        args = super(LogisticRegression, self)._compile_args(*inputs, **kwargs)
        assert len(inputs) > 0

        args["inputArtifact"] = inputs[0]

        args["regularizedType"] = kwargs.get("regularized_type")
        args["regularizedLevel"] = kwargs.get("regularized_level")
        args["maxIter"] = kwargs.get("max_iter")
        args["epsilon"] = kwargs.get("epsilon")
        args["goodValue"] = kwargs.get("good_value")

        args["labelColName"] = kwargs.get("label_col")
        args["modelName"] = kwargs.get("model_name")
        feature_cols = kwargs.get("feature_cols")
        if feature_cols is not None:
            if isinstance(feature_cols, list):
                args["featureColNames"] = ",".join(kwargs.get("feature_cols"))
            else:
                args["featureColNames"] = feature_cols

        return args

    def fit(self, input_data, model_name, label_col, good_value, job_name=None, wait=True,
            show_outputs=True, feature_cols=None, enable_sparse=None, sparse_delimiter=None):
        """

        Args:
            input_data: input data for train, could be one of ODPS Table object, odps resource
                        url or odps table name.
            wait:
            job_name:
            good_value:
            sparse_delimiter:
            enable_sparse:
            feature_cols:
            label_col:
            model_name:

        Returns:

        """
        return super(LogisticRegression, self).fit(input_data,
                                                   job_name=job_name,
                                                   wait=wait,
                                                   show_outputs=show_outputs,
                                                   model_name=model_name,
                                                   feature_cols=feature_cols,
                                                   label_col=label_col,
                                                   enable_sparse=enable_sparse,
                                                   sparse_delimiter=sparse_delimiter,
                                                   good_value=good_value)


class RandomForestClassifier(XFlowEstimator):
    _identifier_default = "random-forests-xflow-maxCompute"

    _provider_default = ProviderAlibabaPAI

    _version_default = "1.0.0"

    def __init__(self, session, tree_num, random_col_num, max_tree_deep, min_num_obj=None,
                 min_num_per=None, max_record_size=None, **kwargs):
        super(RandomForestClassifier, self).__init__(session=session, tree_num=tree_num,
                                                     random_col_num=random_col_num,
                                                     max_tree_deep=max_tree_deep,
                                                     min_num_obj=min_num_obj,
                                                     min_num_per=min_num_per,
                                                     max_record_size=max_record_size,
                                                     **kwargs)

    def _compile_args(self, *inputs, **kwargs):
        args = super(RandomForestClassifier, self)._compile_args(*inputs, **kwargs)
        assert len(inputs) > 0

        args["inputArtifact"] = inputs[0]
        args["labelColName"] = kwargs.get("label_col")
        args["modelName"] = kwargs.get("model_name")
        args["treeNum"] = kwargs.get("tree_num")
        args["weighColName"] = kwargs.get("weight_col")
        if kwargs.get("feature_cols") is not None:
            args["featureColNames"] = ",".join(kwargs.get("feature_cols"))
        args["excludedColNames"] = kwargs.get("excluded_cols")
        args["forceCategorical"] = kwargs.get("force_categorical")
        args["algorithmTypes"] = kwargs.get("algo_types")
        args["randomColNum"] = kwargs.get("random_col_num")
        args["minNumObj"] = kwargs.get("min_num_obj")
        args["minNumPer"] = kwargs.get("min_num_per")
        args["maxTreeDeep"] = kwargs.get("max_tree_deep")
        args["maxRecordSize"] = kwargs.get("max_record_size")
        return args

    def fit(self, input_data, model_name=None, feature_cols=None, label_col=None, weight_col=None,
            excluded_cols=None, tree_num=None, wait=True, algo_types=None, random_col_num=None,
            force_categorical=False, **kwargs):
        return super(RandomForestClassifier, self).fit(input_data,
                                                       wait=wait,
                                                       model_name=model_name,
                                                       tree_num=tree_num,
                                                       excluded_cols=excluded_cols,
                                                       feature_cols=feature_cols,
                                                       algo_types=algo_types,
                                                       random_col_num=random_col_num,
                                                       **kwargs)

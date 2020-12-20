======================
使用Estimator
======================


SDK对于部分基础的的算法模块进行了封装，例如逻辑回归和随机森林，使得用户能够更为简单使用PAI服务.

以下是一个逻辑回归的算法的例子


.. code-block:: python

    from pai.algo.classifier import LogisticRegression

    oss_endpoint = "YOUR_OSS_ENDPOINT"
    oss_path = "/YOUR_MODEL_STORE_PATH_IN_OSS/"
    oss_bucket_name = "YOUR_OSS_BUCKET_NAME"
    # OSS Rolearn
    # 公有云用户参考: https://help.aliyun.com/document_detail/106225.html?spm=a2c6h.12873639.0.0.82bd6a8a6K624y
    # 集团内参考: https://yuque.antfin-inc.com/pai-user/manual/fqcsry
    oss_rolearn = "YOUR_OSS_ROLEARN"

    # 算法执行的MaxCompute环境
    maxc_execution = {
        "odpsInfoFile": "/share/base/odpsInfo.ini",
        "endpoint": "MAX_COMPUTE_ENDPOINT",
        "logViewHost": "LOGVIEW_HOST",
        "odpsProject": "YOUR_MAX_COMPUTE_PROJECT",
    }
    model_name = 'test_iris_model_%d' % (random.randint(0, 999999))
    lr = LogisticRegression(regularized_type="l2",
                            pmml_gen=True, pmml_oss_bucket=oss_bucket_name,
                            pmml_oss_path=oss_path, pmml_oss_endpoint=oss_endpoint,
                            pmml_oss_rolearn=oss_rolearn,
                            max_compute_execution=maxc_execution)

    job = lr.fit(wait=True, input_data="odps://pai_online_project/tables/wumai_data",
                job_name="lr-test",
                model_name=model_name, good_value=1, label_col="type",
                feature_cols=["f1", "f2", "f3", "f4"])

    job.wait_for_completion()
    offline_model = job.create_model(output_name="outputArtifact")
import os

test_data_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)))

SCRIPT_DIR_PATH = os.path.join(test_data_dir, "script_dir")

SHELL_SCRIPT_DIR_PATH = os.path.join(test_data_dir, "shell_scripts")

RAW_ARTIFACT_RW_DIR_PATH = os.path.join(test_data_dir, "read_write_raw_artifact")

MAXC_SQL_TEMPLATE_SCRIPT_PATH = os.path.join(test_data_dir, "maxc_sql_scripts")

OPERATOR_MANIFEST_DIR = os.path.join(test_data_dir, "manifests")

CUSTOM_JOB_SCRIPT_PATH = os.path.join(test_data_dir, "custom_job")

CUSTOM_JOB_XGB_PATH = os.path.join(test_data_dir, "custom_job_xgb")

IRIS_DATA_PATH = os.path.join(test_data_dir, "iris_train_test")

PMML_MODEL_PATH = os.path.join(test_data_dir, "pmml_model/regression_model.xml")

TF_MNIST_MODEL_PATH = os.path.join(test_data_dir, "tf_mnist_model")

KERAS_MNIST_SCRIPT_PATH = os.path.join(test_data_dir, "keras_mnist_script")

TORCH_MNIST_SCRIPT_PATH = os.path.join(test_data_dir, "torch_mnist_script")

PYTORCH_MNIST_MODEL_PATH = os.path.join(
    test_data_dir, "pytorch_1_8_mnist_model/torch_mnist.pt"
)

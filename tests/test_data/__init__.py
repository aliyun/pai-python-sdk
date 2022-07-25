import os

test_data_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)))

SCRIPT_DIR_PATH = os.path.join(test_data_dir, "script_dir")

SHELL_SCRIPT_DIR_PATH = os.path.join(test_data_dir, "shell_scripts")

RAW_ARTIFACT_RW_DIR_PATH = os.path.join(test_data_dir, "read_write_raw_artifact")

MAXC_SQL_TEMPLATE_SCRIPT_PATH = os.path.join(test_data_dir, "maxc_sql_scripts")

OPERATOR_MANIFEST_DIR = os.path.join(test_data_dir, "manifests")

CUSOMT_JOB_SCRIPT_PATH = os.path.join(test_data_dir, "custom_job")

CUSTOM_JOB_XGB_PATH = os.path.join(test_data_dir, "custom_job_xgb")

IRIS_DATA_PATH = os.path.join(test_data_dir, "iris_train_test")

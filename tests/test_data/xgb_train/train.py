# %%writefile $source_code_dir/xgb_train.py

import argparse
import logging
import os

import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

TRAINING_BASE_DIR = "/ml/"
TRAINING_CODE_DIR = os.path.join(TRAINING_BASE_DIR, "code/")
TRAINING_OUTPUT_MODEL_DIR = os.path.join(TRAINING_BASE_DIR, "output/model/")


def load_train_test(data_path):
    df = pd.read_csv(data_path, sep=",")
    train, test = train_test_split(df, test_size=0.3)
    train_y = train["target"]
    train_x = train.drop(["target"], axis=1)
    test_y = test["target"]
    test_x = test.drop(["target"], axis=1)
    return train_x, train_y, test_x, test_y


def load_dataset(path):
    if not os.path.exists(path):
        return None, None
    df = pd.read_csv(
        filepath_or_buffer=path,
        sep=",",
    )

    train_y = df["target"]
    train_x = df.drop(["target"], axis=1)
    return train_x, train_y


def main():
    parser = argparse.ArgumentParser(description="XGBoost train example")
    # 用户指定的任务参数
    parser.add_argument(
        "--n_estimators", type=int, default=500, help="The number of base model."
    )
    parser.add_argument(
        "--objective",
        type=str,
        help="Objective function used by XGBoost",
    )

    parser.add_argument(
        "--max_depth",
        type=int,
        default=3,
        help="The maximum depth of the tree.",
    )

    parser.add_argument(
        "--eta",
        type=float,
        default=0.2,
        help="Step size shrinkage used in update to prevents overfitting.",
    )
    parser.add_argument(
        "--eval_metric",
        type=str,
        default=None,
        help="Evaluation metrics for validation data",
    )

    # 作业数据的数据，也通过arguments的方式传递给到训练脚本.
    parser.add_argument(
        "--train_data",
        type=str,
        default=os.environ.get("PAI_INPUT_TRAIN", None),
        help="Input train data path.",
    )
    parser.add_argument(
        "--test_data",
        type=str,
        default=os.environ.get("PAI_INPUT_TEST", None),
        help="Input train data path.",
    )
    args, _ = parser.parse_known_args()
    print(vars(args))

    # 读取传入到容器内的数据
    train_x, train_y = load_dataset(args.train_data)
    print("Train dataset: train_shape={}".format(train_x.shape))
    test_x, test_y = load_dataset(args.test_data)
    if test_x is None or test_y is None:
        print("Test dataset not found")
        eval_set = [(train_x, train_y)]
    else:
        eval_set = [(train_x, train_y), (test_x, test_y)]

    # 这里使用XGBoost的SKLearn API进行作业训练.
    clf = XGBClassifier(
        max_depth=args.max_depth,
        eta=args.eta,
        n_estimators=args.n_estimators,
        objective=args.objective,
        eval_metric=args.eval_metric,
    )
    clf.fit(train_x, train_y, eval_set=eval_set)

    y_pred = clf.predict(test_x)
    accuracy = metrics.accuracy_score(test_y, y_pred)

    # 写出作业在测试集上的精度到 /ml/output/output_parameters/test-accuracy 文件
    print("Output model accuracy=%s" % accuracy)

    # 写出作业产出模型到 /ml/output/model/
    os.makedirs(TRAINING_OUTPUT_MODEL_DIR, exist_ok=True)
    clf.save_model(os.path.join(TRAINING_OUTPUT_MODEL_DIR, "model.json"))
    print(f"Save model succeed: model_path={TRAINING_OUTPUT_MODEL_DIR}xgb_model")


if __name__ == "__main__":
    main()

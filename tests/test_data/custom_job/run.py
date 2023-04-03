import argparse
import os

import pandas as pd
from joblib import dump
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

TRAINING_BASE_DIR = "/ml/"
TRAINING_CODE_DIR = f"{TRAINING_BASE_DIR}code/"
TRAINING_OUTPUT_MODEL_DIR = f"{TRAINING_BASE_DIR}output/model/"

TRAINING_OUTPUT_ACCURACY_PATH = (
    f"{TRAINING_BASE_DIR}output/output_parameters/test-accuracy"
)


def tree_dir(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, "").count(os.sep)
        indent = " " * 4 * (level)
        print("{}{}/".format(indent, os.path.basename(root)))
        subindent = " " * 4 * (level + 1)
        for f in files:
            print("{}{}".format(subindent, f))


def load_datasets(channel_name):
    path = f"{TRAINING_BASE_DIR}input/data/{channel_name}/"
    if not os.path.exists(path):
        return None, None

    # use first file in the channel dir.
    file_name = next(
        iter([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]),
        None,
    )
    if not file_name:
        raise ValueError(f"Not found input file in channel path: {path}")
    file_path = os.path.join(path, file_name)
    df = pd.read_csv(
        filepath_or_buffer=file_path,
        sep=",",
    )

    y = df["target"]
    x = df.drop(["target"], axis=1)
    return x, y


def main():
    parser = argparse.ArgumentParser(description="RandomForest demo algorithm")
    parser.add_argument(
        "--n_estimator", type=int, default=100, help="The number of trees in the forest"
    )
    parser.add_argument(
        "--criterion",
        type=str,
        default="gini",
        choices=["gini", "entropy"],
        help="The function to measure the quality of a split, supported criteria: {'gini', 'entropy'}",
    )

    parser.add_argument(
        "--max_depth",
        type=int,
        default=None,
        help="The maximum depth of the tree.",
    )

    args, _ = parser.parse_known_args()

    tree_dir("/ml")

    estimator = RandomForestClassifier(
        n_estimators=args.n_estimator,
        criterion=args.criterion,
        max_depth=args.max_depth,
        oob_score=True,
    )
    train_x, train_y = load_datasets("train")
    estimator = estimator.fit(train_x, train_y)
    print(
        "oob_score for the train dataset: train:oob_score={0}".format(
            estimator.oob_score_
        )
    )
    test_x, test_y = load_datasets("test")
    accuracy = None
    if test_x is not None and test_y is not None:
        print("Score the model with test dataset")
        pred_y = estimator.predict(test_x)
        accuracy = accuracy_score(test_y, pred_y)
        print("classifier accuracy score: test:accuracy={0}".format(accuracy))
    print("training completed.")
    output_model_dir = TRAINING_OUTPUT_MODEL_DIR
    os.makedirs(output_model_dir, exist_ok=True)
    model_path = os.path.join(output_model_dir, "model.pkl")
    dump(estimator, model_path)

    os.makedirs(os.path.join(output_model_dir, "model_v2"), exist_ok=True)
    dump(estimator, os.path.join(output_model_dir, "model_v2", "model_v2.pkl"))

    print(f"model dump succeed: {model_path}")
    if accuracy is not None:
        os.makedirs(os.path.dirname(TRAINING_OUTPUT_ACCURACY_PATH), exist_ok=True)
        with open(TRAINING_OUTPUT_ACCURACY_PATH, "w") as f:
            f.write(str(accuracy))
        print("write accuracy succeed.")


if __name__ == "__main__":
    main()

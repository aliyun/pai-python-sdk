import os

INPUT_DATA_PATH = "/ml/input/data/"
INPUT_CONFIG_PATH = "/ml/input/config/"
OUTPUT_PATH = "/ml/output/model/"

# INPUT_DATA_PATH = "algorithms/tf_text_classification/demo"
# OUTPUT_PATH = "algorithms/tf_text_classification/output/"

CHANNEL_TRAIN = "train"
CHANNEL_VALIDATION = "validation"
CHANNEL_TEST = "test"
CHANNEL_MODEL = "model"
CHANNEL_PREPROCESS_MODEL = "prep-model"
HYPERPARAMETER_FILE = "hyper-parameters.json"

TRAIN_CHANNEL_PATH = os.path.join(INPUT_DATA_PATH, CHANNEL_TRAIN)
VALIDATION_CHANNEL_PATH = os.path.join(INPUT_DATA_PATH, CHANNEL_VALIDATION)
TEST_CHANNEL_PATH = os.path.join(INPUT_DATA_PATH, CHANNEL_TEST)
MODEL_CHANNEL_PATH = os.path.join(INPUT_DATA_PATH, CHANNEL_MODEL)
PREPROCESS_MODEL_PATH = os.path.join(INPUT_DATA_PATH, CHANNEL_PREPROCESS_MODEL)
HYPERPARAMETER_PATH = os.path.join(INPUT_CONFIG_PATH, HYPERPARAMETER_FILE)
# OUTPUT_MODEL_PATH = os.path.join(OUTPUT_PATH, CHANNEL_MODEL)
OUTPUT_MODEL_PATH = OUTPUT_PATH


BATCH_SIZE = "batch_size"
DROPOUT = "dropout"
LEARNING_RATE = "initial_learning_rate"
NUM_CLASSES = "num_classes"
NUM_EPOCHS = "num_epochs"

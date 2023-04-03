import atexit
import glob
import json
import logging
import os
import sys

import constants
import official.nlp.optimization
import tensorflow as tf
import tensorflow_hub as tfhub

# noinspection PyUnresolvedReferences
import tensorflow_text as text

print("Tensorflow list physical devices: {}".format(tf.config.list_physical_devices()))


class FineTuneClassifier(tf.keras.Model):
    def __init__(self, base_model, num_classes, dropout=0.1, trainable=True):
        super(FineTuneClassifier, self).__init__(name="prediction")
        base_encoder = tf.saved_model.load(base_model)
        self.encoder = tfhub.KerasLayer(base_encoder, trainable=trainable)
        self.dropout = tf.keras.layers.Dropout(dropout)
        self.dense = tf.keras.layers.Dense(num_classes)

    def call(self, preprocessed_text):
        encoder_outputs = self.encoder(preprocessed_text)
        pooled_output = encoder_outputs["pooled_output"]
        x = self.dropout(pooled_output)
        x = self.dense(x)
        return x


class MetricsPublisher(tf.keras.callbacks.Callback):
    def on_train_batch_end(self, step, logs=None):
        if step % 100 == 0:
            lr = float(self.model.optimizer.learning_rate(step=step))
            log_string_head = f"tensorflow:TRAIN:lr = {lr},step = {step}"
            for metric_key in logs:
                log_string_head += f",{metric_key} = {logs[metric_key]}"
            logging.info(log_string_head)

    def on_test_end(self, logs=None):
        log_string_head = "tensorflow:VALIDATION:"
        log_string_head += ",".join(
            [f"{metric_key} = {logs[metric_key]}" for metric_key in logs]
        )
        logging.info(log_string_head)


def make_bert_preprocess_model(sentence_features, seq_length=128):
    """Returns Model mapping string features to BERT inputs.

    Args:
      sentence_features: a list with the names of string-valued features.
      seq_length: an integer that defines the sequence length of BERT inputs.

    Returns:
      A Keras Model that can be called on a list or dict of string Tensors
      (with the order or names, resp., given by sentence_features) and
      returns a dict of tensors for input to BERT.
    """

    input_segments = [
        tf.keras.layers.Input(shape=(), dtype=tf.string, name=ft)
        for ft in sentence_features
    ]

    # Tokenize the text to word pieces.
    bert_preprocess = tf.saved_model.load(constants.PREPROCESS_MODEL_PATH)
    tokenizer = tfhub.KerasLayer(bert_preprocess.tokenize, name="tokenizer")
    segments = [tokenizer(s) for s in input_segments]

    # Optional: Trim segments in a smart way to fit seq_length.
    # Simple cases (like this example) can skip this step and let
    # the next step apply a default truncation to approximately equal lengths.
    truncated_segments = segments

    # Pack inputs. The details (start/end token ids, dict of output tensors)
    # are model-dependent, so this gets loaded from the SavedModel.
    packer = tfhub.KerasLayer(
        bert_preprocess.bert_pack_inputs,
        arguments=dict(seq_length=seq_length),
        name="packer",
    )
    model_inputs = packer(truncated_segments)
    return tf.keras.Model(input_segments, model_inputs)


def load_csv_data_into_tf(
    csv_file,
    batch_size,
    is_training=False,
    delimiter=",",
    preprocess_model=lambda ex: ex,
):
    options = tf.data.Options()
    # options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.DATA
    dataset = tf.data.experimental.make_csv_dataset(
        csv_file,
        batch_size=batch_size,
        field_delim=delimiter,
        header=False,
        column_names=["label", "sentence"],
        num_epochs=1,
    ).with_options(options)

    if is_training:
        dataset = dataset.shuffle(2000).repeat()

    dataset = dataset.map(lambda ex: (preprocess_model(ex), ex["label"]))
    # dataset = dataset.cache().prefetch(buffer_size=tf.data.AUTOTUNE)
    dataset = dataset.cache().prefetch(buffer_size=256)
    return dataset


def find_file_in_path(path, file_type="*"):
    files = glob.glob(os.path.join(path, file_type))
    if len(files) != 1:
        raise ValueError(f"Expected 1 matched file. Found {len(files)}: {files}")
    return files[0]


def get_num_examples_from_csv(csv_file):
    with open(csv_file, "r") as fr:
        return len(fr.readlines())


def start_training(strategy):
    with open(constants.HYPERPARAMETER_PATH) as hp_file:
        hp = json.load(hp_file)
        hp[constants.BATCH_SIZE] = int(hp[constants.BATCH_SIZE])
        hp[constants.DROPOUT] = float(hp[constants.DROPOUT])
        hp[constants.LEARNING_RATE] = float(hp[constants.LEARNING_RATE])
        hp[constants.NUM_EPOCHS] = int(hp[constants.NUM_EPOCHS])
        hp[constants.NUM_CLASSES] = int(hp[constants.NUM_CLASSES])

    with strategy.scope():
        preprocess_model = make_bert_preprocess_model(["sentence"])
        training_data = load_csv_data_into_tf(
            find_file_in_path(constants.TRAIN_CHANNEL_PATH),
            batch_size=hp[constants.BATCH_SIZE],
            is_training=True,
            delimiter="\t",
            preprocess_model=preprocess_model,
        )
        num_examples = get_num_examples_from_csv(
            find_file_in_path(constants.TRAIN_CHANNEL_PATH)
        )
        steps_per_epoch = num_examples // hp[constants.BATCH_SIZE]
        num_train_steps = steps_per_epoch * hp[constants.NUM_EPOCHS]
        num_warmup_steps = num_train_steps // 10
        if os.path.exists(constants.VALIDATION_CHANNEL_PATH):
            validation_data = load_csv_data_into_tf(
                find_file_in_path(constants.VALIDATION_CHANNEL_PATH),
                batch_size=hp[constants.BATCH_SIZE],
                delimiter="\t",
                preprocess_model=preprocess_model,
            )
        else:
            validation_data = None
        # if os.path.exists(constants.TEST_CHANNEL_PATH):
        #     test_data = load_csv_data_into_tf(
        #         find_file_in_path(constants.TEST_CHANNEL_PATH),
        #         batch_size=hp[constants.BATCH_SIZE],
        #         delimiter="\t",
        #         preprocess_model=preprocess_model,
        #     )
        # else:
        #     pass

        loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        metrics = [
            tf.keras.metrics.SparseCategoricalAccuracy("accuracy", dtype=tf.float32),
            # tf.keras.metrics.AUC(name="auc"),
        ]

        optimizer = official.nlp.optimization.create_optimizer(
            init_lr=hp[constants.LEARNING_RATE],
            num_train_steps=num_train_steps,
            num_warmup_steps=num_warmup_steps,
            optimizer_type="adamw",
        )
        model = FineTuneClassifier(
            base_model=constants.MODEL_CHANNEL_PATH,
            num_classes=hp[constants.NUM_CLASSES],
            dropout=hp[constants.DROPOUT],
        )
        model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

        model.fit(
            x=training_data,
            validation_data=validation_data,
            steps_per_epoch=steps_per_epoch,
            verbose=2,
            epochs=hp[constants.NUM_EPOCHS],
            callbacks=[MetricsPublisher()],
        )

        # Save FineTuneClassifier only for future incremental training
        # model.save(constants.OUTPUT_MODEL_PATH, include_optimizer=True)

        # Save the entire model all together for one-step inference.
        logging.debug("Training completed. Prepare model saving.")
        preprocess_inputs = preprocess_model.inputs
        bert_encoder_inputs = preprocess_model(preprocess_inputs)
        bert_outputs = model(bert_encoder_inputs)
        model_for_inference = tf.keras.Model(preprocess_inputs, bert_outputs)
        model_for_inference.save(constants.OUTPUT_MODEL_PATH)
        logging.debug("Saving completed. Exiting.")


if __name__ == "__main__":
    logging.basicConfig(
        format="%(levelname)s:%(message)s", level=logging.INFO, stream=sys.stdout
    )
    tf.get_logger().setLevel("ERROR")
    training_strategy = tf.distribute.MirroredStrategy()
    start_training(training_strategy)
    # atexit.register(training_strategy._extended._collective_ops._pool.close)  # type: ignore

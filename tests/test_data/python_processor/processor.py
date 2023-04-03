import io
import multiprocessing
import os

import allspark
import joblib
import numpy as np
import sklearn

ENV_PAI_SERVICE_WORKER_COUNT_PER_CPU = "PAI_SERVICE_WORKER_COUNT_PER_CPU"
ENV_PAI_SERVICE_ENDPOINT = "PAI_SERVICE_ENDPOINT"


class CustomPythonProcessor(allspark.BaseProcessor):
    """MyProcessor is an example
    you can send message like this to predict
    curl -v http://127.0.0.1:8080/api/predict/service_name -d '2 105'"""

    def __init__(self, *args, **kwargs):
        super(CustomPythonProcessor, self).__init__(*args, **kwargs)
        self.model = None

    @classmethod
    def load_model(cls):
        model_dir = "/eas/workspace/model"
        # find sklearn mode under the model directory.
        name = next(
            (name for name in os.listdir(model_dir) if name.endswith("pkl")), None
        )
        print("model dir files", os.listdir(model_dir))
        if not name:
            raise RuntimeError(
                "Not found sklearn learn model under the model directory."
            )
        print("Load model from model_path={}".format(os.path.join(model_dir, name)))
        return joblib.load(os.path.join(model_dir, name))

    def initialize(self):
        """load module, executed once at the start of the service
        do service initialization and load models in this function.
        """
        model = self.load_model()
        self.model = model

    def process(self, data):
        """process the request data"""
        print("Process input data: %s", data)
        x = np.load(io.BytesIO(data))
        y = self.model.predict(x)

        output = io.BytesIO()
        np.save(output, y)
        output.seek(0)

        return output.read(), 200


if __name__ == "__main__":
    print("processor.py launching")
    cpu_count = multiprocessing.cpu_count()
    port = int(os.environ.get("PAI_SERVING_PORT", 8000))
    print("PAI_SERVICE_PORT: ", port)
    runner = CustomPythonProcessor(
        worker_processes=cpu_count,
        endpoint=f"0.0.0.0:{port}",
    )
    runner.run()

import io
import logging
import os

import numpy as np
import tensorflow as tf
import tensorflow_text as text
import uvicorn
from fastapi import Depends, FastAPI, Request, Response

print("Tensorflow list physical devices: ", tf.config.list_physical_devices())

logging.basicConfig(
    format="%(asctime)s: %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)


app = FastAPI()


def load_model():
    model_dir = "/eas/workspace/model"
    # find sklearn mode under the model directory.
    return tf.saved_model.load(model_dir)


model = load_model()

logger = logging.getLogger(__name__)

logger.info("Service initializing....")


async def get_body(request: Request):
    return await request.body()


@app.post("/")
def predict(body: bytes = Depends(get_body)):
    logger.info("API Predict Invocation.")
    global model
    response = predict_fn(body, model)
    return Response(content=response)


def predict_fn(data: bytes, model) -> bytes:
    x = np.load(io.BytesIO(data))
    result = model.signatures["serving_default"](tf.constant(x, name="sentences"))
    output = io.BytesIO()
    np.save(output, result["prediction"].numpy())
    output.seek(0)
    return output.read()


if __name__ == "__main__":
    logger.info("FastAPI server launching")
    logger.info(os.environ)
    port = int(os.environ.get("PAI_SERVING_PORT", 7999))
    uvicorn.run(app, host="0.0.0.0", port=port)

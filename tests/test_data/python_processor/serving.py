import io
import logging
import os

import joblib
import numpy as np
import uvicorn
from fastapi import Depends, FastAPI, Request, Response

logging.basicConfig(
    format="%(asctime)s: %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)


app = FastAPI()


def load_model():
    model_dir = "/eas/workspace/model"
    # find sklearn mode under the model directory.
    name = next((name for name in os.listdir(model_dir) if name.endswith("pkl")), None)
    print("model dir files", os.listdir(model_dir))
    if not name:
        raise RuntimeError("Not found sklearn learn model under the model directory.")

    return joblib.load(os.path.join(model_dir, name))


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
    y = model.predict(x)
    output = io.BytesIO()
    np.save(output, y)
    output.seek(0)
    return output.read()


if __name__ == "__main__":
    logger.info("FastAPI server launching")
    logger.info(os.environ)
    port = int(os.environ.get("PAI_SERVING_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

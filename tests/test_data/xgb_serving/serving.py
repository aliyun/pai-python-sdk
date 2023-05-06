import io
import logging
import os

import numpy as np
import uvicorn
import xgboost
from fastapi import Depends, FastAPI, Request, Response
from xgboost import XGBClassifier

print("XGBoost Version: ", xgboost.__version__)

logging.basicConfig(
    format="%(asctime)s: %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)


app = FastAPI()


def load_model():
    model_dir = os.environ.get("MODEL_MOUNT_PATH", "/eas/workspace/model")
    print("model_dir is", model_dir)
    # find sklearn mode under the model directory.
    name = next((name for name in os.listdir(model_dir) if name.endswith("json")), None)
    print("model dir files", os.listdir(model_dir))
    if not name:
        raise RuntimeError("Not found sklearn learn model under the model directory.")

    xgb_model = XGBClassifier()
    xgb_model.load_model(os.path.join(model_dir, name))

    return xgb_model


model = load_model()

logger = logging.getLogger(__name__)

logger.info("Service initializing....")


async def get_body(request: Request):
    return await request.body()


@app.post("/")
def predict_v1(body: bytes = Depends(get_body)):
    logger.info("API PredictV1 Invocation.")
    global model
    response = predict_fn(body, model)
    return Response(content=response)


@app.post("/predict")
def predict_v2(body: bytes = Depends(get_body)):
    logger.info("API PredictV2 Invocation.")
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
    port = int(os.environ.get("LISTENING_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

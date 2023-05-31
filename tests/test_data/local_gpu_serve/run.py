import os

import torch
from flask import Flask, request

app = Flask(__name__)


@app.post("/")
def predict():
    print("Request Data: ", request.data.decode())
    return torch.randn(2, 3).numpy().tolist()


if __name__ == "__main__":
    if not torch.cuda.is_available():
        raise ValueError("CUDA is not available.")
    print("Current CUDA Device: ", torch.cuda.current_device())
    port = int(os.environ.get("LISTENING_PORT", 8000))
    app.run(host="0.0.0.0", port=port)

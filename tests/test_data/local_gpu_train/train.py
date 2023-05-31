import subprocess

import torch


def run():
    if not torch.cuda.is_available():
        raise ValueError("CUDA is not available.")
    print("Torch CUDA Current Device: ", torch.cuda.current_device())
    subprocess.check_call(["nvidia-smi"])


if __name__ == "__main__":
    run()

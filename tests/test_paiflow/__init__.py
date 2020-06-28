import os

import yaml

_current_dir_path = os.path.dirname(os.path.abspath(__file__))


def load_local_yaml(name):
    with open(os.path.join(_current_dir_path, "test_data", name), 'r') as f:
        return yaml.load(f.read(), yaml.FullLoader)

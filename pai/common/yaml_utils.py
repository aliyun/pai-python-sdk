#  Copyright 2023 Alibaba, Inc. or its affiliates.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import yaml


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def dump(data):
    """Serialize input Python object with NoAliasDumper.

    Args:
        data: a Python object.

    Returns:
        str: Return the produced string.

    """
    return yaml.dump(data, Dumper=NoAliasDumper)


def dump_all(seq):
    """Serialize a sequence of Python objects with NoAliasDumper.

    Args:
        seq : A sequence of Python objects.

    Returns:
        str: Return the produced string.

    """
    return yaml.dump_all(seq, Dumper=NoAliasDumper)


def safe_load(stream):
    """Parse the first YAML document in the stream."""
    return yaml.safe_load(stream)

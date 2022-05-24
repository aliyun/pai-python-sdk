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

#!/bin/bash
# Generate and apply type annotation using MonkeyType.
# Documents: https://monkeytype.readthedocs.io/en/stable/index.html
#
# Note: As said in the documents, annotation from MonkeyType is informative first draft,
# and should be corrected by the developer.


test_module=${1:-tests/unit}

python -m pip install MonkeyType

# Collect type hints by run the unit test
monkeytype run -m pytest $test_module

# Apply the collected type information.
monkeytype list-modules | grep 'pai\.' | grep -v "pai\.schema" | grep -v "pai\.operator" | grep -v "pai\.pipeline" | grep -v "pai\.libs" | xargs -L 1 monkeytype  apply

Contributing to PAI Python SDK
================================



Developing and testing
--------------------------
Initialize a virtual environment for development purpose with conda (or pyenv).

.. code-block:: shell

    # use conda
    conda create --name pai-dev-py36 python=3.6
    conda activate pai-dev-py36

    # install develop requirements
    python -m pip install -r requirements/dev-requirements.txt
    python -m pip install -e .


Setup pre-commit config with **pre-commit** tool (included in dev-requirements.txt).

.. code-block:: shell

    # move .pre-commit-config.yaml to git hook path.
    pre-commit install


Using nox
----------------------------------

The project use `nox <https://nox.readthedocs.io/en/latest/>`__  to run linter and code formatter(black).

.. code-block:: shell

    # show available session configured in noxfile.py
    nox -l

    # run linter (flake8 && black check)
    nox -s lint

    # run code formatter.
    nox -s black

    # build the document
    nox -s doc

    # run all tests, linter and code-formatter.
    nox


Run test
----------------------------------

Use **nox** to run the unit and integration tests.

Before running integration tests, you should initialize a test config file ( *test.ini* ) under directory tests/integration.
For the detail content in the config file, please check the file *tests/integration/test.init.template*



.. code-block:: shell

    # run unit test
    nox -s unit

    # run integration test
    nox -s integration

    # passing extra arguments to pytest
    # example: enable parallel test with 8 worker.
    nox -s integration -- -n 8

    # example: run a specific test case.
    nox -s integration -- -k TestPmmlPredictor

    # overwrite default test_config name (test.ini).
    # example: use test_public_cn_shanghai.ini under tests/integration as the config file.
    PAI_TEST_CONFIG=test_public_cn_shanghai.ini nox -s integration

    # test notebooks in toturial
    nox -s notebook



Release Package/Documents
----------------------------------

Currently, the project use OSS to distribute the package and publish the documents. For OSS credentials, please contact with the project owner.

.. code-block:: shell

    # release current package to OSS
    # OSS URL for the package
    # https://pai-sdk.oss-cn-shanghai.aliyuncs.com/alipai/dist/alipai-0.3.6.dev3-py2.py3-none-any.whl
    ./tools/release_pkg.sh oss

    # publish documents for preview purpose.
    ./tools/publish_doc.sh preview

    # publish documents for production purpose.
    ./tools/publish_doc.sh production

Package Structure
--------------------------

An explanation of the package structure shown below.

```plain

├── docs/                           // Documents of the project.
├── pai/
│   ├── api/                        // ResourceAPIs used to operate specific Resource with PAI REST API.
│   ├── common/                     // Some common utilities.
│   ├── libs/                       // Thirdparty libs.
│   ├── schema                      // schema class used to transform between API object and resource entity.
│   ├── estimator.py                // Files under pai are major API provided by PAI SDK.
│   ├── model.py
│   ├── predictor.py
│   ├── ...
│   ├── ...
├── tests
│   ├── integration/                // Integration test case
│   ├── test_data/                  // Resource used in test case.
│   └── unit/                       // Unit test case.
└── tools/                          // Tools used for publishing SDK and document.

```

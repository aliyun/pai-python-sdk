import os.path

import nox
from nox.sessions import Session

BLACK_VERSION = "black==22.6.0"

TEST_DEPENDENCIES = [
    "pytest",
    "pytest-cov",
    "pytest-xdist",
    "mock>=2.0.0",
    "aliyun-python-sdk-core==2.13.25",
]

PASSING_ENVIRONMENTS = {
    "PAI_TEST_CONFIG": "test.ini",
}


UNIT_TEST_PYTHON_VERSIONS = ["3.6", "3.7", "3.8"]
# INTEGRATION_TEST_PYTHON_VERSIONS = ["3.6"]
TEST_VENV_BACKEND = os.environ.get("PAI_TEST_VENV_BACKEND", "conda")


def install_test_dependencies(session: Session):
    # install package
    session.install("-e", ".")

    # fix eas_prediction protobuf requirement.
    try:
        session.install("protobuf==3.20.*")
    except Exception:
        pass

    # install test requirements
    session.install(*TEST_DEPENDENCIES)


@nox.session
def lint(session: Session):
    """Enforce code style with flake8."""
    session.install("flake8")
    session.install(BLACK_VERSION)
    session.run("flake8", "--config", ".flake8")
    session.run("black", "--check", ".")


@nox.session(venv_backend=TEST_VENV_BACKEND)
def integration(session: Session):
    """Run integration test."""
    install_test_dependencies(session=session)

    env = {
        key: os.environ.get(key, value)
        for key, value in PASSING_ENVIRONMENTS.items()
        if os.environ.get(key, value) is not None
    }

    session.run(
        "pytest",
        "--cov-config=.coveragerc",
        "--cov-append",
        "--cov-report=html",
        "--cov=pai",
        os.path.join("tests", "integration"),
        *session.posargs,
        env=env,
    )
    session.run(
        "coverage",
        "report",
        "-i",
        "--rcfile=.coveragerc",
    )


@nox.session(venv_backend=TEST_VENV_BACKEND, python=UNIT_TEST_PYTHON_VERSIONS)
def unit(session: Session):
    """Run unit test."""
    install_test_dependencies(session=session)
    session.run(
        "pytest",
        "--cov-config=.coveragerc",
        "--cov-append",
        "--cov-report=html",
        "--cov=pai",
        os.path.join("tests", "unit"),
        *session.posargs,
    )
    session.run(
        "coverage",
        "report",
        "-i",
        "--rcfile=.coveragerc",
    )


@nox.session(reuse_venv=True)
def black(session: Session):
    """Format code with black."""
    session.install("black==22.6.0")
    session.run("black", ".")


@nox.session(reuse_venv=True)
def doc(session: Session):
    """Build the documents with Sphinx."""
    session.install("-e", ".")
    session.install("sphinx", "sphinx-rtd-theme")

    with session.chdir("./docs"):
        session.run(
            "sphinx-build",
            "-T",
            "-b",
            "html",
            "source",
            "build",
        )


@nox.session(reuse_venv=True)
def coverage(session: Session):
    """"""
    session.install("coverage", "pytest-cov")
    session.run("coverage", "report", "--show-missing")
    session.run("coverage", "erase")

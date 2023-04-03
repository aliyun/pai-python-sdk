import os.path

import nox
from nox.sessions import Session

_pkg_root = os.path.dirname(os.path.abspath(__file__))

TEST_REQUIREMENTS = os.path.join(
    _pkg_root,
    "requirements/test-requirements.txt",
)

LINT_REQUIREMENTS = os.path.join(
    _pkg_root,
    "requirements/lint-requirements.txt",
)


DOC_REQUIREMENTS = os.path.join(
    _pkg_root,
    "requirements/doc-requirements.txt",
)

PASSING_ENVIRONMENTS = {
    "PAI_TEST_CONFIG": "test.ini",
}


UNIT_TEST_PYTHON_VERSIONS = ["3.6", "3.7", "3.8"]
# INTEGRATION_TEST_PYTHON_VERSIONS = ["3.6"]
TEST_VENV_BACKEND = os.environ.get("PAI_TEST_VENV_BACKEND", "conda")


def install_test_dependencies(session: Session):
    # install package
    session.install("-e", ".")

    # install test requirements
    session.install("-r", TEST_REQUIREMENTS)


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


@nox.session
def lint(session: Session):
    """Enforce code style with flake8."""
    session.install("-r", LINT_REQUIREMENTS)
    session.run("flake8", "--config", ".flake8")
    session.run("black", "--check", ".")


@nox.session(reuse_venv=True)
def black(session: Session):
    """Format code with black."""
    session.install("-r", LINT_REQUIREMENTS)
    session.run("black", ".")


@nox.session(reuse_venv=True)
def doc(session: Session):
    """Build the documents with Sphinx."""
    session.install("-e", ".")
    session.install("-r", DOC_REQUIREMENTS)

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
    """Coverage report"""
    install_test_dependencies(session)
    session.run("coverage", "report", "--show-missing")
    session.run("coverage", "erase")


@nox.session(reuse_venv=True)
def notebook(session: Session):
    """Run jupyter notebook test with nbmake.

    How to use nbmake:
    https://semaphoreci.com/blog/test-jupyter-notebooks-with-pytest-and-nbmake

    """
    install_test_dependencies(session)
    session.install("-r", DOC_REQUIREMENTS)

    session.run(
        "pytest",
        "--timeout",
        "3000",
        "--nbmake",
        "-n=auto",
        "docs/source/tutorial/",
    )

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

from __future__ import absolute_import

import os
import subprocess
import tempfile
import warnings
from typing import Dict, Optional

import six
from six.moves import urllib

from .logging import get_logger

logger = get_logger(__name__)


def git_clone_repo(git_config: Dict[str, str], source_dir: Optional[str] = None):
    """Git clone the required repo and checkout the required branch and commit.

    This method will clone the repo to a temporary directory, checkout the required branch and commit,
    and return a dict that contains the updated value of ``source_dir``.

    Example::

        git_config = {
            "repo": "https://github.com/your_repo.git",
            "branch": "master",
            "commit": "xxxxxxx",
            "username": "xxxxxxx",
            "password": "xxxxxxx",
            "token": "xxxxxxx",
        }
        updated_args = git_clone_repo(git_config, source_dir="./train/src/")

    Args:
        git_config (Dict[str, str]): Git configuration used to clone the repo. Including
            ``repo``, ``branch``, ``commit``, ``username``, ``password`` and ``token``.
            The ``repo`` is required. All other fields are optional. ``repo`` specifies
            the Git repository. If you don't provide ``branch``, the default value 'master'
            is used. If you don't provide ``commit``, the latest commit in the specified
            branch is used. ``username``, ``password`` and ``token`` are for authentication
            purpose.
        source_dir (Optional[str], optional): A relative location to a directory in the git
            repo (default: None). If you don't provide this argument, the root directory of
            the git repo is used. If you provide this argument, the source directory must
            exist in the git repo.

    Returns:
        dict: A dict that contains the updated value of ``source_dir``.
    """
    _validate_git_config(git_config)
    dest_dir = tempfile.mkdtemp()
    _build_and_run_clone_command(git_config, dest_dir)
    _checkout_commit(git_config, dest_dir)

    updated_args = {
        "source_dir": source_dir,
    }

    if source_dir:
        if not os.path.isdir(os.path.join(dest_dir, source_dir)):
            raise ValueError("Source directory does not exist in the repo.")
        updated_args["source_dir"] = os.path.join(dest_dir, source_dir)
    else:
        updated_args["source_dir"] = dest_dir
    return updated_args


def _validate_git_config(git_config):
    """Validate the git configuration.

    Check if ``repo`` is provided and if the values in ``git_config`` are strings.

    Args:
        git_config (Dict[str, str]): Git configuration to be validated.

    Raises:
        ValueError: If ``repo`` is not provided or the values in ``git_config`` are not strings.
    """
    if "repo" not in git_config:
        raise ValueError(
            "repo not found in git_config. Please provide a repo for git_config."
        )
    for key in git_config:
        if not isinstance(git_config[key], six.string_types):
            raise ValueError(f"'{key}' must be a string.")


def _build_and_run_clone_command(git_config, dest_dir):
    """Build and run the clone command.

    If ``repo`` in git_config is valid, build and run the clone command. Otherwise, raise an error.

    Args:
        git_config (Dict[str, str]): Git configuration used to clone the repo.
        dest_dir (str): The destination directory to clone the repo to.

    Raises:
        ValueError: If ``repo`` provided is not supported.
    """
    if git_config["repo"].startswith("https://codeup.aliyun.com/") or git_config[
        "repo"
    ].startswith("git@codeup.aliyun.com"):
        _clone_command_for_codeup(git_config, dest_dir)
    elif git_config["repo"].startswith("https://github.com/") or git_config[
        "repo"
    ].startswith("git@github.com"):
        _clone_command_for_github(git_config, dest_dir)
    else:
        raise ValueError("repo provided is not supported.")


def _clone_command_for_codeup(git_config, dest_dir):
    """Build and run the clone command for Alibaba Codeup.

    If ``repo`` starts with ``https://``, use https to clone the repo. If ``repo`` starts with ``git@``,
    use ssh to clone the repo. Otherwise, raise an error.

    Args:
        git_config (Dict[str, str]): Git configuration used to clone the repo.
        dest_dir (str): The destination directory to clone the repo to.
    """
    is_ssh = git_config["repo"].startswith("git@")
    is_https = git_config["repo"].startswith("https://")
    if is_ssh:
        _clone_command_for_ssh(git_config, dest_dir)
    elif is_https:
        _clone_command_for_codeup_https(git_config, dest_dir)
    else:
        raise ValueError("repo must start with 'https://' or 'git@'.")


def _clone_command_for_github(git_config, dest_dir):
    """Build and run the clone command for GitHub.

    If ``repo`` starts with ``https://``, use https to clone the repo. If ``repo`` starts with ``git@``,
    use ssh to clone the repo. Otherwise, raise an error.

    Args:
        git_config (Dict[str, str]): Git configuration used to clone the repo.
        dest_dir (str): The destination directory to clone the repo to.
    """
    is_ssh = git_config["repo"].startswith("git@")
    is_https = git_config["repo"].startswith("https://")
    if is_ssh:
        _clone_command_for_ssh(git_config, dest_dir)
    elif is_https:
        _clone_command_for_github_https(git_config, dest_dir)
    else:
        raise ValueError("repo must start with 'https://' or 'git@'.")


def _clone_command_for_ssh(git_config, dest_dir):
    """Build and run the clone command for GitHub via SSH.

    Clone the repo via SSH. All credentials in ``git_config`` are ignored.

    Args:
        git_config (Dict[str, str]): Git configuration used to clone the repo.
        dest_dir (str): The destination directory to clone the repo to.
    """
    if "username" in git_config or "password" in git_config or "token" in git_config:
        warnings.warn(
            "``username``, ``password``, and ``token`` are not used when cloning via SSH."
        )
    _clone_command(git_config["repo"], dest_dir, branch=git_config.get("branch"))


def _clone_command_for_github_https(git_config, dest_dir):
    """Build and run the clone command for GitHub via HTTPS.

    Clone the repo via HTTPS. If ``token`` is provided, use token to clone the repo. If ``username``
    and ``password`` are provided, use ``username`` and ``password`` to clone the repo. Otherwise,
    clone the repo without authentication.

    Args:
        git_config (Dict[str, str]): Git configuration used to clone the repo.
        dest_dir (str): The destination directory to clone the repo to.
    """
    repo_url = git_config["repo"]
    updated_url = repo_url
    if "token" in git_config:
        if "username" in git_config or "password" in git_config:
            warnings.warn(
                "``username`` and ``password`` are not used when ``token`` is provided."
            )
        updated_url = _update_url_with_token(repo_url, git_config["token"])
    elif "username" in git_config and "password" in git_config:
        updated_url = _update_url_with_username_and_password(
            repo_url, git_config["username"], git_config["password"]
        )
    elif "username" in git_config or "password" in git_config:
        warnings.warn(
            "``username`` and ``password`` need to be provided together. Credentials provided in git config will be ignored"
        )
    else:
        warnings.warn(
            "No credentials provided. If the repo is private, cloning will fail."
        )
    _clone_command(updated_url, dest_dir, branch=git_config.get("branch"))


def _clone_command_for_codeup_https(git_config, dest_dir):
    """Build and run the clone command for Codeup via HTTPS.

    Clone the repo via HTTPS. If ``username`` and ``token`` are provided, use ``username`` and
    ``token`` to clone the repo. If ``username`` and ``password`` are provided, use ``username``
    and ``password`` to clone the repo. Otherwise, clone the repo without authentication.

    Args:
        git_config (Dict[str, str]): Git configuration used to clone the repo.
        dest_dir (str): The destination directory to clone the repo to.
    """
    repo_url = git_config["repo"]
    updated_url = repo_url
    if "username" in git_config and "token" in git_config:
        if "password" in git_config:
            warnings.warn("``password`` is not used when ``token`` is provided.")
        updated_url = _update_url_with_username_and_password(
            repo_url, git_config["username"], git_config["token"]
        )
    elif "username" in git_config and "password" in git_config:
        updated_url = _update_url_with_username_and_password(
            repo_url, git_config["username"], git_config["password"]
        )
    elif "username" in git_config or "password" in git_config or "token" in git_config:
        warnings.warn(
            "``username`` and ``password``/``token`` of Codeup account need to be "
            "provided together. Credentials provided in git config will be ignored."
        )
    else:
        warnings.warn(
            "No credentials provided. If the repo is private, cloning will fail."
        )

    if "commit" not in git_config and "branch" in git_config:
        # do shallow clone for the specific branch
        shallow_clone_branch = _clone_command(
            updated_url, dest_dir, branch=git_config.get("branch")
        )
    else:
        shallow_clone_branch = None
    _clone_command(updated_url, dest_dir, branch=shallow_clone_branch)


def _clone_command(repo_url, dest_dir, branch=None):
    """Build and run the clone command.

    Clone the repo to ``dest_dir``.

    Args:
        repo_url (str): The URL of the repo to be cloned.
        dest_dir (str): The destination directory to clone the repo to.
        branch (str): The specific branch to be cloned.

    Raises:
        ValueError: If ``repo_url`` does not start with ``https://`` or ``git@``.
    """
    my_env = os.environ.copy()

    if branch:
        # shallow clone the specific branch/tag
        git_command = [
            "git",
            "clone",
            "-c",
            "advice.detachedHead=false",  # disable detached head warning
            "--depth",
            "1",
            "--branch",
            branch,
            repo_url,
            dest_dir,
        ]
    else:
        git_command = ["git", "clone", repo_url, dest_dir]

    if repo_url.startswith("git@"):
        with tempfile.NamedTemporaryFile() as sshnoprompt:
            with open(sshnoprompt.name, "w") as write_pipe:
                write_pipe.write("ssh -oBatchMode=yes $@")
            os.chmod(sshnoprompt.name, 0o511)
            my_env["GIT_SSH"] = sshnoprompt.name
            subprocess.check_call(git_command, env=my_env)
    elif repo_url.startswith("https://"):
        my_env["GIT_TERMINAL_PROMPT"] = "0"
        subprocess.check_call(git_command, env=my_env)
    else:
        raise ValueError("repo must start with 'https://' or 'git@'.")


def _update_url_with_token(repo_url, token):
    """Update the URL with token.

    Update the URL with token. If the URL already contains token, return the URL as is.

    Args:
        repo_url (str): The URL of the repo to be cloned.
        token (str): The token used to clone the repo.

    Returns:
        str: The updated URL for the git clone command.
    """
    index = len("https://")
    if repo_url.find(token) == index:
        return repo_url
    updated_url = repo_url[:index] + token + "@" + repo_url[index:]
    return updated_url


def _update_url_with_username_and_password(repo_url, username, password):
    """Update the URL with username and password.

    Update the URL with username and password.

    Args:
        repo_url (str): The URL of the repo to be cloned.
        username (str): The username used to clone the repo.
        password (str): The password used to clone the repo.

    Returns:
        str: The updated URL for the git clone command.
    """
    index = len("https://")
    password = urllib.parse.quote(password)
    updated_url = repo_url[:index] + username + ":" + password + "@" + repo_url[index:]
    return updated_url


def _checkout_commit(git_config, dest_dir):
    """Checkout the commit specified in ``git_config``.

    If ``commit`` is specified in ``git_config``, checkout the commit.

    Args:
        git_config (Dict[str, str]): Git configuration used to clone the repo.
        dest_dir (str): The destination directory to clone the repo to.
    """
    if "branch" in git_config and "commit" in git_config:
        logger.warning(
            "commit and branch are both specified in git config, ignore branch."
        )
    if "commit" in git_config:
        subprocess.check_call(
            args=[
                "git",
                "-c",
                "advice.detachedHead=false",  # disable detached head warning
                "checkout",
                git_config["commit"],
            ],
            cwd=str(dest_dir),
        )

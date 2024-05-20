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

import io
import subprocess
import time
from random import randint
from typing import Any, Dict, List, Optional, Union

from .logging import get_logger

logger = get_logger(__name__)


def _run_command(command: List[str], input: Optional[str] = None):
    with subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=False,
        bufsize=1,
    ) as p:
        if input:
            p.stdin.write(input.encode())
        p.stdin.close()
        out = io.TextIOWrapper(p.stdout, newline="", errors="replace")
        for line in out:
            logger.info(line)

    return p.returncode


class ContainerRun(object):
    """A class represent a container run in local."""

    CONTAINER_STATUS_RUNNING = "running"
    CONTAINER_STATUS_EXITED = "exited"
    CONTAINER_STATUS_PAUSED = "paused"

    def __init__(self, container, port: Optional[int] = None):
        """Initialize a container run.

        Args:
            container: A docker container object.
            port (int): The host port that container is exposed to.

        """
        self.container = container
        self.port = port

    @property
    def status(self):
        self.container.reload()
        return self.container.status

    def is_running(self):
        """Return True if container is running, otherwise False."""
        return self.status == self.CONTAINER_STATUS_RUNNING

    def is_terminated(self):
        """Return True if container is terminated, otherwise False."""
        return self.status in [
            self.CONTAINER_STATUS_EXITED,
            self.CONTAINER_STATUS_PAUSED,
        ]

    def is_succeeded(self):
        """Return True if container is succeeded, otherwise False."""
        return (
            self.status == "exited" and self.container.attrs["State"]["ExitCode"] == 0
        )

    def wait_for_ready(self, interval=5):
        """Wait until container enter running state or terminated state."""
        while True:
            status = self.status
            if status == self.CONTAINER_STATUS_RUNNING:
                break
            elif status in [self.CONTAINER_STATUS_EXITED, self.CONTAINER_STATUS_PAUSED]:
                raise RuntimeError(
                    "Container is terminated : id={} status={}".format(
                        self.container.id, self.container.status
                    )
                )
            time.sleep(interval)

    def stop(self):
        if self.is_running():
            self.container.stop()

    def start(self):
        if not self.is_running():
            self.container.start()

    def delete(self):
        if self.is_running():
            self.container.stop()
        self.container.remove()

    def watch(self, show_logs: bool = True):
        """Watch container log and wait for container to exit."""
        if not show_logs:
            self.container.wait()
        else:
            log_iter = self.container.logs(
                stream=True,
                follow=True,
            )
            for log in log_iter:
                print(log.decode())

        self.container.reload()
        exit_code = self.container.attrs["State"]["ExitCode"]
        if exit_code != 0:
            raise RuntimeError(
                "Container run exited failed: exit_code={}".format(exit_code)
            )


def run_container(
    image_uri: str,
    container_name: Optional[str] = None,
    port: Optional[int] = None,
    environment_variables: Optional[Dict[str, str]] = None,
    command: Optional[Union[List[str], str]] = None,
    entry_point: Optional[Union[List[str], str]] = None,
    volumes: Optional[Dict[str, Any]] = None,
    working_dir: Optional[str] = None,
    gpu_count: Optional[int] = None,
    gpu_device_ids: Optional[List[str]] = None,
    gpu_capabilities: Optional[List[List[str]]] = None,
) -> ContainerRun:
    """Run a container in local.

    Args:
        image_uri (str):  A docker image uri.
        container_name (str, optional): Name of the container.
        port (int, optional): The port to expose.
        environment_variables (Dict[str, str], optional): Environment variables to set
            in the container.
        command (Union[List[str], str], optional): Command to run the container.
        entry_point (Union[List[str], str], optional): Entry point to run the container.
        volumes (Dict[str, Any], optional): Volumes to mount in the container.
        working_dir (str, optional): Working directory in the container.
        gpu_count (int, optional): Number of GPU devices to request. Set to -1 to
            request all available devices.
            To use GPU, set either ``gpu_count`` or ``gpu_device_ids``.
        gpu_device_ids (List[str], optional): List of strings for GPU device IDs,
            corresponding to `NVIDIA_VISIBLE_DEVICES` in the NVIDIA Runtime.
            To use GPU, set either ``gpu_count`` or ``gpu_device_ids``.
        gpu_capabilities (List[List[str]], optional): This parameter corresponds to
            `NVIDIA_DRIVER_CAPABILITIES` in the NVIDIA Runtime. The default value is
             ``[["compute", "utility"]]`` if ``gpu_device_ids`` or ``gpu_count`` is set.
             Available capabilities for the NVIDIA driver can be found in
            https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/user-guide.html#driver-capabilities.

    Returns:
        ContainerRun: A ContainerRun object.

    """
    try:
        import docker
    except ImportError:
        raise ImportError("Please install docker first: pip install docker")

    client = docker.from_env()
    # use a random host port.
    host_port = randint(49152, 65535)

    if gpu_count or gpu_device_ids or gpu_capabilities:
        if not gpu_capabilities:
            gpu_capabilities = [["compute", "utility"]]
        device_requests = [
            docker.types.DeviceRequest(
                count=gpu_count,
                device_ids=gpu_device_ids,
                capabilities=gpu_capabilities,
            )
        ]
    else:
        device_requests = []

    container = client.containers.run(
        name=container_name,
        entrypoint=entry_point,
        image=image_uri,
        command=command,
        environment=environment_variables,
        ports={port: host_port} if port else None,
        volumes=volumes,
        working_dir=working_dir,
        detach=True,
        device_requests=device_requests,
    )
    container_run = ContainerRun(
        container=container,
        port=host_port,
    )
    return container_run

from __future__ import absolute_import


import logging
import time
from datetime import datetime

from pai.libs.futures import ThreadPoolExecutor
from pai.decorator import cached_property
from pai.core.exception import TimeoutException, PAIException
from pai.core.artifact import ArchivedArtifact
from pai.core.session import get_default_session, Session
from pai.core.workspace import Workspace

logger = logging.getLogger(__name__)


class PipelineRunStatus(object):
    Initialized = "Initialized"
    ReadyToSchedule = "ReadyToSchedule"
    Starting = "Starting"
    Running = "Running"
    WorkflowServiceStarting = "WorkflowServiceStarting"
    Suspended = "Suspended"
    Succeeded = "Succeeded"
    Terminated = "Terminated"
    Unknown = "Unknown"
    Skipped = "Skipped"
    Failed = "Failed"

    @classmethod
    def is_running(cls, status):
        if status in (
            PipelineRunStatus.Starting,
            PipelineRunStatus.Running,
            PipelineRunStatus.WorkflowServiceStarting,
            PipelineRunStatus.ReadyToSchedule,
        ):
            return True
        return False


class PipelineRun(object):
    def __init__(
        self,
        run_id,
        name,
        workspace_id=None,
        status=None,
        node_id=None,
        duration=None,
        started_at=None,
        finished_at=None,
        source=None,
        user_id=None,
        parent_user_id=None,
    ):
        self.run_id = run_id
        self.name = name
        self.workspace_id = workspace_id
        self.status = status
        self.node_id = node_id
        self.duration = duration
        self.started_at = started_at
        self.finished_at = finished_at
        self.source = source
        self.user_id = user_id
        self.parent_user_id = parent_user_id
        self._bind_session = Session.current()

    @classmethod
    def _get_service_client(cls):
        session = get_default_session()
        return session.paiflow_client

    @cached_property
    def workspace(self):
        return Workspace.get(self.workspace_id) if self.workspace_id else None

    @classmethod
    def get(cls, run_id):
        return next(cls.list(run_id=run_id), None)

    @classmethod
    def list(
        cls,
        name=None,
        run_id=None,
        pipeline_id=None,
        status=None,
        sort_by=None,
        order=None,
        workspace_id=None,
        **kwargs
    ):
        generator = cls._get_service_client().list_run_generator(
            name=name,
            run_id=run_id,
            pipeline_id=pipeline_id,
            status=status,
            sort_by=sort_by,
            order=order,
            workspace_id=workspace_id,
            **kwargs
        )
        for info in generator:
            yield cls.deserialize(info)

    @classmethod
    def deserialize(cls, d):
        return cls(
            run_id=d["RunId"],
            node_id=d["NodeId"],
            name=d["Name"],
            workspace_id=d["WorkspaceId"],
            user_id=d.get("UserId"),
            parent_user_id=d.get("ParentUserId"),
            source=d.get("Source"),
            started_at=d.get("StartedAt"),
            status=d.get("Status"),
        )

    def __repr__(self):
        return "PipelineRun:%s" % self.run_id

    def travel_node_status_info(self, node_id, max_depth=10):
        node_status_info = dict()

        def pipelines_travel(curr_node_id, parent=None, cur_depth=1):
            if cur_depth > max_depth:
                return
            run_node_detail_info = self._get_service_client().get_node(
                self.run_id,
                curr_node_id,
                depth=2,
            )
            if (
                not run_node_detail_info
                or "StartedAt" not in run_node_detail_info["StatusInfo"]
            ):
                return

            if parent is None:
                curr_root_name = self.name
            else:
                curr_root_name = "{0}.{1}".format(
                    run_node_detail_info["Metadata"]["Name"], parent
                )
            node_status_info[curr_root_name] = self._pipeline_node_info(
                run_node_detail_info
            )

            pipelines = run_node_detail_info["Spec"].get("Pipelines", [])
            if not pipelines:
                return
            for sub_pipeline in pipelines:
                node_name = "{0}.{1}".format(
                    curr_root_name, sub_pipeline["Metadata"]["Name"]
                )
                node_status_info[node_name] = self._pipeline_node_info(sub_pipeline)
                next_node_id = sub_pipeline["Metadata"]["NodeId"]
                if sub_pipeline["Metadata"]["NodeType"] == "Dag" and next_node_id:
                    pipelines_travel(next_node_id, curr_root_name, cur_depth + 1)

        pipelines_travel(curr_node_id=node_id)
        return node_status_info

    @staticmethod
    def _pipeline_node_info(pipeline_info):
        return {
            "name": pipeline_info["Metadata"]["Name"],
            "nodeId": pipeline_info["Metadata"]["NodeId"],
            "status": pipeline_info["StatusInfo"]["Status"],
            "startedAt": pipeline_info["StatusInfo"]["StartedAt"],
            "finishedAt": pipeline_info["StatusInfo"].get("FinishedAt", None),
        }

    @property
    def run_detail_url(self):
        return self._bind_session.run_detail_url(run_id=self.run_id)

    def get_run_info(self):
        return self._get_service_client().get_run(self.run_id)

    def get_run_node_detail(self, node_id, depth=2):
        return self._get_service_client().get_node(
            self.run_id, node_id=node_id, depth=depth
        )

    def get_outputs(self, name=None, node_id=None, depth=1, type=None):
        if not node_id:
            run_info = self.get_run_info()
            node_id = run_info["NodeId"]

        if not node_id:
            return
        client = self._bind_session.paiflow_client or type(self)._get_service_client()
        outputs = [
            output
            for output in client.list_node_outputs_generator(
                name=name,
                node_id=node_id,
                run_id=self.run_id,
                depth=depth,
                type=type,
            )
        ]

        logger.info(
            "RunInstance outputs: run_id:%s, node_id:%s, outputs:%s"
            % (self.run_id, node_id, len(outputs))
        )
        return [ArchivedArtifact.deserialize(output) for output in outputs]

    def get_status(self):
        return self.get_run_info()["Status"]

    def start(self):
        return self._get_service_client().start_run(self.run_id)

    def terminate(self):
        return self._get_service_client().terminate_run(self.run_id)

    def _wait_for_init(self, timeout=120, retry_interval=1):
        """Wait for "NodeId" allocated to pipeline run.

        Args:
            timeout: timeout of wait_for_completion time.
        """
        start_time = datetime.now()
        run_info = self.get_run_info()
        while (
            PipelineRunStatus.is_running(run_info["Status"]) and not run_info["NodeId"]
        ):
            time_elapse = datetime.now() - start_time
            if time_elapse.seconds > timeout:
                raise TimeoutException("")
            time.sleep(retry_interval)
            run_info = self.get_run_info()

        if run_info.get("NodeId", None):
            return run_info["NodeId"]
        else:
            raise ValueError("Failed in acquire root node_id of pipeline run.")

    def wait_for_completion(self, show_outputs=True, timeout=None):
        """Wait until the pipeline run stop."""
        start_at = datetime.now()
        run_info = self.get_run_info()
        node_id = run_info["NodeId"]
        if not node_id:
            raise ValueError("Expect NodeId in GetRun response")

        run_status = run_info["Status"]
        if run_status == PipelineRunStatus.Initialized:
            raise ValueError(
                'Pipeline run instance is in status "Init", please start the run instance.'
            )
        elif run_status in (PipelineRunStatus.Terminated, PipelineRunStatus.Suspended):
            raise ValueError(
                "Pipeline run instance is stopped(status:%s), please resume/retry the run."
                % run_status
            )
        elif run_status == PipelineRunStatus.Failed:
            raise ValueError("Pipeline run is failed.")
        elif run_status in (PipelineRunStatus.Skipped, PipelineRunStatus.Unknown):
            raise ValueError(
                "Pipeline run in unexpected status(%s:%s)" % (self.run_id, run_status)
            )
        elif run_status == PipelineRunStatus.Succeeded:
            return

        # Wait for Workflow init.
        print("Wait for run workflow init")

        if show_outputs:
            run_logger = _RunLogger(run_instance=self, node_id=node_id)
        else:
            run_logger = _MockRunLogger(run_instance=self, node_id=node_id)

        try:
            prev_status_infos = {}
            root_node_status = run_status
            log_runners = []
            while PipelineRunStatus.is_running(root_node_status):
                curr_time = datetime.now()
                if timeout and (curr_time - start_at).total_seconds() > timeout:
                    raise TimeoutException("RunInstance wait_for_completion timeout.")
                curr_status_infos = self.travel_node_status_info(node_id)
                for node_fullname, status_info in curr_status_infos.items():
                    if (
                        node_fullname not in prev_status_infos
                        and status_info["status"] != PipelineRunStatus.Skipped
                    ):
                        log_runner = run_logger.submit(
                            node_id=status_info["nodeId"], node_name=node_fullname
                        )
                        if log_runner:
                            log_runners.append(log_runner)
                prev_status_infos = curr_status_infos
                root_node_status = (
                    curr_status_infos[self.name]["status"]
                    if self.name in curr_status_infos
                    else root_node_status
                )

                if root_node_status == PipelineRunStatus.Failed:
                    raise PAIException(
                        "PipelineRun failed: run_id={}, run_status_info={}".format(
                            self.run_id, curr_status_infos
                        )
                    )
                failed_nodes = {
                    name: status_info
                    for name, status_info in curr_status_infos.items()
                    if PipelineRunStatus.Failed == status_info["status"]
                }
                if failed_nodes:
                    raise PAIException(
                        "PipelineRun failed: run_id={}, failed_nodes={}".format(
                            self.run_id, failed_nodes
                        )
                    )

                time.sleep(2)
        except (KeyboardInterrupt, PAIException) as e:
            logger.debug("catch expections, %s", e)
            run_logger.stop_tail()
            raise e

        for log_runner in log_runners:
            _ = log_runner.result()

        return self

    def _wait_with_progress(self):
        pass

    def _wait_with_logger(self, node_id):
        pass

    def _list_node_logs_generator(
        self,
        run_id,
        node_id,
        page_offset=0,
        page_size=100,
    ):
        return self._bind_session.paiflow_client.list_node_logs_generator(
            run_id=run_id,
            node_id=node_id,
            page_offset=page_offset,
            page_size=page_size,
        )


class _RunLogger(object):
    executor = ThreadPoolExecutor(5)

    def __init__(self, run_instance, node_id):
        super(_RunLogger, self).__init__()
        self.run_instance = run_instance
        self.node_id = node_id
        self.running_nodes = set()
        self._tail = True

    def tail(
        self,
        node_id,
        node_name,
        page_size=100,
        page_offset=0,
    ):
        if node_id in self.running_nodes:
            return
        self.running_nodes.add(node_id)

        while True and self._tail:
            logs = self.run_instance._list_node_logs_generator(
                run_id=self.run_instance.run_id,
                node_id=node_id,
                page_size=page_size,
                page_offset=page_offset,
            )

            count = 0
            for log in logs:
                print("%s: %s" % (node_name, log))
                page_offset += 1
                count += 1
                if count % page_size == 0:
                    time.sleep(0.5)

            if count == 0:
                status = self.run_instance.get_status()
                if PipelineRunStatus.is_running(status):
                    time.sleep(2)
                else:
                    break

    def submit(
        self,
        node_id,
        node_name,
        page_size=100,
        page_offset=0,
    ):
        print("Add Node Logger: {}, {}".format(node_name, node_id))
        if node_id in self.running_nodes:
            return
        return self.executor.submit(
            self.tail,
            node_id=node_id,
            node_name=node_name,
            page_size=page_size,
            page_offset=page_offset,
        )

    def stop_tail(self):
        self._tail = False


class _MockRunLogger(object):
    def __init__(self, run_instance, node_id):
        super(_MockRunLogger, self).__init__()
        self.run_instance = run_instance
        self.node_id = node_id

    def tail(self, **kwargs):
        pass

    def submit(self, *args, **kwargs):
        pass

    def stop_tail(self):
        pass

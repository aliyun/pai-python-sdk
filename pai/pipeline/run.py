from __future__ import absolute_import

import logging
import time
from datetime import datetime

from pai.libs.futures import ThreadPoolExecutor
from pai.decorator import cached_property
from pai.core.exception import TimeoutException
from pai.pipeline.types.artifact import ArtifactEntity
from pai.core.session import get_default_session
from pai.core.workspace import Workspace

logger = logging.getLogger(__name__)


class PipelineRunStatus(object):
    Init = "Init"
    Running = "Running"
    Suspended = "Suspended"
    Succeeded = "Succeeded"
    Completed = "Succeeded"
    Terminated = "Terminated"
    Unknown = "Unknown"
    Skipped = "Skipped"
    Failed = "Failed"


class PipelineRun(object):

    def __init__(self, run_id, name, workspace_id=None, pipeline_id=None, session=None):
        self._run_id = run_id
        self._name = name
        self._pipeline_id = pipeline_id
        self._workspace_id = workspace_id
        self._session = session or get_default_session()

    @property
    def run_id(self):
        return self._run_id

    @property
    def name(self):
        return self._name

    @property
    def pipeline_id(self):
        return self._pipeline_id

    @classmethod
    def _get_pipeline_client(cls):
        session = get_default_session()
        return session.paiflow_client

    @cached_property
    def workspace(self):
        return Workspace.get(self._workspace_id) if self._workspace_id else None

    @classmethod
    def list(cls, name=None, run_id=None, pipeline_id=None, status=None, sorted_by=None,
             sorted_sequence=None, workspace=None):
        generator = cls._get_pipeline_client().list_run(name=name, run_id=run_id,
                                                        pipeline_id=pipeline_id,
                                                        status=status, sorted_by=sorted_by,
                                                        sorted_sequence=sorted_sequence,
                                                        workspace_id=workspace.id if workspace else None)
        for info in generator:
            yield cls(
                run_id=info["RunId"],
                name=info["Name"],
                pipeline_id=info["PipelineId"],
                workspace_id=info.get("WorkspaceId", None),
            )

    def __repr__(self):
        return "PipelineRun:%s" % self.run_id

    def travel_node_status_info(self, node_id, depth=10):
        node_status_info = dict()

        def pipelines_travel(curr_node_id, parent=None, cur_depth=1):
            if cur_depth > depth:
                return
            run_node_detail_info = self._session.get_run_detail(self.run_id, curr_node_id)
            if not run_node_detail_info:
                return

            if parent is None:
                curr_root_name = self.name
            else:
                curr_root_name = "{0}.{1}".format(run_node_detail_info["Metadata"]["Name"], parent)
            node_status_info[curr_root_name] = self._pipeline_node_info(run_node_detail_info)
            if run_node_detail_info["Metadata"]["NodeType"] != "Dag":
                return
            for sub_pipeline in run_node_detail_info["Spec"]["Pipelines"]:
                node_name = "{0}.{1}".format(curr_root_name, sub_pipeline["Metadata"]["Name"])
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
            "finishedAt": pipeline_info["StatusInfo"]["FinishedAt"],
        }

    @property
    def run_detail_url(self):
        return self._session.run_detail_url(run_id=self.run_id)

    def get_run_info(self):
        return self._session.get_run(self.run_id)

    def get_run_detail(self, node_id, depth=2):
        return self._session.get_run_detail(self.run_id, node_id=node_id, depth=depth)

    def get_outputs(self, name=None, node_id=None, depth=1, typ=None, page_number=1, page_size=200):
        if not node_id:
            run_info = self.get_run_info()
            node_id = run_info["NodeId"]

        if not node_id:
            return
        outputs = self._session.list_run_outputs(run_id=self.run_id, node_id=node_id, depth=depth,
                                                 name=name, typ=typ, page_number=page_number,
                                                 page_size=page_size)

        logger.info("RunInstance outputs: run_id:%s, node_id:%s, outputs:%s" % (
            self.run_id, node_id, outputs))
        return [ArtifactEntity.from_run_output(output) for output in outputs]

    def get_status(self):
        return self.get_run_info()["Status"]

    def start(self):
        return self._session.start_run(self.run_id)

    def terminate(self):
        return self._session.terminate_run(self.run_id)

    def suspend(self):
        return self._session.suspend_run(self.run_id)

    def resume(self):
        return self._session.resume_run(self.run_id)

    def retry(self):
        return self._session.retry_run(self.run_id)

    def get_node_log(self, node_id, pending=False, page_size=100, page_offset=0, from_time=None,
                     to_time=None):
        while True:
            logs = self._session.get_run_log(self.run_id, node_id, from_time=from_time,
                                             to_time=to_time,
                                             page_size=page_size, page_offset=page_offset)

            if logs:
                for log in logs:
                    yield log
                time.sleep(0.2)
                page_offset += page_size
            elif not pending:
                raise StopIteration
            else:
                status = self.get_status()
                if status == PipelineRunStatus.Running:
                    time.sleep(1)
                else:
                    raise StopIteration

    def _wait_for_init(self, timeout=120, retry_interval=1):
        """Wait for "NodeId" allocated to pipeline run.

        Args:
            timeout: timeout of wait_for_completion time.
        """
        start_time = datetime.now()
        run_info = self.get_run_info()
        while run_info["Status"] == PipelineRunStatus.Running and not run_info["NodeId"]:
            run_info = self.get_run_info()
            time_elapse = datetime.now() - start_time
            if time_elapse.seconds > timeout:
                raise TimeoutException("")
            time.sleep(retry_interval)

        if run_info.get("NodeId", None):
            return run_info["NodeId"]
        else:
            raise ValueError("Failed in acquire root node_id of pipeline run.")

    def wait_for_completion(self, show_outputs=True, timeout=None):
        """Wait until the pipeline run stop."""
        start_at = datetime.now()
        run_info = self.get_run_info()
        run_status = run_info["Status"]
        if run_status == PipelineRunStatus.Init:
            raise ValueError(
                'Pipeline run instance is in status "Init", please start the run instance.')
        elif run_status in (PipelineRunStatus.Terminated, PipelineRunStatus.Suspended):
            raise ValueError(
                "Pipeline run instance is stopped(status:%s), please resume/retry the run."
                % run_status)
        elif run_status == PipelineRunStatus.Failed:
            raise ValueError("Pipeline run is failed.")
        elif run_status in (PipelineRunStatus.Skipped, PipelineRunStatus.Unknown):
            raise ValueError("Pipeline run in unexpected status(%s:%s)" % (self.run_id, run_status))
        elif run_status == PipelineRunStatus.Succeeded:
            return

        # Wait for Workflow init.
        print("Wait for run workflow init")
        node_id = self._wait_for_init()

        if show_outputs:
            run_logger = _RunLogger(run_instance=self, node_id=node_id)
        else:
            run_logger = _MockRunLogger(run_instance=self, node_id=node_id)

        prev_status_infos = {}
        root_node_status = run_status
        while root_node_status == PipelineRunStatus.Running:
            curr_time = datetime.now()
            if timeout and (curr_time - start_at).total_seconds() > timeout:
                raise TimeoutException("RunInstance wait_for_completion timeout.")
            curr_status_infos = self.travel_node_status_info(node_id)
            for node_fullname, status_info in curr_status_infos.items():
                if node_fullname not in prev_status_infos and \
                        status_info["status"] != PipelineRunStatus.Skipped:
                    run_logger.submit(node_id=status_info["nodeId"], node_name=node_fullname)
            prev_status_infos = curr_status_infos
            root_node_status = prev_status_infos[self.name][
                "status"] if self.name in prev_status_infos else root_node_status
            time.sleep(2)

        return self

    def _wait_with_progress(self):
        pass

    def _wait_with_logger(self, node_id):
        pass


class _RunLogger(object):
    executor = ThreadPoolExecutor(5)

    def __init__(self, run_instance, node_id):
        super(_RunLogger, self).__init__()
        self.run_instance = run_instance
        self.node_id = node_id
        self.running_nodes = set()
        self._tail = True

    def tail(self, node_id, node_name, from_time=None, to_time=None, page_size=100, page_offset=0):
        if node_id in self.running_nodes:
            return
        self.running_nodes.add(node_id)
        session = self.run_instance._session
        run_id = self.run_instance.run_id

        while True and self._tail:
            logs = session.get_run_log(run_id, node_id, from_time=from_time, to_time=to_time,
                                       page_size=page_size, page_offset=page_offset)
            if logs:
                for log in logs:
                    print("%s: %s" % (node_name, log))
                time.sleep(0.2)
                page_offset += page_size
            else:
                status = self.run_instance.get_status()
                if status == PipelineRunStatus.Running:
                    time.sleep(2)
                else:
                    break

    def submit(self, node_id, node_name, from_time=None, to_time=None, page_size=100,
               page_offset=0):
        self.executor.submit(self.tail, node_id=node_id, node_name=node_name, from_time=from_time,
                             to_time=to_time, page_size=page_size, page_offset=page_offset)

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

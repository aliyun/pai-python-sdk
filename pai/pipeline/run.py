import time
from datetime import datetime

from libs.futures import ThreadPoolExecutor
from pai.exception import TimeoutException
from pai.utils import run_detail_url

RunStatusInit = "Init"
RunStatusRunning = "Running"
RunStatusSuspended = "Suspended"
RunStatusSucceeded = "Succeeded"
RunStatusTerminated = "Terminated"
RunStatusUnknown = "Unknown"
RunStatusSkipped = "Skipped"
RunStatusFailed = "Failed"


class RunInstance(object):

    def __init__(self, run_id, session=None):
        self.run_id = run_id
        self.session = session

    def _prepare(self):
        run_info = self.session.get_run(self.run_id)
        node_id = run_info["NodeId"]
        self.root_node_id = node_id
        run_detail = self.session.get_run_detail(self.run_id, self.root_node_id)
        self.root_node_name = run_detail["Metadata"]["Name"]

    def travel_node_status_info(self, node_id, depth=10):
        node_status_info = dict()

        def pipelines_travel(curr_node_id, parent=None, cur_depth=1):
            if cur_depth > depth:
                return
            run_node_detail = self.session.get_run_detail(self.run_id, curr_node_id)
            if parent is None:
                curr_root_name = self.run_id
            else:
                curr_root_name = "{0}.{1}".format(run_node_detail["Metadata"]["Name"], parent)
            node_status_info[curr_root_name] = self._pipeline_node_info(run_node_detail)
            if run_node_detail["Metadata"]["NodeType"] != "Dag":
                return
            for sub_pipeline in run_node_detail["Spec"]["Pipelines"]:
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
    def run_detail_web_url(self):
        return run_detail_url(self.run_id, self.session.region_id)

    def is_root_node(self, node_id, node_name):
        return node_id == self.root_node_id or node_name == self.root_node_name

    def get_run_info(self):
        return self.session.get_run(self.run_id)

    def get_run_detail(self, node_id):
        return self.session.get_run_detail(self.run_id, node_id=node_id)

    def get_status(self):
        return self.get_run_info()["Status"]

    def start(self):
        return self.session.start_run(self.run_id)

    def terminate(self):
        return self.session.terminate_run(self.run_id)

    def suspend(self):
        return self.session.suspend_run(self.run_id)

    def resume(self):
        return self.session.resume_run(self.run_id)

    def retry(self):
        return self.session.retry_run(self.run_id)

    def get_node_log(self, node_id, pending=False, page_size=100, page_offset=0, from_time=None, to_time=None):
        while True:
            logs = self.session.get_run_log(self.run_id, node_id, from_time=from_time, to_time=to_time,
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
                if status == RunStatusRunning:
                    time.sleep(1)
                else:
                    raise StopIteration

    def _wait_for_node_id(self, timeout=120):
        """Wait for "NodeId" allocated to pipeline run.

        Args:
            timeout: timeout of wait time.
        """
        start_time = datetime.now()
        run_info = self.get_run_info()
        while run_info["Status"] == "Running" and run_info["NodeId"] is None:
            run_info = self.get_run_info()
            time_elapse = datetime.now() - start_time
            if time_elapse.seconds > timeout:
                raise TimeoutException("")
            time.sleep(1)

        if run_info["NodeId"] is not None:
            return run_info["NodeId"]
        else:
            raise ValueError("Failed in acquire root node_id of pipeline run.")

    def wait(self):
        """Wait until the pipeline run stop.

        Args:
            with_log:
        """
        run_info = self.get_run_info()
        run_status = run_info["Status"]
        if run_status == RunStatusInit:
            raise ValueError('Pipeline run instance is in status "Init", please start the run instance.')
        elif run_status in (RunStatusTerminated, RunStatusSuspended):
            raise ValueError("Pipeline run instance is stopped(status:%s), please resume/retry the run." % run_status)
        elif run_status == RunStatusFailed:
            raise ValueError("Pipeline run is failed.")
        elif run_status in (RunStatusSkipped, RunStatusUnknown):
            raise ValueError("Pipeline run in unexpected status(%s:%s)" % (self.run_id, run_status))
        elif run_status == RunStatusSucceeded:
            return

        # run status is Running.
        node_id = run_info.get("NodeId")
        if node_id is None:
            node_id = self._wait_for_node_id()
        assert node_id is not None

        run_logger = RunLogger(run_instance=self, node_id=node_id)
        run_logger.submit(node_id=node_id, node_name=self.run_id)
        node_status_infos = self.travel_node_status_info(node_id)

        running_node = {node_fullname: status_info for node_fullname, status_info in node_status_infos.items()
                        if status_info["status"] == RunStatusRunning}

        for node_fullname, status_info in running_node.items():
            run_logger.submit(node_id=status_info["nodeId"], node_name=node_fullname)

        prev_status_infos = node_status_infos
        root_node_status = prev_status_infos[self.run_id]["status"]

        print("%s root_node_status is: %s" % (time.time(), root_node_status))

        while root_node_status == RunStatusRunning:
            time.sleep(5)
            print("root_node_status is", root_node_status)
            curr_status_infos = self.travel_node_status_info(node_id)

            for node in curr_status_infos:
                if node not in prev_status_infos and curr_status_infos[node]["status"] != RunStatusSkipped:
                    run_logger.submit(node_id=curr_status_infos[node]["nodeId"], node_name=node)
            prev_status_infos = curr_status_infos
            root_node_status = prev_status_infos[self.run_id]["status"]

        print("Run Status: %s" % root_node_status)

    def _wait_with_progress(self):
        pass

    def _wait_with_logger(self, node_id):
        pass


class RunLogger(object):
    executor = ThreadPoolExecutor(5)

    def __init__(self, run_instance, node_id):
        super(RunLogger, self).__init__()
        self.run_instance = run_instance
        self.node_id = node_id
        self.running_nodes = set()
        self._tail = True

    def tail(self, node_id, node_name, from_time=None, to_time=None, page_size=100, page_offset=0):
        if node_id in self.running_nodes:
            return
        self.running_nodes.add(node_id)
        session = self.run_instance.session
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
                if status == RunStatusRunning:
                    time.sleep(2)
                else:
                    break

    def submit(self, node_id, node_name, from_time=None, to_time=None, page_size=100, page_offset=0):
        self.executor.submit(self.tail, node_id=node_id, node_name=node_name, from_time=from_time,
                             to_time=to_time, page_size=page_size, page_offset=page_offset)

    def stop_tail(self):
        self._tail = False

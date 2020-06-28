class RunInstance(object):

    def __init__(self, run_id, session=None):
        self.run_id = run_id
        self.session = session

    def get_run_info(self):
        return self.session.get_pipeline_run(self.run_id)

    def get_status(self):
        return self.get_run_info()["status"]

    def start(self):
        return self.session.start_pipeline_run(self.run_id)

    def terminate(self):
        return self.session.terminate_pipeline_run(self.run_id)

    def suspend(self):
        return self.session.suspend_pipeline_run(self.run_id)

    def resume(self):
        return self.session.resume_pipeline_run(self.run_id)

    def retry(self):
        return self.session.retry_pipeline_run(self.run_id)

    def wait(self):
        """Wait until the pipeline run stop."""
        pass

    def tail_log(self, node_token):
        pass

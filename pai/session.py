from __future__ import absolute_import

from pprint import pprint

import yaml
from aliyunsdkcore.client import AcsClient

from pai.api.client_factory import ClientFactory
from pai.utils import md5_digest, run_detail_url


class Session(object):

    def __init__(self, access_key, access_secret, region_id):
        """ Construct session object with Alibaba Cloud account credential

        Args:
            access_key:
            access_secret:
            region_id:
        """

        if not access_key or not access_secret or not region_id:
            raise ValueError("Please provide access_key, access_secret and region")

        self.region_id = region_id
        self._initialize(access_key, access_secret, region_id)

    def _initialize(self, access_key, access_secret, region):
        self._acs_client = AcsClient(ak=access_key, secret=access_secret, region_id=region)
        self.paiflow_client = ClientFactory.create_paiflow_client(self._acs_client)
        self.sts_client = ClientFactory.create_sts_client(self._acs_client)

    @property
    def account_id(self):
        if not hasattr(self, "_account_id"):
            caller_identity = self.sts_client.get_caller_identity()
            self._account_id = int(caller_identity["AccountId"])
        return self._account_id

    def get_pipeline(self, identifier, provider, version):
        resp = self.paiflow_client.list_pipeline(identifier=identifier, provider=provider,
                                                 version=version)
        if len(resp["Data"]) == 0:
            return

        pipeline_id = resp["Data"][0]["PipelineId"]
        return self.paiflow_client.get_pipeline(pipeline_id)["Data"]

    def get_pipeline_by_id(self, pipeline_id):
        return self.paiflow_client.get_pipeline(pipeline_id)["Data"]

    def list_pipeline(self, page_num=1, page_size=50, source_type='private'):
        return self.paiflow_client.list_pipeline(
            source_type=source_type,
            page_num=page_num,
            page_size=page_size,
        )

    def search_pipeline(self, identifier=None, provider=None, query=None, source_type='private',
                        version=None, page_num=1, page_size=50):
        return self.paiflow_client.list_pipeline(
            identifier=identifier,
            provider=provider,
            query=query,
            source_type=source_type,
            version=version,
            page_num=page_num,
            page_size=page_size,
        )

    def create_pipeline(self, pipeline_def):
        """
        create_pipeline submit `pipeline_manifest` to pipeline service and store. Identifier-provider-version
         is unique key. The same triple combination will result overwrite.

        Args:
            identifier: pipeline identifier.
            version: version of submitted pipeline, md5 value of yaml definition is used as default.
            pipeline_def: pipeline definition manifest.

        Returns:
            pipeline_id
        """

        # pipeline_def['metadata'] = {
        #     'identifier': identifier,
        #     'provider': self.account_id,
        #     'version': version,
        # }
        pipeline_def = yaml.dump(pipeline_def)
        # if version is None:
        #     pipeline_def['metadata']['version'] = md5_digest(pipeline_def)

        resp = self.paiflow_client.create_pipeline(manifest=pipeline_def)
        return resp["Data"]["PipelineId"]

    def describe_pipeline(self, pipeline_id):
        return self.paiflow_client.describe_pipeline(pipeline_id)

    def update_pipeline_privilege(self, pipeline_id, user_ids):
        return self.paiflow_client.update_pipeline_privilege(pipeline_id, user_ids)["Data"]

    def list_pipeline_privilege(self, pipeline_id):
        return self.paiflow_client.list_pipeline_privilege(pipeline_id)["Data"]

    def create_pipeline_run(self, name, arguments, env=None, pipeline_id=None, manifest=None,
                            no_confirm_required=True):
        arguments = {
            "arguments": arguments,
            "env": env
        }
        resp = self.paiflow_client.create_run(name, arguments, pipeline_id=pipeline_id, manifest=manifest,
                                              no_confirm_required=no_confirm_required)
        run_id = resp["Data"]["RunId"]

        print("Create pipeline run success (run_id: {run_id}), please visit the link below to view"
              " the run detail.".format(run_id=run_id))
        print(run_detail_url(run_id, self.region_id))

        return run_id

    def list_pipeline_run(self, name=None, run_id=None, pipeline_id=None, status=None,
                          sorted_by=None, sorted_sequences=None, page_num=1, page_size=50):
        kwargs = locals()
        kwargs.pop("self")
        run_infos = self.paiflow_client.list_run(**kwargs)
        return run_infos

    def get_run_detail(self, run_id, node_id, depth=2):
        run_info = self.paiflow_client.get_run_detail(run_id, node_id, depth=depth)
        return run_info["Data"]

    def get_run_log(self, run_id, node_id, from_time=None, to_time=None,
                    keyword=None, reverse=False, page_offset=0, page_size=100):
        kwargs = locals()
        kwargs.pop("self")
        logs = self.paiflow_client.list_node_log(**kwargs)
        return logs["Data"]

    def list_run_output(self, run_id, node_id, depth=2, name=None, sorted_by=None,
                        sorted_sequence=None, typ=None, page_number=1, page_size=50):
        kwargs = locals()
        kwargs.pop("self")
        outputs = self.paiflow_client.list_run_output(**kwargs)
        return outputs

    def get_run(self, run_id):
        run_info = self.paiflow_client.get_run(run_id)
        return run_info["Data"]

    def terminate_run(self, run_id):
        resp = self.paiflow_client.terminate_run(run_id)
        return resp["Data"]["runId"] == run_id

    def suspend_run(self, run_id):
        resp = self.paiflow_client.suspend_run(run_id)
        return resp["Data"]["runId"] == run_id

    def retry_run(self, run_id):
        resp = self.paiflow_client.retry_run(run_id)
        return resp["Data"]["runId"] == run_id

    def resume_run(self, run_id):
        resp = self.paiflow_client.retry_run(run_id)
        return resp["Data"]["runId"] == run_id

    def start_run(self, run_id):
        resp = self.paiflow_client.retry_run(run_id)
        return resp["Data"]["runId"] == run_id

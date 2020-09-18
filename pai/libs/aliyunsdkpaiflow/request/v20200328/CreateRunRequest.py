# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RoaRequest

class CreateRunRequest(RoaRequest):

	def __init__(self):
		RoaRequest.__init__(self, 'PAIFlow', '2020-03-28', 'CreateRun')
		self.set_uri_pattern('/api/core/v1.0/runs')
		self.set_method('POST')

	def get_PipelineManifest(self):
		return self.get_body_params().get('PipelineManifest')

	def set_PipelineManifest(self,PipelineManifest):
		self.add_body_params('PipelineManifest', PipelineManifest)

	def get_NoConfirmRequired(self):
		return self.get_body_params().get('NoConfirmRequired')

	def set_NoConfirmRequired(self,NoConfirmRequired):
		self.add_body_params('NoConfirmRequired', NoConfirmRequired)

	def get_Name(self):
		return self.get_body_params().get('Name')

	def set_Name(self,Name):
		self.add_body_params('Name', Name)

	def get_Arguments(self):
		return self.get_body_params().get('Arguments')

	def set_Arguments(self,Arguments):
		self.add_body_params('Arguments', Arguments)

	def get_PipelineId(self):
		return self.get_body_params().get('PipelineId')

	def set_PipelineId(self,PipelineId):
		self.add_body_params('PipelineId', PipelineId)

	def get_WorkspaceId(self):
		return self.get_body_params().get('WorkspaceId')

	def set_WorkspaceId(self,WorkspaceId):
		self.add_body_params('WorkspaceId', WorkspaceId)
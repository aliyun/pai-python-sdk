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

class GetPipelineRequest(RoaRequest):

	def __init__(self):
		RoaRequest.__init__(self, 'PAIFlow', '2020-03-28', 'GetPipeline')
		self.set_uri_pattern('/api/core/v1.0/pipelines/overview')
		self.set_method('GET')

	def get_PipelineProvider(self):
		return self.get_query_params().get('PipelineProvider')

	def set_PipelineProvider(self,PipelineProvider):
		self.add_query_param('PipelineProvider',PipelineProvider)

	def get_PipelineVersion(self):
		return self.get_query_params().get('PipelineVersion')

	def set_PipelineVersion(self,PipelineVersion):
		self.add_query_param('PipelineVersion',PipelineVersion)

	def get_PipelineIdentifier(self):
		return self.get_query_params().get('PipelineIdentifier')

	def set_PipelineIdentifier(self,PipelineIdentifier):
		self.add_query_param('PipelineIdentifier',PipelineIdentifier)

	def get_PipelineId(self):
		return self.get_query_params().get('PipelineId')

	def set_PipelineId(self,PipelineId):
		self.add_query_param('PipelineId',PipelineId)
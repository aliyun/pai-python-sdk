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

class ListPipelinesRequest(RoaRequest):

	def __init__(self):
		RoaRequest.__init__(self, 'PAIFlow', '2020-03-28', 'ListPipelines')
		self.set_uri_pattern('/api/core/v1.0/pipelines')
		self.set_method('GET')

	def get_PageSize(self):
		return self.get_query_params().get('PageSize')

	def set_PageSize(self,PageSize):
		self.add_query_param('PageSize',PageSize)

	def get_PipelineProvider(self):
		return self.get_query_params().get('PipelineProvider')

	def set_PipelineProvider(self,PipelineProvider):
		self.add_query_param('PipelineProvider',PipelineProvider)

	def get_FuzzyMatching(self):
		return self.get_query_params().get('FuzzyMatching')

	def set_FuzzyMatching(self,FuzzyMatching):
		self.add_query_param('FuzzyMatching',FuzzyMatching)

	def get_PipelineVersion(self):
		return self.get_query_params().get('PipelineVersion')

	def set_PipelineVersion(self,PipelineVersion):
		self.add_query_param('PipelineVersion',PipelineVersion)

	def get_PipelineIdentifier(self):
		return self.get_query_params().get('PipelineIdentifier')

	def set_PipelineIdentifier(self,PipelineIdentifier):
		self.add_query_param('PipelineIdentifier',PipelineIdentifier)

	def get_PageNumber(self):
		return self.get_query_params().get('PageNumber')

	def set_PageNumber(self,PageNumber):
		self.add_query_param('PageNumber',PageNumber)

	def get_WorkspaceId(self):
		return self.get_query_params().get('WorkspaceId')

	def set_WorkspaceId(self,WorkspaceId):
		self.add_query_param('WorkspaceId',WorkspaceId)
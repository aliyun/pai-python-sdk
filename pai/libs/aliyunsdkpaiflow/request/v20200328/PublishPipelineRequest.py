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

class PublishPipelineRequest(RoaRequest):

	def __init__(self):
		RoaRequest.__init__(self, 'PAIFlow', '2020-03-28', 'PublishPipeline')
		self.set_uri_pattern('/api/core/v1.0/pipelines/publication')
		self.set_method('PUT')

	def get_SrcPipelineVersion(self):
		return self.get_body_params().get('SrcPipelineVersion')

	def set_SrcPipelineVersion(self,SrcPipelineVersion):
		self.add_body_params('SrcPipelineVersion', SrcPipelineVersion)

	def get_SrcPipelineId(self):
		return self.get_body_params().get('SrcPipelineId')

	def set_SrcPipelineId(self,SrcPipelineId):
		self.add_body_params('SrcPipelineId', SrcPipelineId)

	def get_SrcPipelineProvider(self):
		return self.get_body_params().get('SrcPipelineProvider')

	def set_SrcPipelineProvider(self,SrcPipelineProvider):
		self.add_body_params('SrcPipelineProvider', SrcPipelineProvider)

	def get_SrcPipelineIdentifier(self):
		return self.get_body_params().get('SrcPipelineIdentifier')

	def set_SrcPipelineIdentifier(self,SrcPipelineIdentifier):
		self.add_body_params('SrcPipelineIdentifier', SrcPipelineIdentifier)

	def get_TgtPipelineProvider(self):
		return self.get_body_params().get('TgtPipelineProvider')

	def set_TgtPipelineProvider(self,TgtPipelineProvider):
		self.add_body_params('TgtPipelineProvider', TgtPipelineProvider)
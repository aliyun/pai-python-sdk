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

class UpdateResourceGroupRequest(RoaRequest):

	def __init__(self):
		RoaRequest.__init__(self, 'AIWorkSpace', '2020-08-14', 'UpdateResourceGroup')
		self.set_uri_pattern('/api/core/v1.0/workspaces/[WorkspaceId]/resources/[ResourceName]/resourceInstances/[ResourceInstanceId]/resourceGroups')
		self.set_method('PUT')

	def get_ResourceGroupName(self):
		return self.get_body_params().get('ResourceGroupName')

	def set_ResourceGroupName(self,ResourceGroupName):
		self.add_body_params('ResourceGroupName', ResourceGroupName)

	def get_ResourceInstanceId(self):
		return self.get_path_params().get('ResourceInstanceId')

	def set_ResourceInstanceId(self,ResourceInstanceId):
		self.add_path_param('ResourceInstanceId',ResourceInstanceId)

	def get_ResourceGroupProductType(self):
		return self.get_body_params().get('ResourceGroupProductType')

	def set_ResourceGroupProductType(self,ResourceGroupProductType):
		self.add_body_params('ResourceGroupProductType', ResourceGroupProductType)

	def get_ResourceName(self):
		return self.get_path_params().get('ResourceName')

	def set_ResourceName(self,ResourceName):
		self.add_path_param('ResourceName',ResourceName)

	def get_CommodityCode(self):
		return self.get_body_params().get('CommodityCode')

	def set_CommodityCode(self,CommodityCode):
		self.add_body_params('CommodityCode', CommodityCode)

	def get_WorkspaceId(self):
		return self.get_path_params().get('WorkspaceId')

	def set_WorkspaceId(self,WorkspaceId):
		self.add_path_param('WorkspaceId',WorkspaceId)

	def get_ResourceGroupMode(self):
		return self.get_body_params().get('ResourceGroupMode')

	def set_ResourceGroupMode(self,ResourceGroupMode):
		self.add_body_params('ResourceGroupMode', ResourceGroupMode)
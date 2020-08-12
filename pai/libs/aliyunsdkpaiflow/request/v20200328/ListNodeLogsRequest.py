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

class ListNodeLogsRequest(RoaRequest):

	def __init__(self):
		RoaRequest.__init__(self, 'PAIFlow', '2020-03-28', 'ListNodeLogs')
		self.set_uri_pattern('/api/core/v1.0/runs/[RunId]/nodes/[NodeId]/logs')
		self.set_method('GET')

	def get_PageOffset(self):
		return self.get_query_params().get('PageOffset')

	def set_PageOffset(self,PageOffset):
		self.add_query_param('PageOffset',PageOffset)

	def get_PageSize(self):
		return self.get_query_params().get('PageSize')

	def set_PageSize(self,PageSize):
		self.add_query_param('PageSize',PageSize)

	def get_FromTimeInSeconds(self):
		return self.get_query_params().get('FromTimeInSeconds')

	def set_FromTimeInSeconds(self,FromTimeInSeconds):
		self.add_query_param('FromTimeInSeconds',FromTimeInSeconds)

	def get_RunId(self):
		return self.get_path_params().get('RunId')

	def set_RunId(self,RunId):
		self.add_path_param('RunId',RunId)

	def get_Keyword(self):
		return self.get_query_params().get('Keyword')

	def set_Keyword(self,Keyword):
		self.add_query_param('Keyword',Keyword)

	def get_Reverse(self):
		return self.get_query_params().get('Reverse')

	def set_Reverse(self,Reverse):
		self.add_query_param('Reverse',Reverse)

	def get_NodeId(self):
		return self.get_path_params().get('NodeId')

	def set_NodeId(self,NodeId):
		self.add_path_param('NodeId',NodeId)

	def get_ToTimeInSeconds(self):
		return self.get_query_params().get('ToTimeInSeconds')

	def set_ToTimeInSeconds(self,ToTimeInSeconds):
		self.add_query_param('ToTimeInSeconds',ToTimeInSeconds)
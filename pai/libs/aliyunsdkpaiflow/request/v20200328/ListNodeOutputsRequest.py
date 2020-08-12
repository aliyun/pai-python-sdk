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

class ListNodeOutputsRequest(RoaRequest):

	def __init__(self):
		RoaRequest.__init__(self, 'PAIFlow', '2020-03-28', 'ListNodeOutputs')
		self.set_uri_pattern('/api/core/v1.0/runs/[RunId]/nodes/[NodeId]/outputs')
		self.set_method('GET')

	def get_SortedBy(self):
		return self.get_query_params().get('SortedBy')

	def set_SortedBy(self,SortedBy):
		self.add_query_param('SortedBy',SortedBy)

	def get_Depth(self):
		return self.get_query_params().get('Depth')

	def set_Depth(self,Depth):
		self.add_query_param('Depth',Depth)

	def get_PageSize(self):
		return self.get_query_params().get('PageSize')

	def set_PageSize(self,PageSize):
		self.add_query_param('PageSize',PageSize)

	def get_Name(self):
		return self.get_query_params().get('Name')

	def set_Name(self,Name):
		self.add_query_param('Name',Name)

	def get_RunId(self):
		return self.get_path_params().get('RunId')

	def set_RunId(self,RunId):
		self.add_path_param('RunId',RunId)

	def get_Type(self):
		return self.get_query_params().get('Type')

	def set_Type(self,Type):
		self.add_query_param('Type',Type)

	def get_NodeId(self):
		return self.get_path_params().get('NodeId')

	def set_NodeId(self,NodeId):
		self.add_path_param('NodeId',NodeId)

	def get_SortedSequence(self):
		return self.get_query_params().get('SortedSequence')

	def set_SortedSequence(self,SortedSequence):
		self.add_query_param('SortedSequence',SortedSequence)

	def get_PageNumber(self):
		return self.get_query_params().get('PageNumber')

	def set_PageNumber(self,PageNumber):
		self.add_query_param('PageNumber',PageNumber)
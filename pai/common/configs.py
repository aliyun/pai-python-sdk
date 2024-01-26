#  Copyright 2024 Alibaba, Inc. or its affiliates.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from typing import List, Optional


class UserVpcConfig(object):
    """UserVpcConfig is used to give training job access to resources in your VPC."""

    def __init__(
        self,
        vpc_id: str,
        security_group_id: str,
        switch_id: Optional[str] = None,
        extended_cidrs: List[str] = None,
    ):
        """Initialize UserVpcConfig.

        Args:
            vpc_id (str): Specifies the ID of the VPC that training job instance
                connects to.
            security_group_id (str): The ID of the security group that training job
                instances belong to.
            switch_id (str, optional): The ID of the vSwitch to which the instance
                belongs. Defaults to None.
            extended_cidrs (List[str], optional): The CIDR blocks configured for the
                ENI of the training job instance. If it is not specified, the CIDR block
                will be configured as the same as the VPC network segmentation, which
                means that the training job instance can access all resources in the
                VPC. Defaults to None.
        """

        self.vpc_id = vpc_id
        self.security_group_id = security_group_id
        self.switch_id = switch_id
        self.extended_cidrs = extended_cidrs

    def to_dict(self):
        return {
            "VpcId": self.vpc_id,
            "SecurityGroupId": self.security_group_id,
            "SwitchId": self.switch_id,
            "ExtendedCIDRs": self.extended_cidrs,
        }

#  Copyright 2023 Alibaba, Inc. or its affiliates.
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
from dataclasses import dataclass
from typing import Dict, List, Optional

from ..common.logging import get_logger
from ..libs.alibabacloud_aiworkspace20210204.models import (
    LineageEntity,
    RegisterLineageRequest,
)
from .base import ServiceName, WorkspaceScopedResourceAPI

logger = get_logger(__name__)


@dataclass
class _LineageEntity:
    Attributes: Dict[str, str] = None
    EntityType: Optional[str] = None
    Name: Optional[str] = None
    QualifiedName: Optional[str] = None


class LineageAPI(WorkspaceScopedResourceAPI):
    BACKEND_SERVICE_NAME = ServiceName.PAI_WORKSPACE

    _register_lineage = "register_lineage_with_options"

    def log_lineage(
        self,
        inputs: List[_LineageEntity],
        outputs: List[_LineageEntity],
        job_id: str,
        workspace_id: str,
    ):
        input_entities = []
        output_entities = []
        for input in inputs:
            input_entities.append(
                LineageEntity(
                    attributes=input.Attributes,
                    entity_type=input.EntityType,
                    name=input.Name,
                    qualified_name=input.QualifiedName,
                )
            )
        for output in outputs:
            output_entities.append(
                LineageEntity(
                    attributes=output.Attributes,
                    entity_type=output.EntityType,
                    name=output.Name,
                    qualified_name=output.QualifiedName,
                )
            )
        request = RegisterLineageRequest(
            register_task_as_entity=True,
            input_entities=input_entities,
            output_entities=output_entities,
            qualified_name="pai_dlcjob-task." + job_id,
            name=job_id,
            attributes={"WorkspaceId": workspace_id},
        )
        response = self._do_request(method_=self._register_lineage, request=request)
        logger.debug(response)

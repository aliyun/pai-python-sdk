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

from typing import Any, Dict, List, Optional

from .common import ProviderAlibabaPAI
from .common.logging import get_logger
from .common.utils import make_list_resource_iterator
from .session import Session, get_default_session

logger = get_logger(__name__)


def list_common_datasets(
    name: str = None,
    session: Optional[Session] = None,
) -> List[Dict[str, Any]]:
    session = session or get_default_session()

    gen = make_list_resource_iterator(
        session.dataset_api.list,
        name=name,
        provider=ProviderAlibabaPAI,
        # set the workspace_id manually, prevent using the default workspace of the
        # session.
        workspace_id=0,
        order="DESC",
    )

    return gen

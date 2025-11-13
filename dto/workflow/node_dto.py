from typing import Any, Dict, List

from pydantic import BaseModel, ConfigDict

from helpers.node.node_templates.node_template_types import (
    NodeTypeCategory,
    NodeTypeDefinition,
)
from helpers.utils import req_res_examples as examples


class NodeStatusResponse(BaseModel):
    """노드 상태 응답"""

    model_config = ConfigDict(
        json_schema_extra={"example": examples.EXAMPLE_NODE_STATUS_RESPONSE}  # type: ignore
    )

    node_id: str
    status: str
    progress: float | None = None
    result: Dict[str, Any] | None = None
    error: str | None = None
    started_at: str | None = None
    completed_at: str | None = None


class NodeTypeResponse(BaseModel):
    category: Dict[NodeTypeCategory, List[NodeTypeDefinition]]

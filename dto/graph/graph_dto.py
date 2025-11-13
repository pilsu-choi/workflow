from typing import Any, Dict

from pydantic import BaseModel, ConfigDict, Field

from helpers.utils import req_res_examples as examples


class GraphDetailResponse(BaseModel):
    """그래프 상세 정보 응답"""

    model_config = ConfigDict(
        json_schema_extra={"example": examples.EXAMPLE_GRAPH_DETAIL_RESPONSE}  # type: ignore
    )

    id: int
    name: str
    description: str | None = None
    properties: Dict[str, Any] = Field(
        default={}, examples=[examples.EXAMPLE_GRAPH_PROPERTIES]
    )
    created_at: str | None = None
    updated_at: str | None = None


class GraphMetadataResponse(BaseModel):
    """그래프 메타데이터 응답"""

    model_config = ConfigDict(
        json_schema_extra={"example": examples.EXAMPLE_GRAPH_METADATA_RESPONSE}  # type: ignore
    )

    id: int
    name: str
    description: str | None = None
    properties: Dict[str, Any] = Field(
        default={}, examples=[examples.EXAMPLE_GRAPH_PROPERTIES]
    )
    created_at: str | None = None
    updated_at: str | None = None

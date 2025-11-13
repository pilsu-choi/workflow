from typing import Any, Dict

from pydantic import BaseModel, ConfigDict, Field

from helpers.utils import req_res_examples as examples


class VertexCreateRequest(BaseModel):
    """Vertex 생성 요청 DTO"""

    model_config = ConfigDict(
        json_schema_extra={"example": examples.EXAMPLE_VERTEX_CREATE_REQUEST}  # type: ignore
    )

    id: int | None = None  # 클라이언트 측 임시 ID (업데이트 시 매핑용)
    type: str
    properties: Dict[str, Any] = Field(
        default={}, examples=[examples.EXAMPLE_LLM_NODE_PROPERTIES]
    )


class VertexDetailResponse(BaseModel):
    """Vertex 상세 정보 응답"""

    model_config = ConfigDict(
        json_schema_extra={"example": examples.EXAMPLE_VERTEX_DETAIL_RESPONSE}  # type: ignore
    )

    id: int
    type: str
    properties: Dict[str, Any] = Field(
        default={}, examples=[examples.EXAMPLE_LLM_NODE_PROPERTIES]
    )
    created_at: str | None = None
    updated_at: str | None = None

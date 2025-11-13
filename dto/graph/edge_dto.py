from typing import Any, Dict

from pydantic import BaseModel, ConfigDict, Field

from helpers.utils import req_res_examples as examples


class EdgeCreateRequest(BaseModel):
    """Edge 생성 요청 DTO"""

    model_config = ConfigDict(
        json_schema_extra={"example": examples.EXAMPLE_EDGE_CREATE_REQUEST}  # type: ignore
    )

    source_id: int
    target_id: int
    type: str = "default"
    source_properties: Dict[str, Any] = Field(
        default={}, examples=[examples.EXAMPLE_EDGE_SOURCE_PROPERTIES]
    )
    target_properties: Dict[str, Any] = Field(
        default={}, examples=[examples.EXAMPLE_EDGE_TARGET_PROPERTIES]
    )


class EdgeDetailResponse(BaseModel):
    """Edge 상세 정보 응답"""

    model_config = ConfigDict(
        json_schema_extra={"example": examples.EXAMPLE_EDGE_DETAIL_RESPONSE}  # type: ignore
    )

    id: int
    source_id: int
    target_id: int
    type: str
    source_properties: Dict[str, Any] = Field(
        default={}, examples=[examples.EXAMPLE_EDGE_SOURCE_PROPERTIES]
    )
    target_properties: Dict[str, Any] = Field(
        default={}, examples=[examples.EXAMPLE_EDGE_TARGET_PROPERTIES]
    )
    created_at: str | None = None
    updated_at: str | None = None

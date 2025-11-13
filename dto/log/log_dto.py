from typing import Any, Dict, List

from pydantic import BaseModel, ConfigDict, Field

from helpers.utils import req_res_examples as examples


class ExecutionLogMessageResponse(BaseModel):
    """실행 로그 메시지 응답"""

    model_config = ConfigDict(
        json_schema_extra={"example": examples.EXAMPLE_EXECUTION_LOG_MESSAGE_RESPONSE}  # type: ignore
    )

    timestamp: str
    level: str
    message: str
    node_id: str | None = None


class ExecutionLogResponse(BaseModel):
    """실행 로그 응답"""

    model_config = ConfigDict(
        json_schema_extra={"example": examples.EXAMPLE_EXECUTION_LOG_RESPONSE}  # type: ignore
    )

    execution_id: str
    graph_id: int
    status: str
    started_at: str
    completed_at: str | None = None
    execution_time: float | None = None
    success: bool | None = None
    error: str | None = None
    node_results: Dict[str, Any] = Field(
        default={}, examples=[examples.EXAMPLE_NODE_RESULTS]
    )
    execution_order: List[str] = []
    messages: List[ExecutionLogMessageResponse] | None = None


class ExecutionLogSearchResponse(BaseModel):
    """실행 로그 검색 응답"""

    model_config = ConfigDict(
        json_schema_extra={"example": examples.EXAMPLE_EXECUTION_LOG_SEARCH_RESPONSE}  # type: ignore
    )

    total: int
    logs: List[ExecutionLogResponse]
    query: str | None = None
    level: str | None = None

from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel, ConfigDict, Field

from dto.graph.edge_dto import EdgeCreateRequest, EdgeDetailResponse
from dto.graph.graph_dto import GraphDetailResponse
from dto.graph.vertex_dto import VertexCreateRequest, VertexDetailResponse
from helpers.utils import req_res_examples as examples


class WorkflowExecutionResult:
    """워크플로우 실행 결과"""

    def __init__(self):
        self.success: bool = False
        self.start_time: datetime | None = None
        self.end_time: datetime | None = None
        self.execution_time: float | None = None
        self.node_results: Dict[str, Any] = {}
        self.errors: List[str] = []
        self.execution_order: List[str] = []
        self.execution_id: str | None = None
        self.logs: List[str] = []  # 실행 중 수집된 로그 메시지들


class WorkflowCreateRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"example": examples.EXAMPLE_WORKFLOW_CREATE_REQUEST}  # type: ignore
    )

    name: str
    description: str = ""
    vertices: List[VertexCreateRequest] = []
    edges: List[EdgeCreateRequest] = []


class WorkflowCreateResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"example": examples.EXAMPLE_WORKFLOW_CREATE_RESPONSE}  # type: ignore
    )

    success: bool
    graph_id: int
    message: str


class WorkflowExecuteRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"example": examples.EXAMPLE_WORKFLOW_EXECUTE_REQUEST}  # type: ignore
    )

    initial_inputs: Dict[str, Any] | None = Field(
        default=None, examples=[examples.EXAMPLE_INITIAL_INPUTS]
    )


class WorkflowExecuteResponse(BaseModel):
    execution_id: str
    model_config = ConfigDict(
        json_schema_extra={"example": examples.EXAMPLE_WORKFLOW_EXECUTE_RESPONSE}  # type: ignore
    )

    success: bool
    result: Dict[str, Any] = Field(examples=[examples.EXAMPLE_NODE_RESULTS])
    errors: List[str]
    execution_order: List[str]
    execution_time: float
    start_time: datetime
    end_time: datetime


class WorkflowGetResponses(BaseModel):
    success: bool
    graph: Dict[str, Any]
    vertices: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]


class WorkflowUpdateRequest(BaseModel):
    """워크플로우 업데이트 요청 DTO"""

    model_config = ConfigDict(
        json_schema_extra={"example": examples.EXAMPLE_WORKFLOW_UPDATE_REQUEST}  # type: ignore
    )

    name: str | None = None
    description: str | None = None
    vertices: List[VertexCreateRequest] | None = None
    edges: List[EdgeCreateRequest] | None = None


# === Response Models ===


class WorkflowSummaryResponse(BaseModel):
    """워크플로우 요약 정보 응답"""

    model_config = ConfigDict(
        json_schema_extra={"example": examples.EXAMPLE_WORKFLOW_SUMMARY_RESPONSE}  # type: ignore
    )

    id: int
    name: str
    description: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class WorkflowDetailResponse(BaseModel):
    """워크플로우 전체 상세 정보 응답"""

    model_config = ConfigDict(
        json_schema_extra={"example": examples.EXAMPLE_WORKFLOW_DETAIL_RESPONSE}  # type: ignore
    )

    graph: GraphDetailResponse
    vertices: List[VertexDetailResponse]
    edges: List[EdgeDetailResponse]


class WorkflowStatusResponse(BaseModel):
    """워크플로우 상태 응답"""

    model_config = ConfigDict(
        json_schema_extra={"example": examples.EXAMPLE_WORKFLOW_STATUS_RESPONSE}  # type: ignore
    )

    graph_id: int
    status: str
    execution_id: str | None = None
    current_node: str | None = None
    progress: float | None = None
    message: str | None = None


class WorkflowDeleteResponse(BaseModel):
    """워크플로우 삭제 응답"""

    model_config = ConfigDict(
        json_schema_extra={"example": examples.EXAMPLE_WORKFLOW_DELETE_RESPONSE}  # type: ignore
    )

    success: bool
    message: str
    graph_id: int | None = None


class WorkflowUpdateResponse(BaseModel):
    """워크플로우 업데이트 응답"""

    model_config = ConfigDict(
        json_schema_extra={"example": examples.EXAMPLE_WORKFLOW_UPDATE_RESPONSE}  # type: ignore
    )

    success: bool
    graph_id: int
    message: str

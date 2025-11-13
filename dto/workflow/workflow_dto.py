from datetime import datetime
from typing import Any, Dict, List

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

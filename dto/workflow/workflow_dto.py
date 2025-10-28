from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel


class VertexCreateRequest(BaseModel):
    """Vertex 생성 요청 DTO"""

    type: str
    properties: Dict[str, Any] = {}


class EdgeCreateRequest(BaseModel):
    """Edge 생성 요청 DTO"""

    source_id: int
    target_id: int
    type: str = "default"
    source_properties: Dict[str, Any] = {}
    target_properties: Dict[str, Any] = {}


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


class WorkflowCreateRequest(BaseModel):
    name: str
    description: str = ""
    vertices: List[VertexCreateRequest] = []
    edges: List[EdgeCreateRequest] = []


class WorkflowCreateResponse(BaseModel):
    success: bool
    graph_id: int
    message: str


class WorkflowExecuteRequest(BaseModel):
    initial_inputs: Dict[str, Any] | None = None


class WorkflowExecuteResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
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

    name: str | None = None
    description: str | None = None
    vertices: List[VertexCreateRequest] | None = None
    edges: List[EdgeCreateRequest] | None = None

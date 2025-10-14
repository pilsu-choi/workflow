from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel


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
    vertices: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]


class WorkflowExecuteRequest(BaseModel):
    initial_inputs: Dict[str, Any] | None = None

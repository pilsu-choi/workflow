import enum
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from dataclasses import dataclass


class NodeType(enum.Enum):
    # Input/Output nodes
    TEXT_INPUT = "TEXT_INPUT"
    TEXT_OUTPUT = "TEXT_OUTPUT"
    JSON_INPUT = "JSON_INPUT"
    JSON_OUTPUT = "JSON_OUTPUT"
    FILE_INPUT = "FILE_INPUT"
    FILE_OUTPUT = "FILE_OUTPUT"

    # Processing nodes
    LLM_NODE = "LLM_NODE"
    API_CALL = "API_CALL"
    FUNCTION = "FUNCTION"
    CONDITION = "CONDITION"
    LOOP = "LOOP"

    # Utility nodes
    WEBHOOK = "WEBHOOK"
    DELAY = "DELAY"
    MERGE = "MERGE"
    SPLIT = "SPLIT"


class NodeInputOutputType(enum.Enum):
    TEXT = "TEXT"
    JSON = "JSON"
    FILE = "FILE"
    NUMBER = "NUMBER"
    BOOLEAN = "BOOLEAN"
    ARRAY = "ARRAY"
    OBJECT = "OBJECT"


@dataclass
class NodeInputOutput:
    name: str
    type: NodeInputOutputType
    required: bool = True
    value: Any = None
    description: str = ""


class BaseNode(ABC):
    """워크플로우 노드의 기본 클래스"""

    def __init__(self, node_id: str, properties: Dict[str, Any]):
        self.node_id = node_id
        self.properties = properties
        self.inputs: List[NodeInputOutput] = []
        self.outputs: List[NodeInputOutput] = []
        self.status: str = "pending"  # pending, running, completed, failed
        self.result: Any = None
        self.error: str | None = None

    @abstractmethod
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """노드 실행 로직"""
        pass

    @abstractmethod
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """입력 검증"""
        pass

    def get_input_schema(self) -> List[NodeInputOutput]:
        """입력 스키마 반환"""
        return self.inputs

    def get_output_schema(self) -> List[NodeInputOutput]:
        """출력 스키마 반환"""
        return self.outputs

    def set_status(self, status: str):
        """상태 설정"""
        self.status = status

    def set_result(self, result: Any):
        """결과 설정"""
        self.result = result
        self.status = "completed"

    def set_error(self, error: str):
        """에러 설정"""
        self.error = error
        self.status = "failed"

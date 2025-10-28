import enum
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, List, Literal

from pydantic import Field

if TYPE_CHECKING:
    from database.graph.edge import Edge


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
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4())[:8],
        description="Node의 input, output 포트 ID",
    )
    name: str = Field(description="Node의 input, output으로 대응되는 필드 이름")
    type: NodeInputOutputType = Field(description="Node의 input, output 타입")
    required: bool = Field(default=True)
    value: Any = Field(default=None)
    description: str = Field(description="Node의 input, output으로 대응되는 필드 설명")


class BaseNode(ABC):
    """워크플로우 노드의 기본 클래스"""

    def __init__(self, node_id: str, properties: Dict[str, Any]):
        self.node_id = node_id
        self.properties = properties
        self.inputs: List[NodeInputOutput] = []
        self.outputs: List[NodeInputOutput] = []
        self.status: str = "pending"  # pending, running, completed, failed
        self.error: str | None = None
        self.result: Any = None  # 노드 실행 결과
        self.in_connections: List["Edge"] = (
            []
        )  # TODO: Edge 받지 않고 사용 필드만 받아서 최적화 필요
        self.out_connections: List["Edge"] = (
            []
        )  # TODO: Edge 받지 않고 사용 필드만 받아서 최적화 필요

    @abstractmethod
    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """노드 실행 로직."""
        pass

    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """
        self.inputs 에 정의된 입력 필드가 모두 inputs에 있는지 검증.
        required=True인 필드만 검증.
        """
        for param in self.get_input_schema():
            if param.required and param.name not in inputs:
                return False
        return True

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

    def add_connection_port(
        self,
        edge: "Edge",
        direction: Literal["in", "out"],
    ):
        """노드의 입력 또는 출력 포트 값을 다음 노드의 입력 또는 출력 포트에 매핑"""

        if direction == "in":
            # TODO: 연결되는 input port 이름 혹은 id 체크 필요
            self.in_connections.append(edge)
        elif direction == "out":
            # TODO: 연결되는 output port 이름 혹은 id 체크 필요
            self.out_connections.append(edge)
        else:
            # TODO: raise logic check
            raise ValueError(f"Invalid direction: {direction}. Must be 'in' or 'out'.")

    def get_connected_edges(self, direction: Literal["in", "out"]) -> List["Edge"]:
        """연결된 노드의 입력 또는 출력 포트 스키마 반환"""
        if direction == "in":
            return self.in_connections
        elif direction == "out":
            return self.out_connections
        else:
            # TODO: raise logic check
            raise ValueError(f"Invalid direction: {direction}. Must be 'in' or 'out'.")

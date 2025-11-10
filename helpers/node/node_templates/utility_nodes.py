import json
from typing import Any, Dict

from helpers.node.node_base import BaseNode, NodeInputOutput, NodeInputOutputType
from helpers.node.node_type import NodeType
from setting.logger import get_logger

logger = get_logger(__name__)


class JSONParserNode(BaseNode):
    """JSON 파서 노드"""

    inputs = [
        NodeInputOutput(
            name="data",
            type=NodeInputOutputType.TEXT,
            description="파싱할 텍스트 데이터",
        )
    ]
    outputs = [
        NodeInputOutput(
            name="output",
            type=NodeInputOutputType.JSON,
            description="파싱된 JSON 데이터",
        )
    ]
    type = NodeType.PARSER_NODE

    def __init__(self, node_id: str, properties: Dict[str, Any]):
        super().__init__(node_id, properties)

    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        data = inputs.get("data", {})
        try:
            # json_data = json.loads(data)
            json_data = data
            return {"output": json_data}
        except json.JSONDecodeError:
            raise ValueError("유효하지 않은 JSON 데이터")


class ChatInputNode(BaseNode):
    """채팅 입력 노드"""

    inputs = [
        NodeInputOutput(
            name="message",
            type=NodeInputOutputType.TEXT,
            description="채팅 메시지",
        )
    ]
    outputs = [
        NodeInputOutput(
            name="output",
            type=NodeInputOutputType.TEXT,
            description="채팅 메시지",
        )
    ]
    type = NodeType.CHAT_INPUT

    def __init__(self, node_id: str, properties: Dict[str, Any]):
        super().__init__(node_id, properties)

    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        message = inputs.get("message", "")
        return {"output": message}

    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        return super().validate_inputs(inputs)


class ChatOutputNode(BaseNode):
    """채팅 출력 노드"""

    inputs = [
        NodeInputOutput(
            name="message",
            type=NodeInputOutputType.TEXT,
            description="채팅 메시지",
        )
    ]
    type = NodeType.CHAT_OUTPUT

    def __init__(self, node_id: str, properties: Dict[str, Any]):
        super().__init__(node_id, properties)

    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        message = inputs.get("message", "")
        return {"output": message}

    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        return super().validate_inputs(inputs)

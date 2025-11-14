import json
from typing import Any, Dict

from pydantic import BaseModel

from helpers.node.node_base import BaseNode, NodeInputOutput, NodeInputOutputType
from helpers.node.node_templates.node_field_types import (
    FieldOption,
    NodeField,
    NodeFieldsDefinition,
)
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
    properties: BaseModel

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

    @classmethod
    def get_properties(cls) -> BaseModel:
        return cls.properties

    @classmethod
    def get_properties_schema(cls) -> NodeFieldsDefinition:
        return NodeFieldsDefinition(
            fields=[
                NodeField(
                    name="operation_type",
                    type="select",
                    required=True,
                    default="serialize",
                    options=[
                        FieldOption(value="serialize", label="JSON 텍스트 변환"),
                        FieldOption(value="extract_value", label="JSON 값 추출"),
                        FieldOption(value="extract_fields", label="JSON 값 제거"),
                        FieldOption(value="add_fields", label="JSON 필드 추가"),
                    ],
                ),
                NodeField(
                    name="field_path",
                    type="text",
                    show_if="operation_type == extract_value",
                    placeholder="e.g., user.name, data.items[0].title",
                ),
                NodeField(
                    name="fields_to_extract",
                    type="text",
                    show_if="operation_type == extract_fields",
                    placeholder="e.g., name, email, age (comma-separated)",
                ),
                NodeField(
                    name="fields_to_add",
                    type="keyvalue",
                    show_if="operation_type == add_fields",
                ),
            ]
        )


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
    properties: BaseModel

    def __init__(self, node_id: str, properties: Dict[str, Any]):
        super().__init__(node_id, properties)

    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        message = inputs.get("message", "")
        return {"output": message}

    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        return super().validate_inputs(inputs)

    @classmethod
    def get_properties(cls) -> BaseModel:
        return cls.properties

    @classmethod
    def get_properties_schema(cls) -> NodeFieldsDefinition:
        return NodeFieldsDefinition(
            fields=[],
            info="Chat Input node provides user input for chat-based workflows. No additional configuration required.",
        )


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
    properties: BaseModel

    def __init__(self, node_id: str, properties: Dict[str, Any]):
        super().__init__(node_id, properties)

    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        message = inputs.get("message", "")
        return {"output": message}

    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        return super().validate_inputs(inputs)

    @classmethod
    def get_properties(cls) -> BaseModel:
        return cls.properties

    @classmethod
    def get_properties_schema(cls) -> NodeFieldsDefinition:
        return NodeFieldsDefinition(
            fields=[],
            info="Chat Output node provides formatted output for chat-based workflows. No additional configuration required.",
        )

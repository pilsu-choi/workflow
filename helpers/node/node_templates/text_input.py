from typing import Any, Dict

from helpers.node.node_base import BaseNode, NodeInputOutput, NodeInputOutputType


class TextInputNode(BaseNode):
    """텍스트 입력 노드"""

    def __init__(self, node_id: str, properties: Dict[str, Any]):
        super().__init__(node_id, properties)
        self.outputs = [
            NodeInputOutput(
                name="text",
                type=NodeInputOutputType.TEXT,
                description="입력된 텍스트",
            )
        ]

    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        text = inputs.get("text", "")
        inputs["text"] = text
        self.result = inputs
        result = inputs.copy()
        return result

    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        return True  # 입력 노드는 외부 입력을 받지 않음

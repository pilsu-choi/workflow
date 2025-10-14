from typing import Any, Dict
from helpers.node.node_base import (
    BaseNode,
    NodeInputOutput,
    NodeInputOutputType,
    NodeInputOutput,
)


class ConditionNode(BaseNode):
    """조건문 노드"""

    def __init__(self, node_id: str, properties: Dict[str, Any]):
        super().__init__(node_id, properties)
        self.inputs = [
            NodeInputOutput(
                name="condition",
                type=NodeInputOutputType.TEXT,
                description="조건식",
            ),
            NodeInputOutput(
                name="value",
                type=NodeInputOutputType.TEXT,
                description="비교할 값",
            ),
        ]
        self.outputs = [
            NodeInputOutput(
                name="true",
                type=NodeInputOutputType.BOOLEAN,
                description="조건이 참일 때",
            ),
            NodeInputOutput(
                name="false",
                type=NodeInputOutputType.BOOLEAN,
                description="조건이 거짓일 때",
            ),
        ]

    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        condition = inputs.get("condition", "")
        value = inputs.get("value", "")

        # 간단한 조건 평가 (실제로는 더 복잡한 파싱 필요)
        try:
            result = eval(condition.replace("value", f'"{value}"'))
            return {"true": result, "false": not result}
        except:
            return {"true": False, "false": True}

    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        return "condition" in inputs and "value" in inputs

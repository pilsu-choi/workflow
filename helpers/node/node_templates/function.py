from typing import Any, Dict
from helpers.node.node_base import (
    BaseNode,
    NodeInputOutput,
    NodeInputOutputType,
    NodeInputOutput,
)


class FunctionNode(BaseNode):
    """함수 실행 노드"""

    def __init__(self, node_id: str, properties: Dict[str, Any]):
        super().__init__(node_id, properties)
        self.inputs = [
            NodeInputOutput(
                name="code",
                type=NodeInputOutputType.TEXT,
                description="실행할 Python 코드",
            ),
            NodeInputOutput(
                name="args",
                type=NodeInputOutputType.JSON,
                description="함수 인자들",
                required=False,
            ),
        ]
        self.outputs = [
            NodeInputOutput(
                name="result",
                type=NodeInputOutputType.JSON,
                description="함수 실행 결과",
            )
        ]

    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        code = inputs.get("code", "")
        args = inputs.get("args", {})

        try:
            # 안전한 코드 실행을 위한 제한된 환경
            local_vars = {"args": args}
            exec(code, {"__builtins__": {}}, local_vars)
            result = local_vars.get("result", None)
            return {"result": result}
        except Exception as e:
            raise Exception(f"코드 실행 오류: {str(e)}")

    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        return "code" in inputs and inputs["code"]

from typing import Any, Dict
from helpers.node.node_base import (
    BaseNode,
    NodeInputOutput,
    NodeInputOutputType,
    NodeInputOutput,
)


class LLMNode(BaseNode):
    """LLM 노드"""

    def __init__(self, node_id: str, properties: Dict[str, Any]):
        super().__init__(node_id, properties)
        self.inputs = [
            NodeInputOutput(
                name="prompt",
                type=NodeInputOutputType.TEXT,
                description="LLM에 전달할 프롬프트",
            ),
            NodeInputOutput(
                name="model",
                type=NodeInputOutputType.TEXT,
                description="사용할 모델명",
                value="gpt-3.5-turbo",
            ),
        ]
        self.outputs = [
            NodeInputOutput(
                name="response",
                type=NodeInputOutputType.TEXT,
                description="LLM 응답",
            )
        ]

    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        # 실제 LLM 호출 로직은 여기에 구현
        # 현재는 모의 응답 반환
        prompt = inputs.get("prompt", "")
        model = inputs.get("model", "gpt-3.5-turbo")

        # 모의 응답
        response = f"LLM 응답 (모델: {model}): {prompt[:50]}..."
        inputs["response"] = response
        return inputs

    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        # return "prompt" in inputs and inputs["prompt"]
        return "text" in inputs and inputs["text"]

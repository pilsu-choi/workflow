import os
from typing import Any, Dict

from dotenv import load_dotenv
from openai import AsyncOpenAI

from helpers.node.node_base import BaseNode, NodeInputOutput, NodeInputOutputType
from helpers.node.node_type import NodeType

load_dotenv()


# FIXME: 테스트용 llm 호출 코드
async def call_openai_model(model: str, prompt: str, api_key: str) -> str | None:
    client = AsyncOpenAI(api_key=api_key)
    response = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


class LLMNode(BaseNode):
    """LLM 노드"""

    inputs = [
        NodeInputOutput(
            name="user_prompt",
            type=NodeInputOutputType.TEXT,
            description="LLM에 전달할 프롬프트",
        ),
    ]
    outputs = [
        NodeInputOutput(
            name="response",
            type=NodeInputOutputType.TEXT,
            description="LLM 응답",
        )
    ]
    type = NodeType.LLM_NODE

    def __init__(self, node_id: str, properties: Dict[str, Any]):
        super().__init__(node_id, properties)

    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:

        # input snapshot 저장
        self.params = inputs

        # 실제 LLM 호출 로직은 여기에 구현
        # 현재는 모의 응답 반환
        prompt = inputs.get("user_prompt", "")
        # model은 inputs나 properties에서 가져오기
        model = inputs.get("model") or self.properties.get("model", "gpt-4.1")
        api_key = os.getenv("OPENAI_API_KEY")

        # 모의 응답
        if api_key is None:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        response = await call_openai_model(model, prompt, api_key)
        result = inputs.copy()
        result["response"] = response
        result["node_type"] = self.__class__.__name__
        return result

    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """
        현재는 부모 클래스의 default method 이용하여 inputs 검증 진행. 필요시 override.
        """
        return super().validate_inputs(inputs)

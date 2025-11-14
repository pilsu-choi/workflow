from typing import Any, Dict

from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic import BaseModel

from helpers.node.node_base import BaseNode, NodeInputOutput, NodeInputOutputType
from helpers.node.node_templates.node_field_types import NodeField, NodeFieldsDefinition
from helpers.node.node_type import NodeType

load_dotenv()


# FIXME: 테스트용 llm 호출 코드
async def call_openai_model(model: str, prompt: str, api_key: str) -> str:
    client = AsyncOpenAI(api_key=api_key)
    response = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


class LLMProperties(BaseModel):
    provider: str = ""
    model_name: str = ""
    api_key: str | None = None
    system_prompt: str = ""
    user_prompt: str = ""


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
    properties: LLMProperties

    def __init__(self, node_id: str, properties: Dict[str, Any]):
        super().__init__(node_id, properties)

    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:

        # input snapshot 저장
        self.params = inputs

        # TODO: model_provider에 따라 api request url 변경 및 후처리 로직 작성 필요 - AISP 연동
        prompt = inputs.get("user_prompt", "")
        # model은 inputs나 properties에서 가져오기
        model = inputs.get("model") or self.properties.model_name
        api_key = self.properties.api_key

        # 모의 응답
        response = await call_openai_model(model, prompt, api_key)  # type: ignore
        result = inputs.copy()
        result["response"] = response
        result["node_type"] = self.__class__.__name__
        return result

    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """
        현재는 부모 클래스의 default method 이용하여 inputs 검증 진행. 필요시 override.
        """
        return super().validate_inputs(inputs)

    def validate_properties(self, properties: Dict[str, Any]) -> BaseModel:
        """
        properties를 검증하고 BaseModel로 반환
        """
        return LLMProperties.model_validate(properties)

    @classmethod
    def get_properties(cls) -> BaseModel:
        return cls.properties

    @classmethod
    def get_properties_schema(cls) -> NodeFieldsDefinition:
        return NodeFieldsDefinition(
            fields=[
                NodeField(
                    name="provider",
                    type="select",
                    required=True,
                    default="openai",
                    options=["openai", "anthropic", "google", "meta"],
                ),
                {
                    "name": "model_name",
                    "type": "model_select",
                    "required": True,
                    "depends_on": "provider",
                },
                {
                    "name": "api_key",
                    "type": "password",
                    "required": True,
                    "placeholder": "Enter your API key",
                },
                {
                    "name": "user_prompt",
                    "type": "textarea",
                    "rows": 3,
                    "placeholder": "Enter user prompt here. Use {{variable}} for templating.",
                },
                {
                    "name": "system_prompt",
                    "type": "textarea",
                    "rows": 3,
                    "placeholder": "Enter system prompt here.",
                },
            ]
        )


# FIXME: 나중에 실제 모델 정보로 변경 필요
temp_model_map = {
    "openai": ["gpt-4.1", "gpt-4.2", "gpt-4.3"],
    "anthropic": ["claude-3.7-sonnet", "claude-3.7-sonnet-20250219"],
    "google": ["gemini-2.0-flash", "gemini-2.0-flash-lite"],
    "meta": ["llama-3.1-8b", "llama-3.1-8b-instant"],
}

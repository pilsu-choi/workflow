"""
노드 템플릿 통합 정의 모듈 (Level 3 - 최상위)

역할:
- 모든 노드 정보를 통합해서 완전한 노드 정의 생성
- 프론트엔드 노드 패널에 표시할 노드 카탈로그 제공
- 카테고리별 노드 목록 관리

특징:
- 모든 노드 구현체를 import하여 조합
- 실행 시점에 노드 정보를 수집하여 NODE_TYPES 생성
- API 응답으로 프론트엔드에 전달

사용처:
- GET /api/nodes - 사용 가능한 모든 노드 목록 조회
- 프론트엔드 노드 패널 렌더링
- 노드 타입별 메타데이터 제공

의존성 계층:
  node_type.py
       ↓
  node_field_types.py
       ↓
  node 구현체들 (llm.py, condition.py 등)
       ↓
  node_template_types.py (현재 파일)

주의:
- 이 파일은 모든 노드 구현체를 import하므로 순환 import 주의
- 노드 구현체는 이 파일을 import하면 안됨
"""

import enum
from typing import Dict, List

from pydantic import BaseModel, Field

from helpers.node.node_base import NodeInputOutput
from helpers.node.node_templates.condition import ConditionNode
from helpers.node.node_templates.llm import LLMNode
from helpers.node.node_templates.node_field_types import NodeFieldsDefinition
from helpers.node.node_templates.utility_nodes import (
    ChatInputNode,
    ChatOutputNode,
    JSONParserNode,
)
from helpers.node.node_type import NodeType
from helpers.utils import req_res_examples as examples


class NodeTypeDefinition(BaseModel):
    """
    개별 노드의 완전한 정의

    프론트엔드 노드 패널에서 표시할 모든 정보를 포함:
    - 노드 타입 및 메타데이터 (type, label, description, icon, color)
    - 카테고리 분류 (AI_ML, DATA_PROCESSING, LOGIC, INPUT_OUTPUT)
    - 입출력 포트 정의 (inputs, outputs)
    - 설정 필드 스키마 (properties)

    사용 예시:
        프론트엔드에서 이 정보를 받아서:
        1. 노드 팔레트에 아이콘과 이름 표시
        2. 노드 추가 시 입출력 포트 생성
        3. 노드 설정 창에 동적 폼 생성
    """

    type: str
    label: str
    description: str
    category: str
    icon: str
    color: str
    inputs: list[NodeInputOutput] = Field(examples=[examples.EXAMPLE_NODE_INPUTS])
    outputs: list[NodeInputOutput] = Field(examples=[examples.EXAMPLE_NODE_OUTPUTS])
    properties: NodeFieldsDefinition


class NodeTypeCategory(enum.Enum):
    """
    노드 카테고리 분류

    프론트엔드 노드 패널에서 탭/섹션으로 구분하여 표시
    """

    AI_ML = "AI_ML"
    DATA_PROCESSING = "DATA_PROCESSING"
    LOGIC = "LOGIC"
    INPUT_OUTPUT = "INPUT_OUTPUT"


# 전체 노드 카탈로그
#
# 구조:
#     {
#         NodeTypeCategory.AI_ML: [LLM Node 정의, ...],
#         NodeTypeCategory.DATA_PROCESSING: [Parser Node 정의, ...],
#         NodeTypeCategory.LOGIC: [Condition Node 정의, ...],
#         NodeTypeCategory.INPUT_OUTPUT: [Chat Input/Output 정의, ...]
#     }
#
# 사용:
#     - GET /api/v1/nodes API 응답으로 전달
#     - 프론트엔드에서 노드 추가 UI 렌더링
#     - 새 노드 추가 시 이 딕셔너리에 등록
#
# 확장:
#     새 노드 추가 방법:
#     1. 노드 클래스 작성 (llm.py, condition.py 참고)
#     2. 이 파일에서 해당 노드 import
#     3. 적절한 카테고리에 NodeTypeDefinition 추가
NODE_TYPES: Dict[NodeTypeCategory, List[NodeTypeDefinition]] = {
    NodeTypeCategory.AI_ML: [
        NodeTypeDefinition(
            type=NodeType.LLM_NODE.value,
            label="Language Model",
            description="AI language model with configurable provider and prompts",
            category=NodeTypeCategory.AI_ML,
            icon="SmartToy",
            color="#9c27b0",
            inputs=LLMNode.get_input_schema(),
            outputs=LLMNode.get_output_schema(),
            properties=LLMNode.get_properties_schema(),
        )
    ],
    NodeTypeCategory.DATA_PROCESSING: [
        NodeTypeDefinition(
            type=NodeType.PARSER_NODE.value,
            label="Parser",
            description="Parse and transform JSON data with various operations",
            category=NodeTypeCategory.DATA_PROCESSING,
            icon="Code",
            color="#2196f3",
            inputs=JSONParserNode.get_input_schema(),
            outputs=JSONParserNode.get_output_schema(),
            properties=JSONParserNode.get_properties_schema(),
        )
    ],
    NodeTypeCategory.LOGIC: [
        NodeTypeDefinition(
            type=NodeType.CONDITION.value,
            label="If/Else",
            description="Conditional logic with comparison operators",
            category=NodeTypeCategory.LOGIC,
            icon="Condition",
            color="#e65100",
            inputs=ConditionNode.get_input_schema(),
            outputs=ConditionNode.get_output_schema(),
            properties=ConditionNode.get_properties_schema(),
        )
    ],
    NodeTypeCategory.INPUT_OUTPUT: [
        NodeTypeDefinition(
            type=NodeType.CHAT_INPUT.value,
            label="CHAT INPUT",
            description="Input node for chat-based workflows",
            category=NodeTypeCategory.INPUT_OUTPUT,
            icon="Input",
            color="#ff5722",
            inputs=ChatInputNode.get_input_schema(),
            outputs=ChatInputNode.get_output_schema(),
            properties=ChatInputNode.get_properties_schema(),
        ),
        NodeTypeDefinition(
            type=NodeType.CHAT_OUTPUT.value,
            label="CHAT OUTPUT",
            description="Output node for chat-based workflows with configurable formatting",
            category=NodeTypeCategory.INPUT_OUTPUT,
            icon="Reply",
            color="#4caf50",
            inputs=ChatOutputNode.get_input_schema(),
            outputs=ChatOutputNode.get_output_schema(),
            properties=ChatOutputNode.get_properties_schema(),
        ),
    ],
}

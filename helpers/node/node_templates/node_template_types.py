import enum
from typing import Dict, List

from pydantic import BaseModel, Field

from dto.workflow.workflow_dto import examples
from helpers.node.node_base import NodeInputOutput
from helpers.node.node_templates.condition import ConditionNode
from helpers.node.node_templates.llm import LLMNode
from helpers.node.node_templates.utility_nodes import (
    ChatInputNode,
    ChatOutputNode,
    JSONParserNode,
)
from helpers.node.node_type import NodeType


class NodeTypeDefinition(BaseModel):
    type: str
    label: str
    description: str
    category: str
    icon: str
    color: str
    inputs: list[NodeInputOutput] = Field(examples=[examples.EXAMPLE_NODE_INPUTS])
    outputs: list[NodeInputOutput] = Field(examples=[examples.EXAMPLE_NODE_OUTPUTS])


class NodeTypeCategory(enum.Enum):
    AI_ML = "AI_ML"
    DATA_PROCESSING = "DATA_PROCESSING"
    LOGIC = "LOGIC"
    INPUT_OUTPUT = "INPUT_OUTPUT"


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
        ),
    ],
}

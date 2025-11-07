import enum
from typing import Dict

from pydantic import BaseModel

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
    inputs: list[NodeInputOutput]
    outputs: list[NodeInputOutput]


class NodeTypeCategory(enum.Enum):
    AI_ML = "AI_ML"
    DATA_PROCESSING = "DATA_PROCESSING"
    LOGIC = "LOGIC"
    INPUT_OUTPUT = "INPUT_OUTPUT"


NODE_TYPES: Dict[NodeType, NodeTypeDefinition] = {
    NodeType.LLM_NODE: NodeTypeDefinition(
        type="LLM_NODE",
        label="Language Model",
        description="AI language model with configurable provider and prompts",
        category=NodeTypeCategory.AI_ML,
        icon="SmartToy",
        color="#9c27b0",
        inputs=LLMNode.get_input_schema(),
        outputs=LLMNode.get_output_schema(),
    ),
    NodeType.PARSER_NODE: NodeTypeDefinition(
        type="PARSER_NODE",
        label="Parser",
        description="Parse and transform JSON data with various operations",
        category=NodeTypeCategory.DATA_PROCESSING,
        icon="Code",
        color="#2196f3",
        inputs=JSONParserNode.get_input_schema(),
        outputs=JSONParserNode.get_output_schema(),
    ),
    NodeType.CONDITION: NodeTypeDefinition(
        type="CONDITION",
        label="If/Else",
        description="Conditional logic with comparison operators",
        category=NodeTypeCategory.LOGIC,
        icon="Condition",
        color="#e65100",
        inputs=ConditionNode.get_input_schema(),
        outputs=ConditionNode.get_output_schema(),
    ),
    NodeType.CHAT_INPUT: NodeTypeDefinition(
        type="CHAT_INPUT",
        label="CHAT INPUT",
        description="Input node for chat-based workflows",
        category=NodeTypeCategory.INPUT_OUTPUT,
        icon="Input",
        color="#ff5722",
        inputs=ChatInputNode.get_input_schema(),
        outputs=ChatInputNode.get_output_schema(),
    ),
    NodeType.CHAT_OUTPUT: NodeTypeDefinition(
        type="CHAT_OUTPUT",
        label="CHAT OUTPUT",
        description="Output node for chat-based workflows with configurable formatting",
        category=NodeTypeCategory.INPUT_OUTPUT,
        icon="Reply",
        color="#4caf50",
        inputs=ChatOutputNode.get_input_schema(),
        outputs=ChatOutputNode.get_output_schema(),
    ),
}

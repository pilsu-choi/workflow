import enum
from typing import Dict

from pydantic import BaseModel


class NodeType(enum.Enum):
    # Input/Output nodes
    TEXT_INPUT = "TEXT_INPUT"
    TEXT_OUTPUT = "TEXT_OUTPUT"
    JSON_INPUT = "JSON_INPUT"
    JSON_OUTPUT = "JSON_OUTPUT"
    FILE_INPUT = "FILE_INPUT"
    FILE_OUTPUT = "FILE_OUTPUT"
    CHAT_INPUT = "CHAT_INPUT"
    CHAT_OUTPUT = "CHAT_OUTPUT"

    # Processing nodes
    LLM_NODE = "LLM_NODE"
    API_CALL = "API_CALL"
    FUNCTION = "FUNCTION"
    CONDITION = "CONDITION"
    LOOP = "LOOP"

    # Utility nodes
    WEBHOOK = "WEBHOOK"
    DELAY = "DELAY"
    MERGE = "MERGE"
    SPLIT = "SPLIT"
    PARSER_NODE = "PARSER_NODE"


class NodeInputOutputType(enum.Enum):
    TEXT = "TEXT"
    JSON = "JSON"
    FILE = "FILE"
    NUMBER = "NUMBER"
    BOOLEAN = "BOOLEAN"
    ARRAY = "ARRAY"
    OBJECT = "OBJECT"


class NodeTypeDefinition(BaseModel):
    type: str
    label: str
    description: str
    category: str
    icon: str
    color: str


NODE_TYPES: Dict[NodeType, NodeTypeDefinition] = {
    NodeType.LLM_NODE: NodeTypeDefinition(
        type="LLM_NODE",
        label="Language Model",
        description="AI language model with configurable provider and prompts",
        category="AI_ML",
        icon="SmartToy",
        color="#9c27b0",
    ),
    NodeType.PARSER_NODE: NodeTypeDefinition(
        type="PARSER_NODE",
        label="Parser",
        description="Parse and transform JSON data with various operations",
        category="DATA_PROCESSING",
        icon="Code",
        color="#2196f3",
    ),
    NodeType.CONDITION: NodeTypeDefinition(
        type="CONDITION",
        label="If/Else",
        description="Conditional logic with comparison operators",
        category="LOGIC",
        icon="Condition",
        color="#e65100",
    ),
    NodeType.CHAT_INPUT: NodeTypeDefinition(
        type="CHAT_INPUT",
        label="CHAT INPUT",
        description="Input node for chat-based workflows",
        category="INPUT_OUTPUT",
        icon="Input",
        color="#ff5722",
    ),
    NodeType.CHAT_OUTPUT: NodeTypeDefinition(
        type="CHAT_OUTPUT",
        label="CHAT OUTPUT",
        description="Output node for chat-based workflows with configurable formatting",
        category="INPUT_OUTPUT",
        icon="Reply",
        color="#4caf50",
    ),
}

import enum


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

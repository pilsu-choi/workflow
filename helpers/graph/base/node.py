import enum


class NodeType(enum.Enum):
    FUNCTION = "FUNCTION"
    TEXT_IO = "TEXT_IO"
    WEBHOOK = "WEBHOOK"


class NodeInputType(enum.Enum):
    TEXT = "TEXT"
    JSON = "JSON"
    FILE = "FILE"

"""
노드 타입 정의 모듈 (Level 0 - 최하위)

역할:
- 시스템에서 사용 가능한 모든 노드 타입의 고유 식별자(enum) 정의
- 노드 입출력 데이터 타입의 고유 식별자 정의

특징:
- 외부 의존성 없음 (표준 라이브러리만 사용)
- 전체 시스템에서 참조하는 기본 상수
- 노드 팩토리, 라우팅, 타입 체크에서 사용

의존성 계층:
  node_type.py (현재 파일)
       ↓
  node_field_types.py
       ↓
  node 구현체들 (llm.py, condition.py 등)
       ↓
  node_template_types.py
"""

import enum


class NodeType(enum.Enum):
    """워크플로우에서 사용 가능한 노드 타입 정의"""

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
    """노드 입출력 포트의 데이터 타입 정의"""

    TEXT = "TEXT"
    JSON = "JSON"
    FILE = "FILE"
    NUMBER = "NUMBER"
    BOOLEAN = "BOOLEAN"
    ARRAY = "ARRAY"
    OBJECT = "OBJECT"

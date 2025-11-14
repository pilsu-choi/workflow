from typing import Any, Dict

from helpers.node.node_base import BaseNode
from helpers.node.node_templates.condition import ConditionNode
from helpers.node.node_templates.llm import LLMNode
from helpers.node.node_templates.utility_nodes import (
    ChatInputNode,
    ChatOutputNode,
    JSONParserNode,
)
from helpers.node.node_type import NodeType


class NodeFactory:
    """노드 생성 팩토리"""

    _node_classes: dict[NodeType, type[BaseNode]] = {
        NodeType.LLM_NODE: LLMNode,
        NodeType.CONDITION: ConditionNode,
        NodeType.PARSER_NODE: JSONParserNode,
        NodeType.CHAT_INPUT: ChatInputNode,
        NodeType.CHAT_OUTPUT: ChatOutputNode,
    }

    @classmethod
    def create_node(
        cls, node_type: NodeType, node_id: str, properties: Dict[str, Any]
    ) -> BaseNode:
        """노드 타입에 따라 적절한 노드 인스턴스 생성"""
        if node_type not in cls._node_classes:
            raise ValueError(f"지원하지 않는 노드 타입: {node_type}")

        node_class = cls._node_classes[node_type]
        return node_class(node_id, properties)

    @classmethod
    def register_node_type(cls, node_type: NodeType, node_class: type[BaseNode]):
        """새로운 노드 타입 등록"""
        cls._node_classes[node_type] = node_class

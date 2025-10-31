# 노드 팩토리
from typing import Any, Dict

from helpers.node.node_base import BaseNode, NodeType
from helpers.node.node_templates.condition import ConditionNode
from helpers.node.node_templates.function import FunctionNode
from helpers.node.node_templates.llm import LLMNode
from helpers.node.node_templates.text_input import TextInputNode
from helpers.node.node_templates.utility_nodes import (  # MergeNode,
    DelayNode,
    JSONOutputNode,
    JSONParserNode,
    SplitNode,
    TextOutputNode,
    WebhookNode,
)


class NodeFactory:
    """노드 생성 팩토리"""

    _node_classes: dict[NodeType, type[BaseNode]] = {
        NodeType.TEXT_INPUT: TextInputNode,
        NodeType.TEXT_OUTPUT: TextOutputNode,
        NodeType.JSON_OUTPUT: JSONOutputNode,
        NodeType.LLM_NODE: LLMNode,
        NodeType.CONDITION: ConditionNode,
        NodeType.FUNCTION: FunctionNode,
        NodeType.DELAY: DelayNode,
        NodeType.WEBHOOK: WebhookNode,
        # NodeType.MERGE: MergeNode,
        NodeType.SPLIT: SplitNode,
        NodeType.PARSER_NODE: JSONParserNode,  # PasrerNode,
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

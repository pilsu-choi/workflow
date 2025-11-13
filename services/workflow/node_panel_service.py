from dto.workflow.node_dto import NodePanelComponent, NodePanelResponse
from helpers.node.node_templates.node_template_types import NODE_TYPES


class NodePanelService:
    @classmethod
    def get_node_types(cls) -> NodePanelResponse:
        components: list[NodePanelComponent] = []
        for category, nodes in NODE_TYPES.items():
            components.append(
                NodePanelComponent(category=category, nodes=nodes, count=len(nodes))
            )
        return NodePanelResponse(components=components)

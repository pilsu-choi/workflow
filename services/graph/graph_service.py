from database.graph.edge import Edge
from database.graph.vertex import Vertex
from helpers.graph.base.node import NodeInputType, NodeType
from services.graph.edge_service import EdgeService
from services.graph.vertex_service import VertexService
from setting.logger import get_logger
from repositories.graph.graph_repository import GraphRepository
from fastapi import Depends
from database.graph.graph import Graph

logger = get_logger(__name__)


class GraphService:
    def __init__(
        self,
        graph_repository: GraphRepository = Depends(GraphRepository),
        vertex_service: VertexService = Depends(VertexService),
        edge_service: EdgeService = Depends(EdgeService),
        vertexs: list[Vertex] = [],
        edges: list[Edge] = [],
    ):
        self.graph_repository = graph_repository
        self.vertex_service = vertex_service
        self.edge_service = edge_service
        self.vertexs = vertexs
        self.edges = edges
        self.node_output = {}

    async def create_graph(self, graph: Graph):
        return await self.graph_repository.create_graph(graph)

    async def get_graph(self, graph_id: int):
        return await self.graph_repository.get_graph(graph_id)

    async def get_graphs(self):
        return await self.graph_repository.get_graphs()

    async def update_graph(self, graph_id: int, graph: Graph):
        return await self.graph_repository.update_graph(graph_id, graph)

    async def delete_graph(self, graph_id: int):
        return await self.graph_repository.delete_graph(graph_id)

    async def connect_vertices(self, source_id: int, target_id: int):
        return await self.edge_service.create_edge(
            Edge(source_id=source_id, target_id=target_id)
        )

    # TODO: oreder vertices, run python code, handover results to connected next vertex and aggregate at final vertex
    async def execute_graph(self, graph_id: int):
        result: dict = {}

        # 1. get graph
        graph = await self.get_graph(graph_id)

        # 2. order vertices
        vertices: list[Vertex] = await self.order_vertices(graph_id)

        # 3. run python code
        for vertex in vertices:
            result = await self.run_python_code(vertex.properties)

        # 4. handover results to connected next vertex and aggregate at final vertex

        return

    # TODO: 연결된 vertex 정렬
    async def order_vertices(self, graph_id: int):
        return

    async def run_python_code(
        self, python_code: str, node_input_type: str, node_type: str
    ):
        # 노드의 인풋이 필요한 경우라면 이전 노드 실행 결과 체크
        # TODO: 이전 node의 output을 현재 node의 input으로 사용하여야 함. how to map ?
        try:
            if node_input_type == NodeInputType.TEXT and node_type == NodeType.FUNCTION:
                previous_node_output = self.node_output.get("result", {}).get(
                    "text", None
                )
                # previous node output이 적절하게 존재하면 현재 노드 실행
                if previous_node_output:
                    # exec(python_code, self.node_output)
                    pass

        except Exception as e:
            logger.error(f"Error running python code: {e}")
            return None
        return self.node_output

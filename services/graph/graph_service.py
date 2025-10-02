from database.graph.edge import Edge
from database.graph.vertex import Vertex
from service.graph.edge_service import EdgeService
from service.graph.vertex_service import VertexService
from setting.logger import get_logger
from repository.graph.graph_repository import GraphRepository
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
        return

    # TODO: 연결된 vertex 정렬
    async def order_vertices(self, graph_id: int):
        return

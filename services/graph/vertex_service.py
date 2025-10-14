from database.graph.vertex import Vertex
from setting.logger import get_logger
from repositories.graph.vertex_repository import VertexRepository
from fastapi import Depends

logger = get_logger(__name__)


class VertexService:
    def __init__(self, vertex_repository: VertexRepository):
        self.vertex_repository = vertex_repository

    async def create_vertex(self, vertex: Vertex):
        # TODO: vertex 만들 때 properties에 실행해야 하는 코드 적재. 실행해야 하는 코드를 미리 정의해놓고 사용자한테는 변수만 받도록 ?
        return await self.vertex_repository.create_vertex(vertex)

    async def get_vertex(self, vertex_id: int):
        return await self.vertex_repository.get_vertex(vertex_id)

    async def get_vertices(self):
        return await self.vertex_repository.get_vertices()

    async def update_vertex(self, vertex_id: int, vertex: Vertex):
        return await self.vertex_repository.update_vertex(vertex_id, vertex)

    async def delete_vertex(self, vertex_id: int):
        return await self.vertex_repository.delete_vertex(vertex_id)

    async def get_vertices_by_graph_id(self, graph_id: int):
        return await self.vertex_repository.get_vertices_by_graph_id(graph_id)

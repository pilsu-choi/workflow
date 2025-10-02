from setting.logger import get_logger
from repository.graph.edge_repository import EdgeRepository
from fastapi import Depends
from database.graph.edge import Edge

logger = get_logger(__name__)


class EdgeService:
    def __init__(self, edge_repository: EdgeRepository = Depends(EdgeRepository)):
        self.edge_repository = edge_repository

    async def create_edge(self, edge: Edge):
        return await self.edge_repository.create_edge(edge)

    async def get_edge(self, edge_id: int):
        return await self.edge_repository.get_edge(edge_id)

    async def get_edges(self):
        return await self.edge_repository.get_edges()

    async def update_edge(self, edge_id: int, edge: Edge):
        return await self.edge_repository.update_edge(edge_id, edge)

    async def delete_edge(self, edge_id: int):
        return await self.edge_repository.delete_edge(edge_id)

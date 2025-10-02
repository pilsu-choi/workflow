from database.graph.vertex import Vertex
from sqlalchemy.ext.asyncio import AsyncSession
from setting.logger import get_logger

logger = get_logger(__name__)


class VertexRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_vertex(self, vertex: Vertex):
        await self.db.add(vertex)
        await self.db.commit()
        await self.db.refresh(vertex)
        logger.info(f"Vertex created: {vertex}")
        return vertex

    async def get_vertex(self, vertex_id: int):
        return await self.db.query(Vertex).filter(Vertex.id == vertex_id).first()

    async def get_vertices(self):
        return await self.db.query(Vertex).all()

    async def update_vertex(self, vertex_id: int, vertex: Vertex):
        await self.db.query(Vertex).filter(Vertex.id == vertex_id).update(
            vertex.model_dump()
        )
        await self.db.commit()
        logger.info(f"Vertex updated: {vertex}")
        return vertex

    async def delete_vertex(self, vertex_id: int):
        await self.db.query(Vertex).filter(Vertex.id == vertex_id).delete()
        await self.db.commit()
        logger.info(f"Vertex deleted: {vertex_id}")
        return vertex_id

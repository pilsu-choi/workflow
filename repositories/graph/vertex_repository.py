from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.graph.vertex import Vertex
from setting.logger import get_logger

logger = get_logger(__name__)


class VertexRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_vertex(self, vertex: Vertex):
        self.db.add(vertex)
        await self.db.flush()  # flush로 ID를 즉시 할당
        logger.info(f"Vertex created: {vertex}")
        return vertex

    async def get_vertex(self, vertex_id: int):
        result = await self.db.execute(select(Vertex).where(Vertex.id == vertex_id))
        return result.scalar_one_or_none()

    async def get_vertices(self):
        result = await self.db.execute(select(Vertex))
        return result.scalars().all()

    async def update_vertex(self, vertex_id: int, vertex: Vertex):
        stmt = select(Vertex).where(Vertex.id == vertex_id)
        result = await self.db.execute(stmt)
        existing_vertex = result.scalar_one_or_none()
        if existing_vertex:
            for key, value in vertex.model_dump().items():
                setattr(existing_vertex, key, value)
            await self.db.commit()
            logger.info(f"Vertex updated: {existing_vertex}")
        return existing_vertex

    async def delete_vertex(self, vertex_id: int):
        stmt = select(Vertex).where(Vertex.id == vertex_id)
        result = await self.db.execute(stmt)
        vertex = result.scalar_one_or_none()
        if vertex:
            await self.db.delete(vertex)
            await self.db.commit()
            logger.info(f"Vertex deleted: {vertex_id}")
        return vertex_id

    async def get_vertices_by_graph_id(self, graph_id: int):
        result = await self.db.execute(
            select(Vertex).where(Vertex.graph_id == graph_id)
        )
        return result.scalars().all()

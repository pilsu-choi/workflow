from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.graph.edge import Edge
from setting.logger import get_logger

logger = get_logger(__name__)


class EdgeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_edge(self, edge: Edge):
        self.db.add(edge)
        await self.db.flush()  # flush로 ID를 즉시 할당
        logger.info(f"Edge created: {edge}")
        return edge

    async def get_edge(self, edge_id: int):
        result = await self.db.execute(select(Edge).where(Edge.id == edge_id))
        return result.scalar_one_or_none()

    async def get_edges(self):
        result = await self.db.execute(select(Edge))
        return result.scalars().all()

    async def update_edge(self, edge_id: int, edge: Edge):
        stmt = select(Edge).where(Edge.id == edge_id)
        result = await self.db.execute(stmt)
        existing_edge = result.scalar_one_or_none()
        if existing_edge:
            for key, value in edge.model_dump().items():
                setattr(existing_edge, key, value)
            await self.db.commit()
            logger.info(f"Edge updated: {existing_edge}")
        return existing_edge

    async def delete_edge(self, edge_id: int):
        stmt = select(Edge).where(Edge.id == edge_id)
        result = await self.db.execute(stmt)
        edge = result.scalar_one_or_none()
        if edge:
            await self.db.delete(edge)
            await self.db.commit()
            logger.info(f"Edge deleted: {edge_id}")
        return edge_id

    async def get_edges_by_graph_id(self, graph_id: int):
        result = await self.db.execute(select(Edge).where(Edge.graph_id == graph_id))
        return result.scalars().all()

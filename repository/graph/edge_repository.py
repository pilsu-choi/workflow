from database.graph.edge import Edge
from sqlalchemy.ext.asyncio import AsyncSession
from setting.logger import get_logger

logger = get_logger(__name__)


class EdgeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_edge(self, edge: Edge):
        await self.db.add(edge)
        await self.db.commit()
        await self.db.refresh(edge)
        logger.info(f"Edge created: {edge}")

        return edge

    async def get_edge(self, edge_id: int):
        return await self.db.query(Edge).filter(Edge.id == edge_id).first()

    async def get_edges(self):
        return await self.db.query(Edge).all()

    async def update_edge(self, edge_id: int, edge: Edge):
        await self.db.query(Edge).filter(Edge.id == edge_id).update(edge.model_dump())
        await self.db.commit()
        logger.info(f"Edge updated: {edge}")
        return edge

    async def delete_edge(self, edge_id: int):
        await self.db.query(Edge).filter(Edge.id == edge_id).delete()
        await self.db.commit()
        logger.info(f"Edge deleted: {edge_id}")
        return edge_id

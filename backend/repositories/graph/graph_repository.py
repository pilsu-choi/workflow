from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.graph.graph import Graph
from setting.logger import get_logger

logger = get_logger(__name__)


class GraphRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        logger.debug(f"GraphRepository initialized with db: {db}")

    async def create_graph(self, graph: Graph):
        self.db.add(graph)
        await self.db.flush()  # flush로 ID를 즉시 할당
        logger.info(f"Graph created: {graph}")
        return graph

    async def get_graph(self, graph_id: int):
        result = await self.db.execute(select(Graph).where(Graph.id == graph_id))
        return result.scalar_one_or_none()

    async def get_graphs(self):
        result = await self.db.execute(select(Graph))
        return result.scalars().all()

    async def update_graph(self, graph_id: int, graph: Graph):
        stmt = select(Graph).where(Graph.id == graph_id)
        result = await self.db.execute(stmt)
        existing_graph = result.scalar_one_or_none()
        if existing_graph:
            for key, value in graph.model_dump().items():
                setattr(existing_graph, key, value)
            await self.db.commit()
            logger.info(f"Graph updated: {existing_graph}")

    async def delete_graph(self, graph_id: int):
        stmt = select(Graph).where(Graph.id == graph_id)
        result = await self.db.execute(stmt)
        graph = result.scalar_one_or_none()
        if graph:
            await self.db.delete(graph)
            await self.db.commit()
            logger.info(f"Graph deleted: {graph_id}")
        return graph_id

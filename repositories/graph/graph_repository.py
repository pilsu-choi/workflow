from sqlalchemy.ext.asyncio import AsyncSession
from database.graph.graph import Graph
from setting.logger import get_logger

logger = get_logger(__name__)


class GraphRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_graph(self, graph: Graph):
        await self.db.add(graph)
        await self.db.commit()
        await self.db.refresh(graph)
        logger.info(f"Graph created: {graph}")
        return graph

    async def get_graph(self, graph_id: int):
        return await self.db.query(Graph).filter(Graph.id == graph_id).first()

    async def get_graphs(self):
        return await self.db.query(Graph).all()

    async def update_graph(self, graph_id: int, graph: Graph):
        await self.db.query(Graph).filter(Graph.id == graph_id).update(
            graph.model_dump()
        )

    async def delete_graph(self, graph_id: int):
        await self.db.query(Graph).filter(Graph.id == graph_id).delete()
        await self.db.commit()
        logger.info(f"Graph deleted: {graph_id}")
        return graph_id

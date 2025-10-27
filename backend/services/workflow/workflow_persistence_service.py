from typing import Any, Dict, List, Tuple

from database.graph.edge import Edge
from database.graph.graph import Graph
from database.graph.vertex import Vertex
from repositories.graph.graph_repository import GraphRepository
from services.graph.edge_service import EdgeService
from services.graph.vertex_service import VertexService
from setting.logger import get_logger

logger = get_logger(__name__)


class WorkflowPersistenceService:
    """워크플로우 영속성 전용 서비스 - 워크플로우 저장/로드 담당"""

    def __init__(
        self,
        graph_repository: GraphRepository,
        vertex_service: VertexService,
        edge_service: EdgeService,
    ):
        self.graph_repository = graph_repository
        self.vertex_service = vertex_service
        self.edge_service = edge_service

    async def save(
        self, graph: Graph, vertices: List[Vertex], edges: List[Edge]
    ) -> Graph:
        """워크플로우를 데이터베이스에 저장"""
        try:
            # 그래프 저장
            saved_graph = await self.graph_repository.create_graph(graph)
            graph_id = saved_graph.id

            # 버텍스들 저장
            await self._save_vertices(vertices, graph_id)

            # 엣지들 저장
            await self._save_edges(edges, graph_id)

            # 모든 작업이 성공하면 commit
            await self.graph_repository.db.commit()
            await self.graph_repository.db.refresh(saved_graph)

            logger.info(f"워크플로우 저장 완료: {saved_graph.id}")
            return saved_graph

        except Exception as e:
            await self.graph_repository.db.rollback()
            logger.error(f"워크플로우 저장 실패: {str(e)}", exc_info=True)
            raise

    async def load(self, graph_id: int) -> Tuple[Graph, List[Vertex], List[Edge]]:
        """데이터베이스에서 워크플로우 로드"""
        try:
            # 그래프 로드
            graph = await self.graph_repository.get_graph(graph_id)
            if not graph:
                raise ValueError(f"그래프를 찾을 수 없습니다: {graph_id}")

            # 버텍스들 로드
            vertices = await self.vertex_service.get_vertices_by_graph_id(graph_id)

            # 엣지들 로드
            edges = await self.edge_service.get_edges_by_graph_id(graph_id)

            logger.info(f"워크플로우 로드 완료. id: {graph_id}")
            return graph, vertices, edges

        except Exception as e:
            logger.error(f"워크플로우 로드 실패: {str(e)}", exc_info=True)
            raise

    async def delete(self, graph_id: int) -> Dict[str, Any]:
        """워크플로우 삭제 (Graph + Vertices + Edges)"""
        try:
            # 관련된 vertices와 edges도 함께 삭제
            vertices = await self.vertex_service.get_vertices_by_graph_id(graph_id)
            edges = await self.edge_service.get_edges_by_graph_id(graph_id)

            # edges 삭제
            for edge in edges:
                await self.edge_service.delete_edge(edge.id)

            # vertices 삭제
            for vertex in vertices:
                await self.vertex_service.delete_vertex(vertex.id)

            # graph 삭제
            await self.graph_repository.delete_graph(graph_id)

            logger.info(f"워크플로우 삭제 완료: {graph_id}")
            return {
                "success": True,
                "message": "워크플로우가 성공적으로 삭제되었습니다",
            }

        except Exception as e:
            logger.error(f"워크플로우 삭제 실패: {str(e)}", exc_info=True)
            return {"success": False, "error": str(e)}

    async def _save_vertices(self, vertices: List[Vertex], graph_id: int):
        """버텍스들 저장"""
        for vertex in vertices:
            vertex.graph_id = graph_id
            await self.vertex_service.create_vertex(vertex)

    async def _save_edges(self, edges: List[Edge], graph_id: int):
        """엣지들 저장"""
        for edge in edges:
            edge.graph_id = graph_id
            await self.edge_service.create_edge(edge)

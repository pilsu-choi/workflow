from typing import Any, Dict, List, Tuple

from sqlalchemy import select

from database.graph.edge import Edge
from database.graph.graph import Graph
from database.graph.vertex import Vertex
from repositories.graph.edge_repository import EdgeRepository
from repositories.graph.graph_repository import GraphRepository
from repositories.graph.vertex_repository import VertexRepository
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
        vertex_repository: VertexRepository,
        edge_repository: EdgeRepository,
    ):
        self.graph_repository = graph_repository
        self.vertex_service = vertex_service
        self.edge_service = edge_service
        self.vertex_repository = vertex_repository
        self.edge_repository = edge_repository

    async def save(
        self, graph: Graph, vertices: List[Vertex], edges: List[Edge]
    ) -> Graph:
        """워크플로우를 데이터베이스에 저장"""
        try:
            # 그래프 저장
            saved_graph = await self.graph_repository.create_graph(graph)
            graph_id = saved_graph.id

            # 버텍스들 저장하고 ID 매핑 생성
            vertex_id_map = await self._save_vertices(vertices, graph_id)

            # 엣지들 저장 (인덱스를 실제 vertex ID로 매핑)
            await self._save_edges(edges, graph_id, vertex_id_map)

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

    async def update(
        self,
        graph_id: int,
        graph_updates: Dict[str, Any] | None = None,
        vertices: List[Vertex] | None = None,
        edges: List[Edge] | None = None,
    ) -> Graph:
        """워크플로우 업데이트"""
        try:
            db = self.graph_repository.db

            # 그래프 조회
            graph = await self.graph_repository.get_graph(graph_id)
            if not graph:
                raise ValueError(f"그래프를 찾을 수 없습니다: {graph_id}")

            # 그래프 메타데이터 업데이트
            if graph_updates:
                for key, value in graph_updates.items():
                    if value is not None and hasattr(graph, key):
                        setattr(graph, key, value)
                await db.flush()

            # vertices와 edges가 제공된 경우, 기존 것들을 삭제하고 새로 생성
            vertex_id_map = {}
            if vertices is not None:
                # 기존 vertices 삭제
                existing_vertices = await db.execute(
                    select(Vertex).where(Vertex.graph_id == graph_id)
                )
                for vertex in existing_vertices.scalars().all():
                    await db.delete(vertex)
                await db.flush()

                # 새 vertices 저장하고 ID 매핑 생성
                vertex_id_map = await self._save_vertices(vertices, graph_id)

            if edges is not None:
                # 기존 edges 삭제
                existing_edges = await db.execute(
                    select(Edge).where(Edge.graph_id == graph_id)
                )
                for edge in existing_edges.scalars().all():
                    await db.delete(edge)
                await db.flush()

                # 새 edges 저장 (인덱스를 실제 vertex ID로 매핑)
                await self._save_edges(edges, graph_id, vertex_id_map)

            # 모든 작업 commit
            await db.commit()
            await db.refresh(graph)

            logger.info(f"워크플로우 업데이트 완료: {graph_id}")
            return graph

        except Exception as e:
            await db.rollback()
            logger.error(f"워크플로우 업데이트 실패: {str(e)}", exc_info=True)
            raise

    async def delete(self, graph_id: int) -> Dict[str, Any]:
        """워크플로우 삭제 (Graph + Vertices + Edges)"""
        try:
            db = self.graph_repository.db

            # 관련된 edges 삭제 (직접 쿼리로 삭제)
            edges = await db.execute(select(Edge).where(Edge.graph_id == graph_id))
            for edge in edges.scalars().all():
                await db.delete(edge)

            # 관련된 vertices 삭제 (직접 쿼리로 삭제)
            vertices = await db.execute(
                select(Vertex).where(Vertex.graph_id == graph_id)
            )
            for vertex in vertices.scalars().all():
                await db.delete(vertex)

            # graph 삭제
            graph = await db.execute(select(Graph).where(Graph.id == graph_id))
            graph_obj = graph.scalar_one_or_none()
            if graph_obj:
                await db.delete(graph_obj)

            # 한 번에 commit
            await db.commit()

            logger.info(f"워크플로우 삭제 완료: {graph_id}")
            return {
                "success": True,
                "message": "워크플로우가 성공적으로 삭제되었습니다",
            }

        except Exception as e:
            await db.rollback()
            logger.error(f"워크플로우 삭제 실패: {str(e)}", exc_info=True)
            return {"success": False, "error": str(e)}

    async def _save_vertices(
        self, vertices: List[Vertex], graph_id: int
    ) -> Dict[int, int]:
        """버텍스들 저장하고 인덱스 -> ID 매핑 반환"""
        vertex_id_map = {}
        for idx, vertex in enumerate(vertices):
            vertex.graph_id = graph_id
            saved_vertex = await self.vertex_service.create_vertex(vertex)
            # 인덱스를 실제 데이터베이스 ID로 매핑
            vertex_id_map[idx] = saved_vertex.id
        return vertex_id_map

    async def _save_edges(
        self, edges: List[Edge], graph_id: int, vertex_id_map: Dict[int, int]
    ):
        """엣지들 저장 (source_id와 target_id를 인덱스에서 실제 ID로 매핑)"""
        for edge in edges:
            edge.graph_id = graph_id
            # source_id와 target_id가 인덱스인 경우 실제 vertex ID로 변환
            if edge.source_id in vertex_id_map:
                edge.source_id = vertex_id_map[edge.source_id]
            if edge.target_id in vertex_id_map:
                edge.target_id = vertex_id_map[edge.target_id]
            await self.edge_service.create_edge(edge)

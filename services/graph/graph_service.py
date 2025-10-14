from typing import List, Dict, Any
from database.graph.graph import Graph
from repositories.graph.graph_repository import GraphRepository
from setting.logger import get_logger

logger = get_logger(__name__)


class GraphService:
    """그래프 메타데이터 관리 전용 서비스 - Graph CRUD 작업만 담당"""

    def __init__(
        self,
        graph_repository: GraphRepository,
    ):
        self.graph_repository = graph_repository

    # === Graph 메타데이터 CRUD 작업 ===
    async def get_graphs(self) -> List[Graph]:
        """모든 그래프 메타데이터 조회"""
        return await self.graph_repository.get_graphs()

    async def get_graph(self, graph_id: int) -> Graph:
        """특정 그래프 메타데이터 조회"""
        return await self.graph_repository.get_graph(graph_id)

    async def create_graph(self, graph: Graph) -> Graph:
        """그래프 메타데이터 생성"""
        return await self.graph_repository.create_graph(graph)

    async def update_graph(self, graph_id: int, graph: Graph) -> Graph:
        """그래프 메타데이터 업데이트"""
        return await self.graph_repository.update_graph(graph_id, graph)

    async def delete_graph_metadata(self, graph_id: int) -> Dict[str, Any]:
        """그래프 메타데이터만 삭제 (워크플로우는 삭제하지 않음)"""
        try:
            await self.graph_repository.delete_graph(graph_id)
            return {
                "success": True,
                "message": "그래프 메타데이터가 성공적으로 삭제되었습니다",
            }
        except Exception as e:
            logger.error(f"그래프 메타데이터 삭제 실패: {str(e)}", exc_info=True)
            return {"success": False, "error": str(e)}

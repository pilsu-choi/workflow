from typing import Any, Dict

from dto.workflow.workflow_dto import WorkflowExecutionResult
from helpers.engine.workflow_engine import WorkflowEngine
from services.workflow.workflow_persistence_service import WorkflowPersistenceService
from setting.logger import get_logger

logger = get_logger(__name__)


class WorkflowExecutionService:
    """워크플로우 실행 전용 서비스 - 워크플로우 실행 및 상태 관리 담당"""

    def __init__(self, persistence_service: WorkflowPersistenceService):
        self.persistence_service = persistence_service
        self.workflow_engine = WorkflowEngine()

    async def execute_workflow(
        self, graph_id: int, initial_inputs: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """워크플로우 실행"""
        try:
            # 워크플로우 로드
            graph, vertices, edges = await self.persistence_service.load(graph_id)

            # 워크플로우 엔진에 로드
            success = await self.workflow_engine.load(vertices, edges)
            if not success:
                raise ValueError("워크플로우 로드 실패")

            # 워크플로우 실행
            result = await self.workflow_engine.start(initial_inputs)

            return self._format_execution_result(result)

        except Exception as e:
            logger.error(f"워크플로우 실행 실패: {str(e)}", exc_info=True)
            return {"success": False, "error": str(e)}

    async def get_workflow_status(self, graph_id: int) -> Dict[str, Any]:
        """워크플로우 상태 조회"""
        try:
            graph, vertices, edges = await self.persistence_service.load(graph_id)
            await self.workflow_engine.load(vertices, edges)
            return self.workflow_engine.get_workflow_status()
        except Exception as e:
            logger.error(f"워크플로우 상태 조회 실패: {str(e)}", exc_info=True)
            return {"error": str(e)}

    async def get_node_status(self, graph_id: int, node_id: str) -> Dict[str, Any]:
        """특정 노드 상태 조회"""
        try:
            graph, vertices, edges = await self.persistence_service.load(graph_id)
            await self.workflow_engine.load(vertices, edges)
            return self.workflow_engine.get_node_status(node_id)
        except Exception as e:
            logger.error(f"노드 상태 조회 실패: {str(e)}", exc_info=True)
            return {"error": str(e)}

    def reset_workflow_engine(self):
        """워크플로우 엔진 상태 초기화"""
        self.workflow_engine.reset_workflow()
        logger.info("워크플로우 엔진 상태 초기화 완료")

    def _format_execution_result(
        self, result: WorkflowExecutionResult
    ) -> Dict[str, Any]:
        """실행 결과 포맷팅"""
        return {
            "success": result.success,
            "execution_time": result.execution_time,
            "node_results": result.node_results,
            "errors": result.errors,
            "execution_order": result.execution_order,
        }

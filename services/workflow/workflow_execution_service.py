from typing import Any, Dict

from dto.workflow.workflow_dto import WorkflowExecuteResponse, WorkflowExecutionResult
from helpers.engine.workflow_engine import WorkflowEngine
from services.workflow.workflow_log_service import WorkflowLogService
from services.workflow.workflow_persistence_service import WorkflowPersistenceService
from setting.logger import get_logger

logger = get_logger(__name__)


class WorkflowExecutionService:
    """워크플로우 실행 전용 서비스 - 워크플로우 실행 및 상태 관리 담당"""

    def __init__(
        self,
        persistence_service: WorkflowPersistenceService,
        log_service: WorkflowLogService | None = None,
    ):
        self.persistence_service = persistence_service
        self.log_service = log_service
        self.workflow_engines: Dict[int, WorkflowEngine] = {}  # graph_id별로 엔진 관리

    async def execute_workflow(
        self, graph_id: int, initial_inputs: Dict[str, Any] | None = None
    ) -> WorkflowExecuteResponse:
        """워크플로우 실행"""
        try:
            # 워크플로우 로드
            graph, vertices, edges = await self.persistence_service.load(graph_id)

            # 워크플로우 엔진 생성 (WebSocket 활성화하여 실시간 상태 전송)
            workflow_engine = WorkflowEngine(
                workflow_id=str(graph_id), enable_websocket=True
            )

            # 워크플로우 엔진에 로드
            success = await workflow_engine.load(vertices, edges)
            if not success:
                raise ValueError("워크플로우 로드 실패")

            # 워크플로우 실행
            result = await workflow_engine.start(initial_inputs)

            # 엔진 인스턴스 저장 (상태 조회용)
            self.workflow_engines[graph_id] = workflow_engine

            # 로그 저장 (log_service가 있는 경우)
            if self.log_service:
                try:
                    await self.log_service.save_execution_log(graph_id, result)
                    logger.info(
                        f"워크플로우 실행 로그 저장 완료: execution_id={result.execution_id}"
                    )
                except Exception as log_error:
                    logger.error(f"로그 저장 실패: {str(log_error)}", exc_info=True)
                    # 로그 저장 실패는 워크플로우 실행 자체는 성공한 것으로 처리

            return self._format_execution_result(result)

        except Exception as e:
            logger.error(f"워크플로우 실행 실패: {str(e)}", exc_info=True)
            return WorkflowExecuteResponse(
                execution_id=result.execution_id,
                success=False,
                result={},
                errors=[str(e)],
                execution_order=[],
                execution_time=0,
                start_time=result.start_time,
                end_time=result.end_time,
            )

    async def get_workflow_status(self, graph_id: int) -> Dict[str, Any]:
        """워크플로우 상태 조회"""
        try:
            # 기존에 실행된 엔진이 있으면 그것을 사용
            if graph_id in self.workflow_engines:
                return self.workflow_engines[graph_id].get_workflow_status()

            # 없으면 새로 로드
            graph, vertices, edges = await self.persistence_service.load(graph_id)
            workflow_engine = WorkflowEngine(
                workflow_id=str(graph_id), enable_websocket=False
            )
            await workflow_engine.load(vertices, edges)
            return workflow_engine.get_workflow_status()
        except Exception as e:
            logger.error(f"워크플로우 상태 조회 실패: {str(e)}", exc_info=True)
            return {"error": str(e)}

    async def get_node_status(self, graph_id: int, node_id: str) -> Dict[str, Any]:
        """특정 노드 상태 조회"""
        try:
            # 기존에 실행된 엔진이 있으면 그것을 사용
            if graph_id in self.workflow_engines:
                return self.workflow_engines[graph_id].get_node_status(node_id)

            # 없으면 새로 로드
            graph, vertices, edges = await self.persistence_service.load(graph_id)
            workflow_engine = WorkflowEngine(
                workflow_id=str(graph_id), enable_websocket=False
            )
            await workflow_engine.load(vertices, edges)
            return workflow_engine.get_node_status(node_id)
        except Exception as e:
            logger.error(f"노드 상태 조회 실패: {str(e)}", exc_info=True)
            return {"error": str(e)}

    def reset_workflow_engine(self, graph_id: int | None = None):
        """워크플로우 엔진 상태 초기화"""
        if graph_id is not None:
            # 특정 워크플로우 엔진 초기화
            if graph_id in self.workflow_engines:
                self.workflow_engines[graph_id].reset_workflow()
                del self.workflow_engines[graph_id]
                logger.info(f"워크플로우 엔진 상태 초기화 완료 (graph_id: {graph_id})")
        else:
            # 모든 워크플로우 엔진 초기화
            for engine in self.workflow_engines.values():
                engine.reset_workflow()
            self.workflow_engines.clear()
            logger.info("모든 워크플로우 엔진 상태 초기화 완료")

    def _format_execution_result(
        self, result: WorkflowExecutionResult
    ) -> WorkflowExecuteResponse:
        """실행 결과 포맷팅"""
        return WorkflowExecuteResponse(
            execution_id=result.execution_id,
            success=result.success,
            result=result.node_results,
            errors=result.errors,
            execution_order=result.execution_order,
            execution_time=result.execution_time,
            start_time=result.start_time,
            end_time=result.end_time,
        )

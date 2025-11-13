import uuid
from collections import defaultdict, deque
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from database.graph.edge import Edge
from database.graph.vertex import Vertex
from dto.workflow.workflow_dto import WorkflowExecutionResult
from helpers.node.factory import NodeFactory
from helpers.node.node_base import BaseNode
from helpers.node.node_type import NodeType
from helpers.websockets import WebSocketHandler, ws_manager
from setting.logger import get_logger

logger = get_logger(__name__)


class WorkflowEngine:
    """워크플로우 실행 엔진"""

    def __init__(
        self, workflow_id: Optional[str] = None, enable_websocket: bool = True
    ):
        self.node_instances: Dict[str, BaseNode] = {}
        self.execution_context: Dict[str, Any] = (
            {}
        )  # 노드 실행 결과 저장. key: 노드 ID, value: 노드 실행 결과. 단, 다음 노드 실행을 위한 input port에 맞춰 데이터 가공
        self.dependencies: Dict[str, Set[str]] = defaultdict(set)
        self.reverse_dependencies: Dict[str, Set[str]] = defaultdict(set)
        self.is_first_execution: bool = True
        self.initial_inputs: Dict[str, Any] = {}
        self.logs: List[str] = []  # 실행 중 로그 메시지 수집
        self.workflow_id = workflow_id  # WebSocket 메시지 전송용
        self.enable_websocket = enable_websocket  # WebSocket 활성화 여부
        self.execution_id: Optional[str] = None  # 현재 실행 ID

    def _add_log(self, message: str):
        """로그 메시지 추가"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        logger.info(message)

    async def load(self, vertices: List[Vertex], edges: List[Edge]) -> bool:
        """데이터베이스에서 워크플로우 로드"""
        try:
            # 노드 인스턴스 생성
            for vertex in vertices:
                node_type = NodeType(vertex.type)
                node_instance = NodeFactory.create_node(
                    node_type, str(vertex.id), vertex.properties
                )
                self.node_instances[str(vertex.id)] = node_instance

            # 의존성 그래프 구성
            for edge in edges:
                source_id = str(edge.source_id)
                target_id = str(edge.target_id)
                source_node = self.node_instances[source_id]
                target_node = self.node_instances[target_id]

                # TODO: check
                source_node.add_connection_port(edge=edge, direction="out")
                target_node.add_connection_port(edge=edge, direction="in")
                self.dependencies[target_id].add(source_id)
                self.reverse_dependencies[source_id].add(target_id)

            self._add_log(
                f"워크플로우 로드 완료: {len(self.node_instances)}개 노드, {len(edges)}개 엣지"
            )
            return True

        except Exception as e:
            self._add_log(f"워크플로우 로드 실패: {str(e)}")
            logger.error(f"워크플로우 로드 실패: {str(e)}", exc_info=True)
            return False

    def _topological_sort(self) -> List[str]:
        """위상 정렬로 실행 순서 결정"""
        in_degree = defaultdict(int)  # 자동으로 0으로 초기화

        # 각 노드의 진입 차수 계산
        for node_id in self.node_instances:
            in_degree[node_id] = len(self.dependencies[node_id])

        # 진입 차수가 0인 노드들을 큐에 추가
        queue = deque(
            [node_id for node_id in self.node_instances if in_degree[node_id] == 0]
        )
        result = []

        while queue:
            current = queue.popleft()
            result.append(current)

            # 현재 노드에서 나가는 엣지들 처리
            for neighbor in self.reverse_dependencies[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # 사이클 검사
        if len(result) != len(self.node_instances):
            raise ValueError("워크플로우에 사이클이 존재합니다")

        return result

    def _collect_node_inputs(self, node_id: str) -> Dict[str, Any]:
        """노드의 입력 데이터 수집"""
        inputs = {}

        # initial_inputs 병합 (첫 실행인 경우)
        if self.is_first_execution:
            inputs.update(self.initial_inputs)

        # 의존성 노드들의 출력을 입력으로 수집
        for dependency_id in self.dependencies[node_id]:
            if dependency_id in self.execution_context:
                dependency_outputs = self.execution_context[dependency_id]
                inputs.update(dependency_outputs)

        return inputs

    async def _execute_node(self, node_id: str) -> Dict[str, Any]:
        """단일 노드 실행"""
        node = self.node_instances[node_id]
        execute_state = {}
        try:
            # 노드 상태를 running으로 설정
            node.set_status("running")

            # WebSocket으로 노드 실행 시작 알림
            await self._send_node_status(node_id, "running")

            # 입력 데이터 수집
            inputs = self._collect_node_inputs(node_id)
            logger.debug(f"노드 {node_id} 입력 데이터: {inputs}")

            # 입력 검증
            if not node.validate_inputs(inputs):
                error_msg = f"노드 {node_id} 입력 검증 실패 - 입력: {inputs}, 필요: {[inp.name for inp in node.get_input_schema()]}"
                self._add_log(error_msg)
                logger.error(error_msg, exc_info=True)
                raise ValueError(
                    f"노드 {node_id}, {node.get_type().value}의 입력 검증 실패"
                )

            # 노드 실행
            self._add_log(f"노드 {node_id} 실행 시작")
            result = await node.execute(inputs)

            # 결과 저장
            node.set_result(result)

            # FIXME: for debug.추후 삭제 필요
            execute_state["original_result"] = result

            # 현재 노드의 output을 다음 노드의 input으로 사용하기 위한 result 세팅.
            # node의 connections 정보를 사용하여 다음 노드의 input 포트에 해당되는 필드에 결과값을 converting 작업 필요.
            # ex)다음 노드의 input 포트에 해당되는 필드가 "user_query"이고, 현재 노드의 output 포트에 해당되는 필드가 "text"인 경우, 결과값을 "user_query" 필드에 매핑.
            for edge in node.get_connected_edges(direction="out"):

                # 노드 포트 매핑하여 체이닝 처리.
                # 다음 노드의 input field를 맞춰줄 땐 조건 체크해야 함. 모든 노드의 조건 체크해아하나?
                # edge.source_properties와 edge.target_properties는 dict 타입으로 저장됨
                source_props = (
                    edge.source_properties
                    if isinstance(edge.source_properties, dict)
                    else edge.source_properties.__dict__
                )
                target_props = (
                    edge.target_properties
                    if isinstance(edge.target_properties, dict)
                    else edge.target_properties.__dict__
                )

                source_name = source_props.get("name")
                target_name = target_props.get("name")

                if source_name:
                    candidate_converted_result = result.get(source_name, None)
                    if candidate_converted_result is not None and target_name:
                        execute_state[target_name] = candidate_converted_result

            self.execution_context[node_id] = execute_state

            if self.is_first_execution:
                self.is_first_execution = False

            self._add_log(f"노드 {node_id} 실행 완료")

            # WebSocket으로 노드 실행 완료 알림
            await self._send_node_status(node_id, "completed", result=result)

            # 연결된 다음 노드들에게 edge flow 알림
            await self._send_edge_flows(node_id)

            return result

        except Exception as e:
            error_msg = f"노드 {node_id} 실행 실패: {str(e)}"
            self._add_log(error_msg)
            logger.error(error_msg, exc_info=True)
            node.set_error(error_msg)

            # WebSocket으로 노드 실행 실패 알림
            await self._send_node_status(node_id, "error", error=error_msg)

            raise

    async def start(
        self, initial_inputs: Dict[str, Any] | None = None
    ) -> WorkflowExecutionResult:
        """워크플로우 실행"""
        result = WorkflowExecutionResult()
        result.start_time = datetime.now()
        result.execution_id = str(uuid.uuid4())  # 실행 ID 생성
        self.execution_id = result.execution_id  # 인스턴스 변수에 저장

        try:
            # 초기 입력 저장
            self.initial_inputs = initial_inputs if initial_inputs else {}

            # 실행 순서 결정
            execution_order = self._topological_sort()
            result.execution_order = execution_order

            self._add_log(
                f"워크플로우 실행 시작 (execution_id: {result.execution_id}): {len(execution_order)}개 노드"
            )

            # WebSocket으로 워크플로우 시작 알림
            await self._send_workflow_start(result.execution_id, execution_order)

            # 순차적으로 노드 실행
            for idx, node_id in enumerate(execution_order):
                try:
                    # WebSocket으로 진행률 전송
                    await self._send_progress(idx + 1, len(execution_order), node_id)

                    # TODO: 병렬 처리 노드 고려 필요. 병렬 처리 노드를 multi processing으로 할 것인지, threading으로 할 것인지, asyncio로 할 것인지 고려 필요.
                    node_result = await self._execute_node(node_id)
                    result.node_results[node_id] = node_result
                except Exception as e:
                    result.errors.append(str(e))
                    # 에러 발생 시 워크플로우 중단
                    break

            # 실행 완료
            result.end_time = datetime.now()
            result.execution_time = (
                result.end_time - result.start_time
            ).total_seconds()
            result.success = len(result.errors) == 0

            if result.success:
                self._add_log(f"워크플로우 실행 성공: {result.execution_time:.2f}초")
            else:
                self._add_log(f"워크플로우 실행 실패: {len(result.errors)}개 에러")
                logger.error(
                    f"워크플로우 실행 실패: {len(result.errors)}개 에러", exc_info=True
                )

            # WebSocket으로 워크플로우 완료 알림
            await self._send_workflow_complete(
                result.execution_id,
                result.success,
                result.execution_time,
                result.errors,
            )

        except Exception as e:
            result.end_time = datetime.now()
            result.execution_time = (
                result.end_time - result.start_time
            ).total_seconds()
            error_msg = f"워크플로우 실행 중 예상치 못한 오류: {str(e)}"
            result.errors.append(error_msg)
            self._add_log(error_msg)
            logger.error(f"워크플로우 실행 중 오류: {str(e)}", exc_info=True)

        # 수집된 로그를 result에 복사
        result.logs = self.logs.copy()
        return result

    def get_node_status(self, node_id: str) -> Dict[str, Any]:
        """노드 상태 조회"""
        if node_id not in self.node_instances:
            return {"error": "노드를 찾을 수 없습니다"}

        node = self.node_instances[node_id]
        return {
            "node_id": node_id,
            "status": node.status,
            "result": node.result,
            "error": node.error,
            "inputs": [
                input_schema.model_dump() for input_schema in node.get_input_schema()
            ],
            "outputs": [
                output_schema.model_dump() for output_schema in node.get_output_schema()
            ],
        }

    def get_workflow_status(self) -> Dict[str, Any]:
        """전체 워크플로우 상태 조회"""
        node_statuses = {}
        for node_id in self.node_instances:
            node_statuses[node_id] = self.get_node_status(node_id)

        return {
            "total_nodes": len(self.node_instances),
            "node_statuses": node_statuses,
            "execution_context": self.execution_context,
        }

    def reset_workflow(self):
        """워크플로우 상태 초기화"""
        self.execution_context.clear()
        self.initial_inputs = {}
        self.is_first_execution = True
        self.logs.clear()  # 로그도 초기화
        self.execution_id = None  # 실행 ID 초기화
        for node in self.node_instances.values():
            node.status = "pending"
            node.result = None
            node.error = None
        logger.info("워크플로우 상태 초기화 완료")

    # ===== WebSocket 관련 메서드 =====

    async def _send_workflow_start(self, execution_id: str, execution_order: List[str]):
        """워크플로우 시작 메시지 전송"""
        if not self.enable_websocket or not self.workflow_id:
            return

        if ws_manager.has_connections(self.workflow_id):
            message = WebSocketHandler.create_workflow_start_message(
                workflow_id=self.workflow_id,
                execution_id=execution_id,
                execution_order=execution_order,
            )
            await ws_manager.broadcast_to_workflow(message, self.workflow_id)

    async def _send_workflow_complete(
        self,
        execution_id: str,
        success: bool,
        execution_time: float,
        errors: List[str],
    ):
        """워크플로우 완료 메시지 전송"""
        if not self.enable_websocket or not self.workflow_id:
            return

        if ws_manager.has_connections(self.workflow_id):
            message = WebSocketHandler.create_workflow_complete_message(
                workflow_id=self.workflow_id,
                execution_id=execution_id,
                success=success,
                execution_time=execution_time,
                errors=errors,
            )
            await ws_manager.broadcast_to_workflow(message, self.workflow_id)

    async def _send_node_status(
        self,
        node_id: str,
        status: str,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
    ):
        """노드 상태 변경 메시지 전송"""
        if not self.enable_websocket or not self.workflow_id or not self.execution_id:
            return

        if ws_manager.has_connections(self.workflow_id):
            message = WebSocketHandler.create_node_status_message(
                workflow_id=self.workflow_id,
                execution_id=self.execution_id,
                node_id=node_id,
                status=status,
                result=result,
                error=error,
            )
            await ws_manager.broadcast_to_workflow(message, self.workflow_id)

    async def _send_edge_flows(self, source_node_id: str):
        """현재 노드에서 다음 노드로의 데이터 흐름 메시지 전송"""
        if not self.enable_websocket or not self.workflow_id or not self.execution_id:
            return

        if not ws_manager.has_connections(self.workflow_id):
            return

        # 현재 노드의 다음 노드들에게 edge flow 메시지 전송
        for target_node_id in self.reverse_dependencies.get(source_node_id, []):
            message = WebSocketHandler.create_edge_flow_message(
                workflow_id=self.workflow_id,
                execution_id=self.execution_id,
                source_node_id=source_node_id,
                target_node_id=target_node_id,
            )
            await ws_manager.broadcast_to_workflow(message, self.workflow_id)

    async def _send_progress(
        self, current_step: int, total_steps: int, current_node_id: str
    ):
        """진행률 메시지 전송"""
        if not self.enable_websocket or not self.workflow_id or not self.execution_id:
            return

        if ws_manager.has_connections(self.workflow_id):
            message = WebSocketHandler.create_progress_message(
                workflow_id=self.workflow_id,
                execution_id=self.execution_id,
                current_step=current_step,
                total_steps=total_steps,
                current_node_id=current_node_id,
            )
            await ws_manager.broadcast_to_workflow(message, self.workflow_id)

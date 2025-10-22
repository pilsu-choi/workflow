from collections import defaultdict, deque
from datetime import datetime
from typing import Any, Dict, List, Set

from database.graph.edge import Edge
from database.graph.vertex import Vertex
from dto.workflow.workflow_dto import WorkflowExecutionResult
from helpers.node.factory import NodeFactory
from helpers.node.node_base import BaseNode, NodeType
from setting.logger import get_logger

logger = get_logger(__name__)


class WorkflowEngine:
    """워크플로우 실행 엔진"""

    def __init__(self):
        self.node_instances: Dict[str, BaseNode] = {}
        self.execution_context: Dict[str, Any] = {}
        self.dependencies: Dict[str, Set[str]] = defaultdict(set)
        self.reverse_dependencies: Dict[str, Set[str]] = defaultdict(set)
        self.is_first_execution: bool = True

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

                self.dependencies[target_id].add(source_id)
                self.reverse_dependencies[source_id].add(target_id)

            logger.info(
                f"워크플로우 로드 완료: {len(self.node_instances)}개 노드, {len(edges)}개 엣지"
            )
            return True

        except Exception as e:
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

        if self.is_first_execution:
            return self.execution_context

        # 의존성 노드들의 출력을 입력으로 수집
        for dependency_id in self.dependencies[node_id]:
            if dependency_id in self.execution_context:
                dependency_outputs = self.execution_context[dependency_id]
                inputs.update(dependency_outputs)

        return inputs

    async def _execute_node(self, node_id: str) -> Dict[str, Any]:
        """단일 노드 실행"""
        node = self.node_instances[node_id]

        try:
            # 노드 상태를 running으로 설정
            node.set_status("running")

            # 입력 데이터 수집
            inputs = self._collect_node_inputs(node_id)

            # 입력 검증
            if not node.validate_inputs(inputs):
                raise ValueError(f"노드 {node_id}의 입력 검증 실패")

            # 노드 실행
            logger.info(f"노드 {node_id} 실행 시작")
            result = node.execute(inputs)

            # 결과 저장
            node.set_result(result)

            # 현재 노드의 output을 다음 노드의 input으로 사용하기 위한 result 세팅
            self.execution_context[node_id] = result

            # TODO: 노드 체이닝 input/ouput 인터페이스 체크. 다음 노드의 input field 체크 및 parameter 자동 매핑 위한 모듈 구현..?
            # 다음 노드의 input field를 맞춰줄 땐 조건 체크해야 함. 모든 노드의 조건 체크해아하나?
            if self.is_first_execution:
                self.is_first_execution = False

            logger.info(f"노드 {node_id} 실행 완료")
            return result

        except Exception as e:
            error_msg = f"노드 {node_id} 실행 실패: {str(e)}"
            logger.error(error_msg, exc_info=True)
            node.set_error(error_msg)
            raise

    async def start(
        self, initial_inputs: Dict[str, Any] | None = None
    ) -> WorkflowExecutionResult:
        """워크플로우 실행"""
        result = WorkflowExecutionResult()
        result.start_time = datetime.now()

        try:
            # 초기 입력 설정
            if initial_inputs:
                self.execution_context.update(initial_inputs)

            # 실행 순서 결정
            execution_order = self._topological_sort()
            result.execution_order = execution_order

            logger.info(f"워크플로우 실행 시작: {len(execution_order)}개 노드")

            # 순차적으로 노드 실행
            for node_id in execution_order:
                try:
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
                logger.info(f"워크플로우 실행 성공: {result.execution_time:.2f}초")
            else:
                logger.error(
                    f"워크플로우 실행 실패: {len(result.errors)}개 에러", exc_info=True
                )

        except Exception as e:
            result.end_time = datetime.now()
            result.execution_time = (
                result.end_time - result.start_time
            ).total_seconds()
            result.errors.append(f"워크플로우 실행 중 예상치 못한 오류: {str(e)}")
            logger.error(f"워크플로우 실행 중 오류: {str(e)}", exc_info=True)

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
                input_schema.__dict__ for input_schema in node.get_input_schema()
            ],
            "outputs": [
                output_schema.__dict__ for output_schema in node.get_output_schema()
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
        for node in self.node_instances.values():
            node.status = "pending"
            node.result = None
            node.error = None
        logger.info("워크플로우 상태 초기화 완료")

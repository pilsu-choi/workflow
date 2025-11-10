"""
워크플로우 실행 로그 관리 서비스 (Elasticsearch 전용)
모든 로그 데이터는 Elasticsearch에 저장되고 관리됩니다.
"""

# mypy: ignore-errors
# FIXME: mypy 오류 정정하기
import re
from datetime import datetime
from typing import Any, Dict, List

from dto.workflow.workflow_dto import WorkflowExecutionResult
from services.elasticsearch.es_client import ElasticsearchClient
from setting.logger import get_logger

logger = get_logger(__name__)


class WorkflowLogService:
    """워크플로우 실행 로그 관리 서비스 (Elasticsearch 전용)"""

    def __init__(self, es_client: ElasticsearchClient):
        self.es_client = es_client

    async def save_execution_log(
        self, graph_id: int, result: WorkflowExecutionResult
    ) -> Dict[str, Any]:
        """워크플로우 실행 결과를 Elasticsearch에 저장"""
        try:
            # 1. 실행 메타데이터 문서 생성
            execution_doc = {
                "doc_type": "execution_metadata",  # 문서 타입 구분
                "execution_id": result.execution_id,
                "graph_id": graph_id,
                "start_time": (
                    result.start_time.isoformat() if result.start_time else None
                ),
                "end_time": result.end_time.isoformat() if result.end_time else None,
                "execution_time": result.execution_time,
                "status": "success" if result.success else "failed",
                "success": result.success,
                "execution_order": result.execution_order,
                "node_results": result.node_results,
                "errors": result.errors,
                "created_at": datetime.now().isoformat(),
                "log_count": len(result.logs),
            }

            # 메타데이터 저장
            await self.es_client.index_log(result.execution_id, execution_doc)

            # 2. 상세 로그 메시지들을 개별 문서로 저장
            log_entries = self._parse_logs(graph_id, result)
            if log_entries:
                await self.es_client.bulk_index_logs(result.execution_id, log_entries)

            logger.info(
                f"Elasticsearch 로그 저장 완료: execution_id={result.execution_id}, "
                f"logs={len(log_entries)}개"
            )

            return {
                "execution_id": result.execution_id,
                "indexed": True,
                "log_count": len(log_entries),
            }

        except Exception as e:
            logger.error(f"워크플로우 실행 로그 저장 실패: {str(e)}", exc_info=True)
            raise

    def _parse_logs(
        self, graph_id: int, result: WorkflowExecutionResult
    ) -> List[Dict[str, Any]]:
        """로그 메시지를 파싱하여 Elasticsearch 문서로 변환"""
        log_entries = []
        sequence = 0

        for log_message in result.logs:
            # 로그 메시지 파싱
            # 형식: "[2025-11-06 12:00:00.000] 메시지"
            timestamp, level, message, node_id = self._parse_log_message(log_message)

            entry = {
                "doc_type": "log_message",  # 문서 타입
                "execution_id": result.execution_id,
                "graph_id": graph_id,
                "timestamp": timestamp,
                "level": level,
                "message": message,
                "node_id": node_id,
                "sequence": sequence,  # 로그 순서
            }

            log_entries.append(entry)
            sequence += 1

        # 에러 로그 추가
        for idx, error in enumerate(result.errors):
            entry = {
                "doc_type": "log_message",
                "execution_id": result.execution_id,
                "graph_id": graph_id,
                "timestamp": (
                    result.end_time.isoformat()
                    if result.end_time
                    else datetime.now().isoformat()
                ),
                "level": "ERROR",
                "message": error,
                "error": error,
                "sequence": sequence + idx,
            }
            log_entries.append(entry)

        return log_entries

    def _parse_log_message(self, log_message: str) -> tuple[str, str, str, str | None]:
        """로그 메시지를 파싱하여 구성 요소 추출"""
        # 형식: "[2025-11-06 12:00:00.000] 메시지"
        parts = log_message.split("]", 1)

        if len(parts) >= 2:
            timestamp_str = parts[0].strip("[")
            message = parts[1].strip()
        else:
            timestamp_str = datetime.now().isoformat()
            message = log_message

        # 로그 레벨 추출 (메시지에서 판단)
        level = self._detect_log_level(message)

        # 노드 ID 추출
        node_id = self._extract_node_id(message)

        return timestamp_str, level, message, node_id

    def _detect_log_level(self, message: str) -> str:
        """메시지 내용에서 로그 레벨 감지"""
        message_lower = message.lower()
        if (
            "실패" in message
            or "오류" in message
            or "에러" in message
            or "error" in message_lower
        ):
            return "ERROR"
        elif "경고" in message or "warning" in message_lower:
            return "WARNING"
        elif "디버그" in message or "debug" in message_lower:
            return "DEBUG"
        else:
            return "INFO"

    def _extract_node_id(self, message: str) -> str | None:
        """메시지에서 노드 ID 추출"""
        match = re.search(r"노드 (\w+)", message)
        return match.group(1) if match else None

    async def get_log_by_execution_id(
        self, execution_id: str, include_messages: bool = True
    ) -> Dict[str, Any] | None:
        """실행 ID로 로그 조회"""
        try:
            # 1. 메타데이터 조회
            metadata_results = await self.es_client.search_logs(
                execution_id=execution_id, size=1
            )

            # doc_type으로 메타데이터만 필터링
            metadata = None
            for result in metadata_results:
                if result.get("doc_type") == "execution_metadata":
                    metadata = result
                    break

            if not metadata:
                # 메타데이터가 없으면 로그 메시지에서 재구성
                all_logs = await self.es_client.search_logs(
                    execution_id=execution_id, size=10000
                )
                if not all_logs:
                    return None
                metadata = self._reconstruct_metadata_from_logs(execution_id, all_logs)

            # 2. 상세 로그 메시지 조회 (필요한 경우)
            if include_messages:
                log_messages = await self.es_client.search_logs(
                    execution_id=execution_id, size=10000
                )
                # doc_type으로 로그 메시지만 필터링
                log_messages = [
                    log for log in log_messages if log.get("doc_type") == "log_message"
                ]
                # 순서대로 정렬
                log_messages.sort(key=lambda x: x.get("sequence", 0))
            else:
                log_messages = []

            return {
                "metadata": metadata,
                "logs": log_messages,
                "log_count": len(log_messages),
            }

        except Exception as e:
            logger.error(f"로그 조회 실패 (execution_id={execution_id}): {str(e)}")
            return None

    def _reconstruct_metadata_from_logs(
        self, execution_id: str, logs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """로그 메시지들로부터 메타데이터 재구성"""
        if not logs:
            return {}

        # 타임스탬프 정렬
        sorted_logs = sorted(logs, key=lambda x: x.get("timestamp", ""))

        first_log = sorted_logs[0]
        last_log = sorted_logs[-1]

        # 에러 로그 수집
        errors = [log["message"] for log in logs if log.get("level") == "ERROR"]

        # 시간 계산
        try:
            start_time = datetime.fromisoformat(first_log["timestamp"])
            end_time = datetime.fromisoformat(last_log["timestamp"])
            execution_time = (end_time - start_time).total_seconds()
        except Exception as e:
            logger.error(f"시간 계산 실패: {str(e)}", exc_info=True)
            start_time = None
            end_time = None
            execution_time = None

        return {
            "doc_type": "execution_metadata",
            "execution_id": execution_id,
            "graph_id": first_log.get("graph_id"),
            "start_time": first_log.get("timestamp"),
            "end_time": last_log.get("timestamp"),
            "execution_time": execution_time,
            "status": "failed" if errors else "success",
            "success": len(errors) == 0,
            "errors": errors,
            "log_count": len(logs),
            "created_at": first_log.get("timestamp"),
        }

    async def get_logs_by_graph_id(
        self, graph_id: int, limit: int = 100, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """그래프 ID로 로그 목록 조회 (메타데이터만)"""
        try:
            # Elasticsearch에서 graph_id로 검색하되, 메타데이터만
            all_results = await self.es_client.search_logs(size=limit * 2)

            # 필터링: 해당 graph_id의 메타데이터만
            metadata_list = [
                result
                for result in all_results
                if result.get("graph_id") == graph_id
                and result.get("doc_type") == "execution_metadata"
            ]

            # 최신순 정렬
            metadata_list.sort(key=lambda x: x.get("created_at", ""), reverse=True)

            # 페이지네이션
            return metadata_list[offset : offset + limit]

        except Exception as e:
            logger.error(f"로그 목록 조회 실패 (graph_id={graph_id}): {str(e)}")
            return []

    async def get_all_logs(
        self, limit: int = 100, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """모든 로그 조회 (메타데이터만)"""
        try:
            # 모든 문서 조회
            all_results = await self.es_client.search_logs(size=limit * 2)

            # 메타데이터만 필터링
            metadata_list = [
                result
                for result in all_results
                if result.get("doc_type") == "execution_metadata"
            ]

            # 최신순 정렬
            metadata_list.sort(key=lambda x: x.get("created_at", ""), reverse=True)

            # 페이지네이션
            return metadata_list[offset : offset + limit]

        except Exception as e:
            logger.error(f"전체 로그 조회 실패: {str(e)}")
            return []

    async def search_logs(
        self,
        graph_id: int | None = None,
        query: str | None = None,
        level: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        limit: int = 100,
    ) -> Dict[str, Any]:
        """로그 검색 (전문 검색)"""
        try:
            # Elasticsearch 검색
            results = await self.es_client.search_logs(
                query=query,
                level=level,
                start_time=start_time,
                end_time=end_time,
                size=limit,
            )

            # graph_id 필터링 (필요한 경우)
            if graph_id is not None:
                results = [r for r in results if r.get("graph_id") == graph_id]

            # execution_id별로 그룹화
            executions = {}
            for result in results:
                exec_id = result.get("execution_id")
                if exec_id not in executions:
                    executions[exec_id] = {"metadata": None, "logs": []}

                if result.get("doc_type") == "execution_metadata":
                    executions[exec_id]["metadata"] = result
                else:
                    executions[exec_id]["logs"].append(result)

            return {
                "total": len(executions),
                "executions": executions,
                "raw_results": results,
            }

        except Exception as e:
            logger.error(f"로그 검색 실패: {str(e)}")
            return {"total": 0, "executions": {}, "raw_results": []}

    async def delete_log(self, execution_id: str) -> Dict[str, Any]:
        """로그 삭제"""
        try:
            await self.es_client.delete_logs_by_execution_id(execution_id)
            return {
                "success": True,
                "message": f"로그가 삭제되었습니다 (execution_id={execution_id})",
            }
        except Exception as e:
            logger.error(f"로그 삭제 실패 (execution_id={execution_id}): {str(e)}")
            return {"success": False, "error": str(e)}

    def format_log(self, log: Dict[str, Any]) -> Dict[str, Any]:
        """로그를 API 응답 형식으로 포맷"""
        # Elasticsearch 문서를 그대로 반환 (이미 적절한 형식)
        return log

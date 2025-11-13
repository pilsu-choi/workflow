"""WebSocket 메시지 처리 핸들러"""

from datetime import datetime
from typing import Any, Dict, Optional

from setting.logger import get_logger

logger = get_logger(__name__)


class WebSocketHandler:
    """WebSocket 메시지 처리 및 이벤트 생성 클래스"""

    @staticmethod
    def create_workflow_start_message(
        workflow_id: str, execution_id: str, execution_order: list[str]
    ) -> Dict[str, Any]:
        """
        워크플로우 시작 메시지 생성

        Args:
            workflow_id: 워크플로우 ID
            execution_id: 실행 ID
            execution_order: 노드 실행 순서

        Returns:
            메시지 dict
        """
        return {
            "type": "workflow_start",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "workflow_id": workflow_id,
                "execution_id": execution_id,
                "execution_order": execution_order,
                "total_nodes": len(execution_order),
            },
        }

    @staticmethod
    def create_workflow_complete_message(
        workflow_id: str,
        execution_id: str,
        success: bool,
        execution_time: float,
        errors: Optional[list[str]] = None,
    ) -> Dict[str, Any]:
        """
        워크플로우 완료 메시지 생성

        Args:
            workflow_id: 워크플로우 ID
            execution_id: 실행 ID
            success: 성공 여부
            execution_time: 실행 시간 (초)
            errors: 에러 메시지 목록

        Returns:
            메시지 dict
        """
        return {
            "type": "workflow_complete",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "workflow_id": workflow_id,
                "execution_id": execution_id,
                "success": success,
                "execution_time": execution_time,
                "errors": errors or [],
            },
        }

    @staticmethod
    def create_node_status_message(
        workflow_id: str,
        execution_id: str,
        node_id: str,
        status: str,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
        progress: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        노드 상태 변경 메시지 생성

        Args:
            workflow_id: 워크플로우 ID
            execution_id: 실행 ID
            node_id: 노드 ID
            status: 노드 상태 (pending, running, completed, error)
            result: 노드 실행 결과
            error: 에러 메시지
            progress: 진행률 (0-100)

        Returns:
            메시지 dict
        """
        return {
            "type": "node_status",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "workflow_id": workflow_id,
                "execution_id": execution_id,
                "node_id": node_id,
                "status": status,
                "result": result,
                "error": error,
                "progress": progress,
            },
        }

    @staticmethod
    def create_edge_flow_message(
        workflow_id: str,
        execution_id: str,
        source_node_id: str,
        target_node_id: str,
        edge_id: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        엣지 플로우 메시지 생성 (데이터 흐름 표시용)

        Args:
            workflow_id: 워크플로우 ID
            execution_id: 실행 ID
            source_node_id: 시작 노드 ID
            target_node_id: 종료 노드 ID
            edge_id: 엣지 ID
            data: 전달되는 데이터 (선택사항)

        Returns:
            메시지 dict
        """
        return {
            "type": "edge_flow",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "workflow_id": workflow_id,
                "execution_id": execution_id,
                "source_node_id": source_node_id,
                "target_node_id": target_node_id,
                "edge_id": edge_id,
                "data": data,
            },
        }

    @staticmethod
    def create_log_message(
        workflow_id: str, execution_id: str, message: str, level: str = "info"
    ) -> Dict[str, Any]:
        """
        로그 메시지 생성

        Args:
            workflow_id: 워크플로우 ID
            execution_id: 실행 ID
            message: 로그 메시지
            level: 로그 레벨 (info, warning, error)

        Returns:
            메시지 dict
        """
        return {
            "type": "log",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "workflow_id": workflow_id,
                "execution_id": execution_id,
                "level": level,
                "message": message,
            },
        }

    @staticmethod
    def create_error_message(
        workflow_id: str, execution_id: str, error: str, node_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        에러 메시지 생성

        Args:
            workflow_id: 워크플로우 ID
            execution_id: 실행 ID
            error: 에러 메시지
            node_id: 에러 발생 노드 ID (선택사항)

        Returns:
            메시지 dict
        """
        return {
            "type": "error",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "workflow_id": workflow_id,
                "execution_id": execution_id,
                "error": error,
                "node_id": node_id,
            },
        }

    @staticmethod
    def create_progress_message(
        workflow_id: str,
        execution_id: str,
        current_step: int,
        total_steps: int,
        current_node_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        진행률 메시지 생성

        Args:
            workflow_id: 워크플로우 ID
            execution_id: 실행 ID
            current_step: 현재 단계
            total_steps: 전체 단계 수
            current_node_id: 현재 실행 중인 노드 ID

        Returns:
            메시지 dict
        """
        progress = (current_step / total_steps * 100) if total_steps > 0 else 0
        return {
            "type": "progress",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "workflow_id": workflow_id,
                "execution_id": execution_id,
                "current_step": current_step,
                "total_steps": total_steps,
                "progress": round(progress, 2),
                "current_node_id": current_node_id,
            },
        }

"""WebSocket 연결 관리 모듈"""

import asyncio
from typing import Dict, Optional, Set

from fastapi import WebSocket, WebSocketDisconnect

from setting.logger import get_logger

logger = get_logger(__name__)


class WebSocketManager:
    """WebSocket 연결을 관리하는 클래스"""

    def __init__(self):
        # workflow_id별로 연결된 클라이언트들을 관리
        self.active_connections: Dict[str, Set[WebSocket]] = {}  # type: ignore
        # 전체 연결 (workflow_id 관계없이)
        self.all_connections: Set[WebSocket] = set()  # type: ignore
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, workflow_id: str) -> bool:
        """
        WebSocket 연결 수락 및 등록

        Args:
            websocket: WebSocket 연결 객체
            workflow_id: 워크플로우 ID

        Returns:
            연결 성공 여부
        """
        try:
            await websocket.accept()
            async with self._lock:
                # workflow_id별 연결 추가
                if workflow_id not in self.active_connections:
                    self.active_connections[workflow_id] = set()
                self.active_connections[workflow_id].add(websocket)

                # 전체 연결 목록에 추가
                self.all_connections.add(websocket)

            logger.info(
                f"WebSocket 연결 성공 - workflow_id: {workflow_id}, "
                f"현재 연결 수: {len(self.active_connections[workflow_id])}"
            )
            return True
        except Exception as e:
            logger.error(f"WebSocket 연결 실패: {str(e)}", exc_info=True)
            return False

    async def disconnect(self, websocket: WebSocket, workflow_id: str):
        """
        WebSocket 연결 해제

        Args:
            websocket: WebSocket 연결 객체
            workflow_id: 워크플로우 ID
        """
        async with self._lock:
            # workflow_id별 연결에서 제거
            if workflow_id in self.active_connections:
                self.active_connections[workflow_id].discard(websocket)
                # 해당 workflow_id에 연결이 없으면 키 삭제
                if not self.active_connections[workflow_id]:
                    del self.active_connections[workflow_id]

            # 전체 연결 목록에서 제거
            self.all_connections.discard(websocket)

        logger.info(
            f"WebSocket 연결 해제 - workflow_id: {workflow_id}, "
            f"남은 연결 수: {len(self.active_connections.get(workflow_id, []))}"
        )

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """
        특정 클라이언트에게 메시지 전송

        Args:
            message: 전송할 메시지 (dict)
            websocket: 대상 WebSocket 연결
        """
        try:
            await websocket.send_json(message)
        except WebSocketDisconnect:
            logger.warning("메시지 전송 중 연결이 끊어짐")
        except Exception as e:
            logger.error(f"개인 메시지 전송 실패: {str(e)}", exc_info=True)

    async def broadcast_to_workflow(self, message: dict, workflow_id: str):
        """
        특정 워크플로우를 구독하는 모든 클라이언트에게 메시지 전송

        Args:
            message: 전송할 메시지 (dict)
            workflow_id: 워크플로우 ID
        """
        if workflow_id not in self.active_connections:
            logger.debug(f"워크플로우 {workflow_id}에 연결된 클라이언트 없음")
            return

        disconnected = []
        connections = list(self.active_connections[workflow_id])

        for connection in connections:
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                disconnected.append(connection)
                logger.warning(
                    f"브로드캐스트 중 연결 끊어짐 - workflow_id: {workflow_id}"
                )
            except Exception as e:
                disconnected.append(connection)
                logger.error(f"메시지 전송 실패: {str(e)}", exc_info=True)

        # 끊어진 연결 정리
        if disconnected:
            async with self._lock:
                for conn in disconnected:
                    self.active_connections[workflow_id].discard(conn)
                    self.all_connections.discard(conn)

    async def broadcast_all(self, message: dict):
        """
        모든 연결된 클라이언트에게 메시지 전송

        Args:
            message: 전송할 메시지 (dict)
        """
        disconnected = []
        connections = list(self.all_connections)

        for connection in connections:
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                disconnected.append(connection)
                logger.warning("브로드캐스트 중 연결 끊어짐")
            except Exception as e:
                disconnected.append(connection)
                logger.error(f"메시지 전송 실패: {str(e)}", exc_info=True)

        # 끊어진 연결 정리
        if disconnected:
            async with self._lock:
                for conn in disconnected:
                    self.all_connections.discard(conn)
                    # 각 workflow_id에서도 제거
                    for workflow_id in list(self.active_connections.keys()):
                        self.active_connections[workflow_id].discard(conn)
                        if not self.active_connections[workflow_id]:
                            del self.active_connections[workflow_id]

    def get_connection_count(self, workflow_id: Optional[str] = None) -> int:
        """
        연결 수 조회

        Args:
            workflow_id: 워크플로우 ID (None이면 전체)

        Returns:
            연결 수
        """
        if workflow_id:
            return len(self.active_connections.get(workflow_id, []))
        return len(self.all_connections)

    def has_connections(self, workflow_id: str) -> bool:
        """
        특정 워크플로우에 연결된 클라이언트가 있는지 확인

        Args:
            workflow_id: 워크플로우 ID

        Returns:
            연결 존재 여부
        """
        return (
            workflow_id in self.active_connections
            and len(self.active_connections[workflow_id]) > 0
        )


# 전역 WebSocket 매니저 인스턴스
ws_manager = WebSocketManager()

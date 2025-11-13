from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from helpers.websockets.manager import ws_manager
from setting.logger import get_logger

router = APIRouter(prefix="/v1/ws", tags=["websocket"])
logger = get_logger(__name__)


# TODO: websocket 연결 엔드포인트 구성
@router.websocket("/workflow/{workflow_id}")
async def websocket_workflow_endpoint(websocket: WebSocket, workflow_id: str):
    """
    워크플로우 실행 상태를 실시간으로 받는 WebSocket 엔드포인트

    Args:
        websocket: WebSocket 연결
        workflow_id: 워크플로우 ID (graph_id)
    """
    # 연결 수락
    await ws_manager.connect(websocket, workflow_id)
    logger.info(f"WebSocket 연결 성공 - workflow_id: {workflow_id}")

    try:
        # 연결 유지 (클라이언트로부터 메시지를 받지만 처리는 하지 않음)
        # 서버에서 클라이언트로 push만 할 것임
        while True:
            # 클라이언트로부터 메시지를 받아서 연결 유지
            # ping/pong 같은 heartbeat 메시지를 주고받을 수 있음
            data = await websocket.receive_text()
            logger.debug(
                f"Received message from client (workflow_id: {workflow_id}): {data}"
            )

            # 필요하다면 여기서 클라이언트 메시지 처리
            # 예: ping 요청에 pong 응답
            if data == "ping":
                await websocket.send_json({"type": "pong", "workflow_id": workflow_id})

    except WebSocketDisconnect:
        logger.info(f"WebSocket 연결 해제 - workflow_id: {workflow_id}")
    except Exception as e:
        logger.error(
            f"WebSocket 에러 - workflow_id: {workflow_id}: {str(e)}", exc_info=True
        )
    finally:
        # 연결 해제
        await ws_manager.disconnect(websocket, workflow_id)

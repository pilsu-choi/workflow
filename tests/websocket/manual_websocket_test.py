"""
수동 WebSocket 테스트 스크립트

실제 서버를 실행한 상태에서 WebSocket 연결을 테스트합니다.

사용법:
1. 먼저 서버 실행: python main.py
2. 다른 터미널에서 이 스크립트 실행: python tests/manual_websocket_test.py
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

import websockets

# 프로젝트 루트를 Python path에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class WebSocketTestClient:
    """WebSocket 테스트 클라이언트"""

    def __init__(self, workflow_id: str, base_url: str = "ws://localhost:8000"):
        self.workflow_id = workflow_id
        self.base_url = base_url
        self.websocket = None
        self.messages = []  # type: ignore

    async def connect(self):
        """WebSocket 연결"""
        url = f"{self.base_url}/api/v1/ws/workflow/{self.workflow_id}"
        print(f"\n🔌 WebSocket 연결 중: {url}")
        self.websocket = await websockets.connect(url)
        print("✅ WebSocket 연결 성공!")

    async def disconnect(self):
        """WebSocket 연결 해제"""
        if self.websocket:
            await self.websocket.close()
            print("\n🔌 WebSocket 연결 해제")

    async def send_ping(self):
        """Ping 전송"""
        print("\n📤 Ping 전송...")
        await self.websocket.send("ping")

    async def receive_message(self, timeout=None):
        """메시지 수신"""
        try:
            if timeout:
                message = await asyncio.wait_for(self.websocket.recv(), timeout=timeout)
            else:
                message = await self.websocket.recv()

            data = json.loads(message)
            self.messages.append(data)
            self._print_message(data)
            return data
        except asyncio.TimeoutError:
            print("⏱️  메시지 수신 타임아웃")
            return None
        except Exception as e:
            print(f"❌ 메시지 수신 에러: {e}")
            return None

    async def listen(self, duration=None):
        """메시지 수신 대기"""
        print("\n👂 메시지 수신 대기 중... (Ctrl+C로 중지)")
        try:
            start_time = datetime.now()
            while True:
                if duration and (datetime.now() - start_time).seconds >= duration:
                    print(f"\n⏱️  {duration}초 경과. 수신 대기 종료.")
                    break

                message = await self.receive_message(timeout=1)
                if message is None:
                    continue

        except KeyboardInterrupt:
            print("\n\n⏹️  수신 대기 중지")
        except Exception as e:
            print(f"\n❌ 에러 발생: {e}")

    def _print_message(self, data: dict):
        """메시지 출력"""
        msg_type = data.get("type", "unknown")
        timestamp = data.get("timestamp", "")

        print(f"\n📨 메시지 수신 [{msg_type}] at {timestamp}")

        if msg_type == "workflow_start":
            print("   ✨ 워크플로우 시작")
            print(f"   - Execution ID: {data['data']['execution_id']}")
            print(f"   - 노드 수: {data['data']['total_nodes']}")
            print(f"   - 실행 순서: {data['data']['execution_order']}")

        elif msg_type == "workflow_complete":
            print("   🏁 워크플로우 완료")
            print(f"   - 성공: {data['data']['success']}")
            print(f"   - 실행 시간: {data['data']['execution_time']:.2f}초")
            if data["data"]["errors"]:
                print(f"   - 에러: {data['data']['errors']}")

        elif msg_type == "node_status":
            node_id = data["data"]["node_id"]
            status = data["data"]["status"]
            emoji = {
                "pending": "⏳",
                "running": "🔄",
                "completed": "✅",
                "error": "❌",
            }.get(status, "❓")
            print(f"   {emoji} 노드 [{node_id}] → {status}")

            if status == "completed" and data["data"].get("result"):
                print(
                    f"   - 결과: {json.dumps(data['data']['result'], indent=2, ensure_ascii=False)}"
                )

            if status == "error" and data["data"].get("error"):
                print(f"   - 에러: {data['data']['error']}")

        elif msg_type == "edge_flow":
            source = data["data"]["source_node_id"]
            target = data["data"]["target_node_id"]
            print(f"   ➡️  데이터 흐름: {source} → {target}")

        elif msg_type == "progress":
            progress = data["data"]["progress"]
            current = data["data"]["current_step"]
            total = data["data"]["total_steps"]
            print(f"   📊 진행률: {progress:.1f}% ({current}/{total})")
            print(f"   - 현재 노드: {data['data']['current_node_id']}")

        elif msg_type == "log":
            level = data["data"]["level"]
            message = data["data"]["message"]
            emoji = {"info": "ℹ️", "warning": "⚠️", "error": "❌"}.get(level, "📝")
            print(f"   {emoji} [{level.upper()}] {message}")

        elif msg_type == "error":
            print(f"   ❌ 에러 발생: {data['data']['error']}")
            if data["data"].get("node_id"):
                print(f"   - 노드: {data['data']['node_id']}")

        elif msg_type == "pong":
            print("   🏓 Pong 수신")

        else:
            print(f"   📄 데이터: {json.dumps(data, indent=2, ensure_ascii=False)}")

    def print_summary(self):
        """수신한 메시지 요약 출력"""
        print("\n" + "=" * 60)
        print("📊 메시지 수신 요약")
        print("=" * 60)

        message_counts = {}
        for msg in self.messages:
            msg_type = msg.get("type", "unknown")
            message_counts[msg_type] = message_counts.get(msg_type, 0) + 1

        print(f"\n총 수신 메시지 수: {len(self.messages)}")
        print("\n메시지 타입별 수:")
        for msg_type, count in sorted(message_counts.items()):
            print(f"  - {msg_type}: {count}개")


async def test_basic_connection():
    """기본 연결 테스트"""
    print("\n" + "=" * 60)
    print("🧪 테스트 1: 기본 WebSocket 연결")
    print("=" * 60)

    client = WebSocketTestClient(workflow_id="2")

    try:
        await client.connect()
        await client.send_ping()
        message = await client.receive_message(timeout=3)

        if message and message["type"] == "pong":
            print("\n✅ Ping/Pong 테스트 성공!")
        else:
            print("\n❌ Ping/Pong 테스트 실패")

    finally:
        await client.disconnect()


async def test_workflow_execution_monitoring():
    """워크플로우 실행 모니터링 테스트"""
    print("\n" + "=" * 60)
    print("🧪 테스트 2: 워크플로우 실행 모니터링")
    print("=" * 60)
    print("\n⚠️  이 테스트를 실행하려면:")
    print("   1. 다른 터미널에서 워크플로우를 실행하세요")
    print("   2. 예: curl -X POST http://localhost:8000/api/v1/workflows/123/execute")
    print("   3. 또는 30초 대기 후 자동 종료됩니다")

    client = WebSocketTestClient(workflow_id="2")

    try:
        await client.connect()
        await client.listen(duration=30)  # 30초 동안 대기
        client.print_summary()

    finally:
        await client.disconnect()


async def test_multiple_connections():
    """여러 클라이언트 동시 연결 테스트"""
    print("\n" + "=" * 60)
    print("🧪 테스트 3: 여러 클라이언트 동시 연결")
    print("=" * 60)

    client1 = WebSocketTestClient(workflow_id="2")
    client2 = WebSocketTestClient(workflow_id="2")

    try:
        print("\n클라이언트 1 연결...")
        await client1.connect()

        print("\n클라이언트 2 연결...")
        await client2.connect()

        print("\n✅ 두 클라이언트 모두 연결 성공!")

        # 각각 ping 전송
        await client1.send_ping()
        msg1 = await client1.receive_message(timeout=3)

        await client2.send_ping()
        msg2 = await client2.receive_message(timeout=3)

        if msg1 and msg2 and msg1["type"] == "pong" and msg2["type"] == "pong":
            print("\n✅ 두 클라이언트 모두 정상 작동!")

    finally:
        await client1.disconnect()
        await client2.disconnect()


async def main():
    """메인 함수"""
    print("\n" + "=" * 60)
    print("🚀 WebSocket 테스트 시작")
    print("=" * 60)
    print("\n⚠️  서버가 실행 중인지 확인하세요!")
    print("   서버 실행: python main.py")
    print("=" * 60)

    try:
        # 테스트 1: 기본 연결
        await test_basic_connection()

        # 테스트 3: 여러 클라이언트
        await test_multiple_connections()

        # 테스트 2: 워크플로우 실행 모니터링 (마지막에 실행)
        choice = input("\n워크플로우 실행 모니터링 테스트를 실행하시겠습니까? (y/n): ")
        if choice.lower() == "y":
            await test_workflow_execution_monitoring()

        print("\n" + "=" * 60)
        print("✅ 모든 테스트 완료!")
        print("=" * 60)

    except ConnectionRefusedError:
        print("\n❌ 서버에 연결할 수 없습니다!")
        print("   서버가 실행 중인지 확인하세요: python main.py")
    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    print("\n🔧 필요한 패키지 설치:")
    print("   pip install websockets")
    print()

    asyncio.run(main())

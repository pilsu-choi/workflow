# WebSocket 구현 요약

워크플로우 실행 시 실시간으로 노드 실행 상태를 프론트엔드에 전송하는 WebSocket 시스템이 구현되었습니다.

## 📁 구현된 파일

### 핵심 모듈
```
helpers/websockets/
├── __init__.py              # 모듈 exports
├── manager.py               # WebSocket 연결 관리 (189 lines)
├── handler.py               # 메시지 생성 헬퍼 (236 lines)
└── README.md               # 사용 가이드 (448 lines)
```

### 통합 파일
```
helpers/engine/
└── workflow_engine.py       # WebSocket 통합 (422 lines)
    - WorkflowEngine에 WebSocket 전송 기능 추가
    - 노드 상태 변경 시 자동 메시지 전송
    - 간선 플로우 애니메이션용 메시지 전송

services/workflow/
└── workflow_execution_service.py  # 서비스 레이어 통합
    - workflow_id별 엔진 관리
    - WebSocket 활성화/비활성화 제어

routers/v1/graph/
└── workflow_router.py       # WebSocket 엔드포인트 추가
    - ws://localhost:8000/api/v1/ws/workflow/{workflow_id}

main.py                      # 라우터 등록 (이미 완료)
```

### 테스트 파일
```
tests/
├── test_websocket.py                          # Pytest 자동 테스트 (367 lines)
├── manual_websocket_test.py                   # 수동 대화형 테스트 (267 lines)
├── integration_websocket_workflow_test.py     # 통합 테스트 (332 lines)
├── WEBSOCKET_TEST_GUIDE.md                   # 테스트 가이드 (395 lines)
└── run_websocket_tests.sh                     # 테스트 실행 스크립트 (203 lines)
```

## 🎯 주요 기능

### 1. WebSocket Manager (`manager.py`)
- ✅ workflow_id별 클라이언트 그룹 관리
- ✅ 연결/해제 자동 관리
- ✅ 브로드캐스트 (워크플로우별, 전체)
- ✅ 개인 메시지 전송
- ✅ 연결 상태 추적
- ✅ 에러 처리 및 자동 정리

### 2. WebSocket Handler (`handler.py`)
7가지 메시지 타입 생성 헬퍼:

| 메시지 타입 | 설명 | 전송 시점 |
|------------|------|----------|
| `workflow_start` | 워크플로우 시작 | 실행 시작 시 |
| `workflow_complete` | 워크플로우 완료 | 실행 완료 시 |
| `node_status` | 노드 상태 변경 | 노드 상태 변경 시 |
| `edge_flow` | 간선 데이터 흐름 | 노드 완료 → 다음 노드 전달 시 |
| `progress` | 전체 진행률 | 각 노드 시작 시 |
| `log` | 로그 메시지 | 필요 시 |
| `error` | 에러 발생 | 에러 발생 시 |

### 3. WorkflowEngine 통합
- ✅ 노드 실행 시작: `running` 상태 전송
- ✅ 노드 실행 완료: `completed` 상태 + 결과 전송
- ✅ 노드 실행 실패: `error` 상태 + 에러 메시지 전송
- ✅ 간선 플로우: 노드 완료 후 다음 노드로의 데이터 흐름 알림
- ✅ 진행률: 전체 워크플로우 진행률 업데이트
- ✅ WebSocket 활성화/비활성화 옵션

## 🔌 WebSocket 엔드포인트

```
ws://localhost:8000/api/v1/ws/workflow/{workflow_id}
```

### 연결 예시 (JavaScript)
```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/ws/workflow/123');

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log(message.type, message.data);
};
```

## 📨 메시지 포맷

### 노드 상태 변경 예시
```json
{
  "type": "node_status",
  "timestamp": "2025-11-13T10:30:02.123456",
  "data": {
    "workflow_id": "123",
    "execution_id": "uuid-string",
    "node_id": "node1",
    "status": "running",
    "result": null,
    "error": null,
    "progress": null
  }
}
```

### 간선 플로우 예시
```json
{
  "type": "edge_flow",
  "timestamp": "2025-11-13T10:30:02.456789",
  "data": {
    "workflow_id": "123",
    "execution_id": "uuid-string",
    "source_node_id": "node1",
    "target_node_id": "node2",
    "edge_id": null,
    "data": null
  }
}
```

## 🧪 테스트

### 빠른 시작

```bash
# 1. 서버 실행
python main.py

# 2. 테스트 스크립트 실행 (대화형)
./run_websocket_tests.sh

# 또는 직접 pytest 실행
pytest tests/test_websocket.py -v
```

### 테스트 커버리지

#### 자동 테스트 (Pytest)
- ✅ WebSocket 연결/해제
- ✅ Ping/Pong 통신
- ✅ 여러 클라이언트 동시 연결
- ✅ 메시지 구조 검증 (7가지 타입)
- ✅ Manager 기능 (연결 관리, 브로드캐스트)
- ✅ 통합 테스트 (워크플로우 실행)
- ✅ 에러 처리 및 재연결

#### 수동 테스트
- ✅ 대화형 연결 테스트
- ✅ 워크플로우 실행 모니터링
- ✅ 여러 클라이언트 동시 연결

#### 통합 테스트
- ✅ 워크플로우 자동 생성
- ✅ 실시간 메시지 수신
- ✅ 메시지 분석 및 검증
- ✅ 자동 정리

## 🎨 프론트엔드 구현 가이드

### 1. React Hook 예시

```typescript
export const useWorkflowWebSocket = (workflowId: string) => {
  const [nodeStatuses, setNodeStatuses] = useState<NodeStatus>({});
  const [edgeFlows, setEdgeFlows] = useState<EdgeFlow[]>([]);
  const [progress, setProgress] = useState<number>(0);

  useEffect(() => {
    const ws = new WebSocket(
      `ws://localhost:8000/api/v1/ws/workflow/${workflowId}`
    );

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      
      switch (message.type) {
        case 'node_status':
          setNodeStatuses(prev => ({
            ...prev,
            [message.data.node_id]: message.data
          }));
          break;
          
        case 'edge_flow':
          // 간선 애니메이션 트리거
          setEdgeFlows(prev => [...prev, message.data]);
          setTimeout(() => {
            setEdgeFlows(prev => 
              prev.filter(f => f !== message.data)
            );
          }, 3000);
          break;
          
        case 'progress':
          setProgress(message.data.progress);
          break;
      }
    };

    return () => ws.close();
  }, [workflowId]);

  return { nodeStatuses, edgeFlows, progress };
};
```

### 2. UI 시각화 권장사항

#### 노드 상태별 색상
```css
.node-pending   { fill: #cccccc; }  /* 회색 */
.node-running   { fill: #ffcc00; }  /* 노란색 + 애니메이션 */
.node-completed { fill: #00ff00; }  /* 초록색 */
.node-error     { fill: #ff0000; }  /* 빨간색 */
```

#### 간선 플로우 애니메이션
```css
.edge-flow {
  stroke: #00ff00;
  stroke-width: 3;
  animation: flow-animation 1s ease-in-out;
}

@keyframes flow-animation {
  0% { stroke-dashoffset: 100; opacity: 0.5; }
  50% { opacity: 1; }
  100% { stroke-dashoffset: 0; opacity: 0.5; }
}
```

## 📊 아키텍처

```
Frontend (React)
    ↓ WebSocket
    ↓ ws://localhost:8000/api/v1/ws/workflow/{workflow_id}
    ↓
WebSocket Router (workflow_router.py)
    ↓
WebSocket Manager (manager.py)
    ↑ broadcast_to_workflow()
    ↑
WorkflowEngine (workflow_engine.py)
    ↓ _send_node_status()
    ↓ _send_edge_flows()
    ↓ _send_progress()
    ↓
WebSocket Handler (handler.py)
    ↓ create_*_message()
    ↓
Frontend (메시지 수신 및 UI 업데이트)
```

## 🚀 사용 방법

### 백엔드 (자동)
```python
# WorkflowEngine은 자동으로 WebSocket 메시지 전송
engine = WorkflowEngine(workflow_id="123", enable_websocket=True)
await engine.start()  # 실행 중 자동으로 메시지 전송
```

### 프론트엔드 (구현 필요)
```javascript
// 1. WebSocket 연결
const ws = new WebSocket(`ws://localhost:8000/api/v1/ws/workflow/${workflowId}`);

// 2. 메시지 수신
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  handleMessage(message);
};

// 3. 워크플로우 실행
fetch(`http://localhost:8000/api/v1/workflows/${workflowId}/execute`, {
  method: 'POST',
  body: JSON.stringify({ initial_inputs: {} })
});

// 4. 실시간으로 노드 상태 및 간선 플로우 업데이트
```

## ✅ 완료된 작업

1. ✅ WebSocket Manager 구현 (연결 관리)
2. ✅ WebSocket Handler 구현 (7가지 메시지 타입)
3. ✅ WorkflowEngine에 WebSocket 통합
4. ✅ WebSocket 라우터 구현
5. ✅ WorkflowExecutionService 개선
6. ✅ 자동 테스트 작성 (Pytest)
7. ✅ 수동 테스트 스크립트 작성
8. ✅ 통합 테스트 스크립트 작성
9. ✅ 테스트 가이드 문서 작성
10. ✅ 사용 가이드 문서 작성
11. ✅ 테스트 실행 스크립트 작성

## 🔜 다음 단계 (프론트엔드)

1. [ ] React에서 WebSocket 클라이언트 구현
2. [ ] 노드 상태 변경 시 UI 업데이트
3. [ ] 간선 플로우 애니메이션 구현
4. [ ] 진행률 표시 (프로그레스 바)
5. [ ] 에러 처리 및 표시
6. [ ] 재연결 로직 구현
7. [ ] Heartbeat (ping/pong) 구현

## 📚 참고 문서

- **사용 가이드**: `/helpers/websockets/README.md`
- **테스트 가이드**: `/tests/WEBSOCKET_TEST_GUIDE.md`
- **이 요약 문서**: `/WEBSOCKET_IMPLEMENTATION_SUMMARY.md`

## 🎉 결과

이제 워크플로우를 실행하면:

1. 📡 WebSocket을 통해 실시간으로 노드 상태 전송
2. 🎨 프론트엔드에서 노드 색상 변경 (pending → running → completed)
3. ➡️  간선에 플로우 애니메이션 표시
4. 📊 전체 진행률 업데이트
5. ❌ 에러 발생 시 즉시 알림

**모든 백엔드 구현이 완료되었습니다!** 🚀

프론트엔드에서 WebSocket 클라이언트를 구현하면 실시간으로 워크플로우 실행 상태를 시각화할 수 있습니다.


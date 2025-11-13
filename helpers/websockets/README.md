# WebSocket 실시간 워크플로우 상태 전송

워크플로우 실행 시 노드의 실행 상태를 실시간으로 프론트엔드에 전송하는 WebSocket 모듈입니다.

## 📁 파일 구조

```
helpers/websockets/
├── __init__.py          # 모듈 exports
├── manager.py           # WebSocket 연결 관리
├── handler.py           # 메시지 생성 및 처리
└── README.md           # 이 문서
```

## 🔌 WebSocket 엔드포인트

```
ws://localhost:8000/api/ws/workflow/{workflow_id}
```

- `workflow_id`: 워크플로우(그래프) ID (graph_id)

## 📨 메시지 타입

### 1. 워크플로우 시작 (`workflow_start`)

워크플로우 실행이 시작될 때 전송됩니다.

```json
{
  "type": "workflow_start",
  "timestamp": "2025-11-13T10:30:00.123456",
  "data": {
    "workflow_id": "123",
    "execution_id": "uuid-string",
    "execution_order": ["node1", "node2", "node3"],
    "total_nodes": 3
  }
}
```

### 2. 워크플로우 완료 (`workflow_complete`)

워크플로우 실행이 완료될 때 전송됩니다.

```json
{
  "type": "workflow_complete",
  "timestamp": "2025-11-13T10:30:05.123456",
  "data": {
    "workflow_id": "123",
    "execution_id": "uuid-string",
    "success": true,
    "execution_time": 5.23,
    "errors": []
  }
}
```

### 3. 노드 상태 변경 (`node_status`)

노드의 실행 상태가 변경될 때 전송됩니다.

**상태 값:**
- `pending`: 대기 중
- `running`: 실행 중
- `completed`: 완료
- `error`: 에러

```json
{
  "type": "node_status",
  "timestamp": "2025-11-13T10:30:02.123456",
  "data": {
    "workflow_id": "123",
    "execution_id": "uuid-string",
    "node_id": "node1",
    "status": "running",  // or "completed", "error"
    "result": { /* 노드 실행 결과 */ },  // status가 "completed"일 때
    "error": "에러 메시지",  // status가 "error"일 때
    "progress": null
  }
}
```

### 4. 엣지 플로우 (`edge_flow`)

노드 간 데이터 흐름을 표시할 때 전송됩니다. 노드 실행 완료 후 다음 노드로 데이터가 전달됨을 알립니다.

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

### 5. 진행률 (`progress`)

전체 워크플로우 진행률을 전송합니다.

```json
{
  "type": "progress",
  "timestamp": "2025-11-13T10:30:02.123456",
  "data": {
    "workflow_id": "123",
    "execution_id": "uuid-string",
    "current_step": 2,
    "total_steps": 5,
    "progress": 40.0,
    "current_node_id": "node2"
  }
}
```

### 6. 로그 (`log`)

워크플로우 실행 중 로그 메시지를 전송합니다.

```json
{
  "type": "log",
  "timestamp": "2025-11-13T10:30:02.123456",
  "data": {
    "workflow_id": "123",
    "execution_id": "uuid-string",
    "level": "info",  // "info", "warning", "error"
    "message": "로그 메시지"
  }
}
```

### 7. 에러 (`error`)

워크플로우 실행 중 에러가 발생했을 때 전송됩니다.

```json
{
  "type": "error",
  "timestamp": "2025-11-13T10:30:02.123456",
  "data": {
    "workflow_id": "123",
    "execution_id": "uuid-string",
    "error": "에러 메시지",
    "node_id": "node1"  // 에러 발생 노드 (선택사항)
  }
}
```

## 💻 프론트엔드 사용 예시

### React/TypeScript 예시

```typescript
import { useEffect, useState } from 'react';

interface NodeStatus {
  [nodeId: string]: {
    status: 'pending' | 'running' | 'completed' | 'error';
    result?: any;
    error?: string;
  };
}

interface EdgeFlow {
  sourceNodeId: string;
  targetNodeId: string;
  timestamp: string;
}

export const useWorkflowWebSocket = (workflowId: string) => {
  const [nodeStatuses, setNodeStatuses] = useState<NodeStatus>({});
  const [edgeFlows, setEdgeFlows] = useState<EdgeFlow[]>([]);
  const [progress, setProgress] = useState<number>(0);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/api/ws/workflow/${workflowId}`);

    ws.onopen = () => {
      console.log('WebSocket connected');
      setIsConnected(true);
      
      // Heartbeat: 주기적으로 ping 전송
      const interval = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
          ws.send('ping');
        }
      }, 30000); // 30초마다

      return () => clearInterval(interval);
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      
      switch (message.type) {
        case 'workflow_start':
          console.log('Workflow started:', message.data);
          // 모든 노드를 pending 상태로 초기화
          const initialStatuses: NodeStatus = {};
          message.data.execution_order.forEach((nodeId: string) => {
            initialStatuses[nodeId] = { status: 'pending' };
          });
          setNodeStatuses(initialStatuses);
          setEdgeFlows([]);
          setProgress(0);
          break;

        case 'workflow_complete':
          console.log('Workflow completed:', message.data);
          setProgress(100);
          break;

        case 'node_status':
          console.log('Node status changed:', message.data);
          setNodeStatuses(prev => ({
            ...prev,
            [message.data.node_id]: {
              status: message.data.status,
              result: message.data.result,
              error: message.data.error,
            }
          }));
          break;

        case 'edge_flow':
          console.log('Edge flow:', message.data);
          setEdgeFlows(prev => [...prev, {
            sourceNodeId: message.data.source_node_id,
            targetNodeId: message.data.target_node_id,
            timestamp: message.timestamp,
          }]);
          
          // 애니메이션 후 제거 (3초 후)
          setTimeout(() => {
            setEdgeFlows(prev => prev.filter(
              flow => flow.timestamp !== message.timestamp
            ));
          }, 3000);
          break;

        case 'progress':
          console.log('Progress:', message.data);
          setProgress(message.data.progress);
          break;

        case 'error':
          console.error('Workflow error:', message.data);
          break;

        case 'pong':
          // Heartbeat 응답
          console.log('pong received');
          break;
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
    };

    return () => {
      ws.close();
    };
  }, [workflowId]);

  return { nodeStatuses, edgeFlows, progress, isConnected };
};
```

### 간선 애니메이션 예시 (CSS)

```css
/* 간선이 활성화될 때 애니메이션 */
.edge-flow {
  stroke: #00ff00;
  stroke-width: 3;
  animation: flow-animation 1s ease-in-out;
}

@keyframes flow-animation {
  0% {
    stroke-dashoffset: 100;
    stroke-dasharray: 10 5;
    opacity: 0.5;
  }
  50% {
    opacity: 1;
  }
  100% {
    stroke-dashoffset: 0;
    opacity: 0.5;
  }
}

/* 노드 상태별 스타일 */
.node-pending {
  fill: #cccccc;
}

.node-running {
  fill: #ffcc00;
  animation: pulse 1s infinite;
}

.node-completed {
  fill: #00ff00;
}

.node-error {
  fill: #ff0000;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
}
```

## 🔧 백엔드 사용 방법

### WorkflowEngine에 WebSocket 통합

`WorkflowEngine`은 자동으로 WebSocket을 통해 상태를 전송합니다.

```python
from helpers.engine.workflow_engine import WorkflowEngine

# WebSocket 활성화 (기본값)
engine = WorkflowEngine(workflow_id="123", enable_websocket=True)

# WebSocket 비활성화 (테스트나 백그라운드 작업용)
engine = WorkflowEngine(workflow_id="123", enable_websocket=False)
```

### 수동으로 메시지 전송

필요한 경우 직접 메시지를 전송할 수 있습니다.

```python
from helpers.websockets import ws_manager, WebSocketHandler

# 특정 워크플로우 구독자들에게 메시지 전송
message = WebSocketHandler.create_node_status_message(
    workflow_id="123",
    execution_id="uuid",
    node_id="node1",
    status="running"
)
await ws_manager.broadcast_to_workflow(message, workflow_id="123")

# 모든 연결된 클라이언트에게 메시지 전송
await ws_manager.broadcast_all(message)

# 특정 클라이언트에게만 메시지 전송
await ws_manager.send_personal_message(message, websocket)
```

## 🎯 UI 구현 권장사항

### 노드 시각화
1. **pending**: 회색 - 대기 중
2. **running**: 노란색 + 펄스 애니메이션 - 실행 중
3. **completed**: 초록색 - 완료
4. **error**: 빨간색 - 에러

### 간선(Edge) 애니메이션
1. `edge_flow` 메시지를 받으면 해당 간선에 흐름 애니메이션 표시
2. 애니메이션은 source → target 방향으로 진행
3. 2-3초 후 애니메이션 제거

### 진행률 표시
1. 전체 워크플로우 진행률을 프로그레스 바로 표시
2. 현재 실행 중인 노드 강조

### 에러 처리
1. 에러 발생 시 노드를 빨간색으로 표시
2. 에러 메시지를 툴팁이나 모달로 표시
3. 워크플로우 실행 중단

## 🧪 테스트

### WebSocket 연결 테스트

```bash
# wscat 설치
npm install -g wscat

# WebSocket 연결
wscat -c ws://localhost:8000/api/ws/workflow/123

# 연결 후 ping 전송
> ping
< {"type": "pong", "workflow_id": "123"}
```

### 워크플로우 실행 및 WebSocket 모니터링

1. WebSocket 연결
```bash
wscat -c ws://localhost:8000/api/ws/workflow/123
```

2. 다른 터미널에서 워크플로우 실행
```bash
curl -X POST "http://localhost:8000/api/workflows/123/execute" \
  -H "Content-Type: application/json" \
  -d '{"initial_inputs": {}}'
```

3. WebSocket에서 실시간 메시지 확인

## 📝 주의사항

1. **연결 유지**: 클라이언트는 주기적으로 ping을 전송하여 연결을 유지해야 합니다.
2. **재연결**: 연결이 끊어지면 자동으로 재연결 로직을 구현하세요.
3. **메모리 관리**: 워크플로우 실행이 완료되면 엔진 인스턴스를 정리합니다.
4. **동시 실행**: 여러 워크플로우를 동시에 실행할 수 있으며, 각각 독립적으로 관리됩니다.
5. **보안**: 프로덕션 환경에서는 WebSocket 인증을 추가해야 합니다.

## 🚀 향후 개선 사항

- [ ] WebSocket 인증 및 권한 관리
- [ ] 메시지 압축 (대용량 결과 데이터)
- [ ] 재연결 시 이전 상태 복구
- [ ] 워크플로우 일시정지/재개 기능
- [ ] 실시간 로그 스트리밍
- [ ] 성능 메트릭 전송 (메모리, CPU 사용량 등)


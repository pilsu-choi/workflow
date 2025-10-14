# Services Architecture

## 📊 서비스 구조 개요

이 문서는 Graph와 Workflow 개념을 명확히 분리한 새로운 서비스 아키텍처를 설명합니다.

## 🏗️ 서비스 계층 구조

```
Services/
├── graph/                          # Graph 메타데이터 관리
│   ├── graph_service.py           # Graph CRUD 전용 서비스
│   ├── vertex_service.py          # Vertex CRUD 서비스
│   └── edge_service.py            # Edge CRUD 서비스
└── workflow/                       # Workflow 실행 및 영속성
    ├── workflow_persistence_service.py  # 워크플로우 저장/로드
    └── workflow_execution_service.py    # 워크플로우 실행
```

## 🎯 서비스별 책임

### 1. GraphService
**역할**: Graph 메타데이터 관리 전용
- Graph CRUD 작업 (생성, 조회, 수정, 삭제)
- 워크플로우 관련 작업은 다른 서비스에 위임

```python
# Graph 메타데이터만 관리
async def get_graphs() -> List[Graph]
async def get_graph(graph_id: int) -> Graph
async def create_graph(graph: Graph) -> Graph
async def update_graph(graph_id: int, graph: Graph) -> Graph
async def delete_graph_metadata(graph_id: int) -> Dict[str, Any]

# 워크플로우 작업은 위임
async def save_workflow() -> persistence_service.save_workflow()
async def execute_workflow() -> execution_service.execute_workflow()
```

### 2. WorkflowPersistenceService
**역할**: 워크플로우 영속성 관리
- 워크플로우 저장 (Graph + Vertices + Edges)
- 워크플로우 로드
- 워크플로우 삭제 (완전 삭제)

```python
async def save_workflow(graph, vertices, edges) -> Graph
async def load_workflow(graph_id) -> Tuple[Graph, List[Vertex], List[Edge]]
async def delete_workflow(graph_id) -> Dict[str, Any]
```

### 3. WorkflowExecutionService
**역할**: 워크플로우 실행 및 상태 관리
- 워크플로우 실행
- 실행 상태 조회
- 노드별 상태 조회

```python
async def execute_workflow(graph_id, initial_inputs) -> Dict[str, Any]
async def get_workflow_status(graph_id) -> Dict[str, Any]
async def get_node_status(graph_id, node_id) -> Dict[str, Any]
```

## 🔄 Graph vs Workflow 구분

### Graph (데이터 구조)
- **정의**: 워크플로우의 메타데이터 컨테이너
- **내용**: 이름, 설명, 생성일시, 속성 등
- **용도**: 식별, 분류, 관리

### Workflow (실행 가능한 프로세스)
- **정의**: Graph + Vertices + Edges + 실행 로직
- **내용**: 노드 인스턴스, 의존성 그래프, 실행 컨텍스트
- **용도**: 실제 비즈니스 로직 실행

## 📡 API 엔드포인트 구분

### Graph 메타데이터 전용
```
GET    /workflows/{graph_id}/metadata     # 그래프 메타데이터만 조회
DELETE /workflows/{graph_id}/metadata     # 그래프 메타데이터만 삭제
```

### Workflow 관련
```
POST   /workflows/                        # 워크플로우 생성 (Graph + Vertices + Edges)
GET    /workflows/{graph_id}              # 워크플로우 전체 조회
POST   /workflows/{graph_id}/execute      # 워크플로우 실행
GET    /workflows/{graph_id}/status       # 워크플로우 상태 조회
DELETE /workflows/{graph_id}              # 워크플로우 완전 삭제
```

### 노드 관련
```
GET    /workflows/{graph_id}/nodes/{node_id}/status  # 노드 상태 조회
```

## 🔧 의존성 주입 구조

```python
# 독립적인 의존성 체인
get_graph_repository() 
    ↓
get_graph_service(graph_repository)  # Graph 메타데이터만 관리

get_graph_repository() + get_vertex_service() + get_edge_service()
    ↓
get_workflow_persistence_service(graph_repository, vertex_service, edge_service)
    ↓
get_workflow_execution_service(persistence_service)
```

### 서비스별 독립성
- **GraphService**: GraphRepository만 의존
- **WorkflowPersistenceService**: GraphRepository + VertexService + EdgeService 의존
- **WorkflowExecutionService**: WorkflowPersistenceService만 의존

## 🎯 장점

### 1. 단일 책임 원칙 준수
- 각 서비스가 명확한 단일 책임을 가짐
- 코드의 가독성과 유지보수성 향상

### 2. 테스트 용이성
- 각 서비스를 독립적으로 테스트 가능
- Mock 객체 사용이 용이함

### 3. 확장성
- 새로운 기능 추가 시 해당 서비스만 수정
- 다른 서비스에 영향 없음

### 4. 재사용성
- 서비스들을 다른 컨텍스트에서 재사용 가능
- API와 내부 로직의 분리

## 🚀 사용 예시

### 워크플로우 생성
```python
# 1. Graph 메타데이터 생성
graph = Graph(name="My Workflow", description="Simple workflow")

# 2. Vertices와 Edges 정의
vertices = [Vertex(type="TEXT_INPUT", properties={...})]
edges = [Edge(source_id=1, target_id=2, type="default")]

# 3. 워크플로우 저장 (WorkflowPersistenceService 직접 사용)
saved_graph = await persistence_service.save_workflow(graph, vertices, edges)
```

### 워크플로우 실행
```python
# 1. 워크플로우 로드 (WorkflowPersistenceService 직접 사용)
graph, vertices, edges = await persistence_service.load_workflow(graph_id)

# 2. 워크플로우 실행 (WorkflowExecutionService 직접 사용)
result = await execution_service.execute_workflow(graph_id, {"input": "test"})
```

### Graph 메타데이터 관리
```python
# Graph 메타데이터만 조회 (GraphService 직접 사용)
graph = await graph_service.get_graph(graph_id)

# Graph 메타데이터만 삭제 (워크플로우는 유지)
await graph_service.delete_graph_metadata(graph_id)
```

## 📝 마이그레이션 가이드

기존 코드에서 새로운 구조로 마이그레이션할 때:

1. **서비스 직접 사용**:
   - 워크플로우 저장/로드: `WorkflowPersistenceService` 직접 사용
   - 워크플로우 실행: `WorkflowExecutionService` 직접 사용
   - Graph 메타데이터: `GraphService` 직접 사용

2. **라우터 엔드포인트 변경**:
   - 워크플로우 생성: `persistence_service.save_workflow()`
   - 워크플로우 조회: `persistence_service.load_workflow()`
   - 워크플로우 실행: `execution_service.execute_workflow()`
   - 워크플로우 삭제: `persistence_service.delete_workflow()`

3. **새로운 엔드포인트 활용**:
   - Graph 메타데이터만 필요한 경우: `/metadata` 엔드포인트 사용
   - 워크플로우 전체가 필요한 경우: 기존 엔드포인트 사용

4. **의존성 주입 업데이트**:
   - 각 서비스가 독립적으로 주입됨
   - 더 명확한 책임 분리
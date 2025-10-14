# Workflow Agent Platform

Langflow와 같은 워크플로우 기반 에이전트 생성 플랫폼입니다. 그래프 구조를 사용하여 복잡한 AI 워크플로우를 시각적으로 구성하고 실행할 수 있습니다.

## 주요 기능

### 🎯 핵심 기능
- **그래프 기반 워크플로우**: Vertex와 Edge를 사용한 시각적 워크플로우 구성
- **다양한 노드 타입**: LLM, 함수, 조건문, 웹훅 등 다양한 노드 지원
- **워크플로우 실행 엔진**: 위상 정렬을 통한 의존성 기반 실행
- **데이터베이스 저장**: PostgreSQL을 사용한 워크플로우 영구 저장
- **REST API**: FastAPI 기반의 완전한 REST API 제공

### 🔧 지원하는 노드 타입

#### 입력/출력 노드
- `TEXT_INPUT`: 텍스트 입력
- `TEXT_OUTPUT`: 텍스트 출력
- `JSON_INPUT`: JSON 입력
- `JSON_OUTPUT`: JSON 출력
- `FILE_INPUT`: 파일 입력
- `FILE_OUTPUT`: 파일 출력

#### 처리 노드
- `LLM_NODE`: LLM 호출 (OpenAI, Anthropic, 로컬 LLM)
- `API_CALL`: 외부 API 호출
- `FUNCTION`: Python 함수 실행
- `CONDITION`: 조건문 처리
- `LOOP`: 반복 처리

#### 유틸리티 노드
- `WEBHOOK`: 웹훅 호출
- `DELAY`: 지연 처리
- `MERGE`: 데이터 병합
- `SPLIT`: 데이터 분할

## 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 데이터베이스 설정
PostgreSQL 데이터베이스를 설정하고 환경변수를 구성합니다:
```bash
export DATABASE_URL="postgresql://username:password@localhost:5432/workflow_db"
```

### 3. 애플리케이션 실행
```bash
python main.py
```

서버가 `http://localhost:8000`에서 실행됩니다.

## API 사용법

### 워크플로우 생성
```bash
curl -X POST "http://localhost:8000/workflows/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Workflow",
    "description": "간단한 워크플로우",
    "vertices": [
      {
        "type": "TEXT_INPUT",
        "properties": {"text": "Hello World"}
      },
      {
        "type": "LLM_NODE",
        "properties": {"model": "gpt-3.5-turbo"}
      }
    ],
    "edges": [
      {
        "source_id": 1,
        "target_id": 2,
        "type": "default"
      }
    ]
  }'
```

### 워크플로우 실행
```bash
curl -X POST "http://localhost:8000/workflows/1/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "initial_inputs": {"custom_input": "value"}
  }'
```

### 워크플로우 조회
```bash
curl "http://localhost:8000/workflows/1"
```

## 워크플로우 예제

### 1. 간단한 LLM 워크플로우
```
텍스트 입력 → LLM 처리 → 텍스트 출력
```

### 2. 조건부 워크플로우
```
텍스트 입력 → 조건 확인 → [긴 텍스트 처리 | 짧은 텍스트 처리] → 병합 → 출력
```

### 3. 웹훅 워크플로우
```
텍스트 입력 → 웹훅 호출 → 지연 → JSON 출력
```

### 4. 복잡한 워크플로우
```
텍스트 입력 → 분할 → [개수 계산 | 대문자 변환] → 병합 → LLM 처리 → 출력
```

## 예제 워크플로우 생성

예제 워크플로우들을 생성하려면:

```bash
python examples/create_sample_workflows.py
```

## 아키텍처

### 데이터베이스 모델
- `Graph`: 워크플로우 메타데이터
- `Vertex`: 워크플로우 노드
- `Edge`: 노드 간 연결

### 서비스 레이어
- `GraphService`: 워크플로우 CRUD 및 실행
- `VertexService`: 노드 관리
- `EdgeService`: 연결 관리

### 워크플로우 엔진
- `WorkflowEngine`: 워크플로우 실행 엔진
- `NodeFactory`: 노드 인스턴스 생성

## 확장성

### 새로운 노드 타입 추가
1. `BaseNode`를 상속받는 새 노드 클래스 생성
2. `NodeType` enum에 새 타입 추가
3. `NodeFactory`에 새 노드 등록

### 예제:
```python
class CustomNode(BaseNode):
    def __init__(self, node_id: str, properties: Dict[str, Any]):
        super().__init__(node_id, properties)
        self.inputs = [NodeInputOutput(name="input", type=NodeInputOutputType.TEXT)]
        self.outputs = [NodeInputOutput(name="output", type=NodeInputOutputType.TEXT)]
    
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        # 커스텀 로직 구현
        return {"output": "processed"}
    
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        return "input" in inputs

# 팩토리에 등록
NodeFactory.register_node_type(NodeType.CUSTOM, CustomNode)
```

## API 문서

서버 실행 후 `http://localhost:8000/docs`에서 Swagger UI를 통해 API 문서를 확인할 수 있습니다.

## 라이선스

MIT License

## 기여하기

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

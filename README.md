# Workflow Agent Platform

Langflow와 같은 워크플로우 기반 에이전트 생성 플랫폼입니다. 그래프 구조를 사용하여 복잡한 AI 워크플로우를 시각적으로 구성하고 실행할 수 있습니다.

## 빠른 시작 (Quick Start)

```bash
# 1. 프로젝트 클론
git clone <repository-url>
cd backend

# 2. Docker Compose로 실행 (가장 쉬운 방법)
docker-compose up -d

# 3. API 문서 확인
open http://localhost:8000/docs
```

완료! 이제 워크플로우를 생성하고 실행할 수 있습니다.

## 목차

- [빠른 시작](#빠른-시작-quick-start)
- [주요 기능](#주요-기능)
- [기술 스택](#기술-스택)
- [설치 및 실행](#설치-및-실행)
- [API 사용법](#api-사용법)
- [워크플로우 예제](#워크플로우-예제)
- [프로젝트 구조](#프로젝트-구조)
- [아키텍처](#아키텍처)
- [확장성](#확장성)
- [개발 워크플로우](#개발-워크플로우)
- [API 엔드포인트](#api-엔드포인트)
- [환경 변수](#환경-변수)
- [문제 해결](#문제-해결)
- [기여하기](#기여하기)

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

## 기술 스택

### 백엔드
- **Python 3.11+**: 최신 Python 기능 활용
- **FastAPI**: 고성능 비동기 웹 프레임워크
- **SQLModel**: SQLAlchemy 기반 ORM (Pydantic 통합)
- **PostgreSQL**: 관계형 데이터베이스
- **Alembic**: 데이터베이스 마이그레이션 도구

### 패키지 관리
- **uv**: 차세대 Python 패키지 관리자 (Rust 기반, 매우 빠름)
- **pyproject.toml**: 표준 Python 프로젝트 설정

### 개발 도구
- **Ruff**: 초고속 Python 린터 (Rust 기반)
- **Black**: 코드 포맷터
- **isort**: Import 정렬
- **MyPy**: 정적 타입 체커
- **pre-commit**: Git 훅 관리

### 인프라
- **Docker**: 컨테이너화
- **Docker Compose**: 다중 컨테이너 관리
- **Uvicorn**: ASGI 서버

### API & 통합
- **OpenAI API**: LLM 노드 통합
- **Anthropic API**: Claude 모델 지원 (예정)
- **Requests**: HTTP 클라이언트

## 설치 및 실행

### 필수 요구사항
- Python 3.11 이상
- Docker & Docker Compose (권장)
- PostgreSQL 15 (로컬 실행 시)

### 방법 1: Docker Compose 사용 (권장)

가장 간단한 실행 방법입니다:

```bash
# 서비스 시작 (PostgreSQL + FastAPI)
docker-compose up -d

# 로그 확인
docker-compose logs -f app

# 서비스 중지
docker-compose down

# 데이터베이스 포함 완전 삭제
docker-compose down -v
```

서버가 `http://localhost:8000`에서 실행됩니다.

### 방법 2: 로컬 개발 환경

#### 1. UV 설치
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# pip를 통한 설치
pip install uv
```

#### 2. 의존성 설치
```bash
# 프로젝트 의존성 설치
uv sync

# 개발 의존성 포함 설치
uv sync --all-groups
```

#### 3. 환경 변수 설정
`.env` 파일을 프로젝트 루트에 생성합니다:

```bash
# 데이터베이스 설정
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/workflow_scratch_2

# 서버 설정
HOST=0.0.0.0
PORT=8000
DEBUG=true

# OpenAI API (LLM 노드 사용 시 필요)
OPENAI_API_KEY=your_api_key_here
```

#### 4. 데이터베이스 설정

PostgreSQL을 로컬에 설치하거나 Docker로 실행:

```bash
# Docker로 PostgreSQL만 실행
docker-compose up -d postgres

# 또는 로컬 PostgreSQL에 데이터베이스 생성
createdb workflow_scratch_2
```

#### 5. 데이터베이스 마이그레이션

Alembic을 사용하여 데이터베이스 스키마를 생성합니다:

```bash
# 최신 마이그레이션 적용
uv run alembic upgrade head

# 마이그레이션 상태 확인
uv run alembic current

# 자세한 Alembic 사용법은 ALEMBIC_GUIDE.md 참조
```

#### 6. 애플리케이션 실행
```bash
# UV를 통해 실행
uv run python main.py

# 또는 직접 실행
python main.py
```

서버가 `http://localhost:8000`에서 실행됩니다.

### Pre-commit 설정 (선택사항)
코드 품질을 유지하기 위한 pre-commit 훅:

```bash
# pre-commit 설치 (이미 의존성에 포함됨)
uv sync

# pre-commit 훅 설치
uv run pre-commit install

# 모든 파일에 대해 실행
uv run pre-commit run --all-files
```

설정된 pre-commit 훅들:
- **Black**: Python 코드 포맷팅
- **isort**: import 문 정렬
- **Ruff**: 린팅 및 코드 품질 검사
- **MyPy**: 타입 체킹

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

## 프로젝트 구조

```
backend/
├── alembic/                    # 데이터베이스 마이그레이션
│   └── versions/              # 마이그레이션 버전 파일들
├── database/                   # 데이터베이스 모델
│   ├── graph/                 # Graph, Vertex, Edge 모델
│   ├── setup.py              # 데이터베이스 초기화
│   └── init.sql/             # 초기 SQL 스크립트
├── dto/                        # 데이터 전송 객체
│   └── workflow/             # 워크플로우 관련 DTO
├── helpers/                    # 헬퍼 및 유틸리티
│   ├── engine/               # 워크플로우 실행 엔진
│   ├── node/                 # 노드 구현체
│   │   ├── node_base.py     # 기본 노드 클래스
│   │   ├── factory.py       # 노드 팩토리
│   │   └── node_templates/  # 노드 타입 구현들
│   └── utils/                # 유틸리티 함수들
├── repositories/               # 데이터베이스 레포지토리
│   └── graph/                # Graph CRUD 작업
├── routers/                    # FastAPI 라우터
│   └── v1/graph/             # v1 API 엔드포인트
├── services/                   # 비즈니스 로직
│   ├── graph/                # 그래프 서비스
│   └── workflow/             # 워크플로우 서비스
├── setting/                    # 설정 파일
│   ├── config.py             # 환경 설정
│   └── logger.py             # 로깅 설정
├── tests/                      # 테스트 파일
├── docker-compose.yml          # Docker Compose 설정
├── Dockerfile                  # Docker 이미지 빌드
├── pyproject.toml              # 프로젝트 메타데이터 및 의존성
├── alembic.ini                 # Alembic 설정
└── main.py                     # 애플리케이션 엔트리포인트
```

## 아키텍처

### 레이어 구조

```
┌─────────────────────────────────────┐
│         FastAPI Routers            │  HTTP 요청 처리
├─────────────────────────────────────┤
│           Services                 │  비즈니스 로직
├─────────────────────────────────────┤
│         Repositories               │  데이터 접근 계층
├─────────────────────────────────────┤
│      Database Models (SQLModel)    │  ORM 모델
└─────────────────────────────────────┘
```

### 핵심 컴포넌트

#### 1. 데이터베이스 모델 (`database/`)
- **Graph**: 워크플로우 메타데이터 (이름, 설명, 생성일)
- **Vertex**: 워크플로우 노드 (타입, 속성)
- **Edge**: 노드 간 연결 (소스, 타겟, 타입)

#### 2. 서비스 레이어 (`services/`)
- **GraphService**: 워크플로우 CRUD 작업
- **WorkflowExecutionService**: 워크플로우 실행 관리
- **WorkflowPersistenceService**: 워크플로우 영구 저장

#### 3. 워크플로우 엔진 (`helpers/engine/`)
- **WorkflowEngine**: 
  - 위상 정렬을 통한 실행 순서 결정
  - 의존성 기반 노드 실행
  - 에러 핸들링 및 상태 관리

#### 4. 노드 시스템 (`helpers/node/`)
- **BaseNode**: 모든 노드의 추상 기본 클래스
- **NodeFactory**: 노드 타입에 따른 인스턴스 생성
- **Node Templates**: 각 노드 타입의 구체적 구현
  - 입출력 노드 (TEXT_INPUT, JSON_OUTPUT 등)
  - 처리 노드 (LLM_NODE, API_CALL, FUNCTION 등)
  - 유틸리티 노드 (WEBHOOK, MERGE, SPLIT 등)

#### 5. API 라우터 (`routers/`)
- REST API 엔드포인트 정의
- 요청/응답 검증
- Swagger 문서 자동 생성

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

## 개발 워크플로우

### 데이터베이스 마이그레이션

모델을 변경한 후 마이그레이션을 생성하고 적용합니다:

```bash
# 1. 모델 변경사항 기반으로 마이그레이션 생성
uv run alembic revision --autogenerate -m "Add new column to graph"

# 2. 마이그레이션 적용
uv run alembic upgrade head

# 3. 마이그레이션 히스토리 확인
uv run alembic history

# 4. 필요시 롤백
uv run alembic downgrade -1
```

자세한 내용은 `ALEMBIC_GUIDE.md`를 참조하세요.

### 테스트 실행

```bash
# 모든 테스트 실행
uv run python -m pytest

# 특정 테스트 파일 실행
uv run python -m pytest tests/test_workflow.py

# 커버리지와 함께 실행
uv run python -m pytest --cov=.
```

### 코드 품질 검사

```bash
# Ruff 린팅
uv run ruff check .

# Ruff 자동 수정
uv run ruff check --fix .

# Black 포맷팅
uv run black .

# isort import 정렬
uv run isort .

# MyPy 타입 체킹
uv run mypy .
```

## API 엔드포인트

### 주요 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/` | 루트 엔드포인트 (헬스 체크) |
| GET | `/docs` | Swagger UI API 문서 |
| GET | `/redoc` | ReDoc API 문서 |
| POST | `/workflows/` | 워크플로우 생성 |
| GET | `/workflows/{id}` | 워크플로우 조회 |
| PUT | `/workflows/{id}` | 워크플로우 수정 |
| DELETE | `/workflows/{id}` | 워크플로우 삭제 |
| POST | `/workflows/{id}/execute` | 워크플로우 실행 |
| GET | `/workflows/` | 워크플로우 목록 조회 |
| POST | `/workflows/import` | 워크플로우 가져오기 |
| GET | `/workflows/{id}/export` | 워크플로우 내보내기 |

### API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## 환경 변수

프로젝트에서 사용하는 환경 변수 목록:

| 변수명 | 설명 | 기본값 | 필수 |
|--------|------|--------|------|
| `DATABASE_URL` | PostgreSQL 연결 URL | - | ✅ |
| `HOST` | 서버 호스트 | `0.0.0.0` | ❌ |
| `PORT` | 서버 포트 | `8000` | ❌ |
| `DEBUG` | 디버그 모드 | `false` | ❌ |
| `OPENAI_API_KEY` | OpenAI API 키 (LLM 노드 사용 시) | - | ⚠️ |
| `LOG_LEVEL` | 로그 레벨 | `INFO` | ❌ |

⚠️ = LLM_NODE를 사용하는 워크플로우 실행 시 필수

## 문제 해결

### 데이터베이스 연결 오류

```bash
# 데이터베이스가 실행 중인지 확인
docker-compose ps

# PostgreSQL 로그 확인
docker-compose logs postgres

# 데이터베이스 재시작
docker-compose restart postgres
```

### 마이그레이션 오류

```bash
# 마이그레이션 상태 확인
uv run alembic current

# 강제로 특정 버전으로 설정 (주의!)
uv run alembic stamp head
```

### 포트 충돌

```bash
# 8000 포트를 사용 중인 프로세스 확인
lsof -i :8000

# 또는 다른 포트로 실행
PORT=8080 python main.py
```

## 성능 및 확장

### 데이터베이스 최적화
- 인덱스가 적절히 설정되어 있습니다 (Graph, Vertex, Edge)
- 복잡한 워크플로우의 경우 연결 풀 크기 조정 고려

### 워크플로우 실행 최적화
- 병렬 실행 가능한 노드는 자동으로 동시 실행됨
- 큰 데이터 처리 시 MERGE/SPLIT 노드 활용
- LLM 노드는 비동기 처리로 최적화됨


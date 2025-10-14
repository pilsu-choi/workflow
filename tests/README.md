# create_simple_workflow() 테스트 가이드

이 디렉토리는 `create_simple_workflow()` 함수에 대한 포괄적인 테스트 코드를 포함합니다.

## 📁 파일 구조

```
tests/
├── __init__.py
├── test_workflow_router.py    # 메인 테스트 파일
└── README.md                  # 이 파일
```

## 🧪 테스트 내용

### TestCreateSimpleWorkflow 클래스
- **성공 케이스**: 정상적인 워크플로우 생성
- **실패 케이스**: 필수 필드 누락, 서비스 에러 등
- **경계 케이스**: 빈 문자열, 추가 필드 등

### TestCreateSimpleWorkflowIntegration 클래스
- **비동기 통합 테스트**: AsyncClient를 사용한 실제 API 호출 테스트

### TestSimpleWorkflowRequestValidation 클래스
- **DTO 검증 테스트**: SimpleWorkflowRequest 모델의 유효성 검사

## 🚀 테스트 실행 방법

### 1. 전체 테스트 실행
```bash
# 프로젝트 루트에서
python run_tests.py

# 또는 직접 pytest 사용
pytest tests/test_workflow_router.py -v
```

### 2. 특정 테스트만 실행
```bash
# 성공 케이스만 테스트
python run_tests.py --specific

# 특정 테스트 클래스만 실행
pytest tests/test_workflow_router.py::TestCreateSimpleWorkflow -v

# 특정 테스트 메서드만 실행
pytest tests/test_workflow_router.py::TestCreateSimpleWorkflow::test_create_simple_workflow_success -v
```

### 3. 테스트 커버리지 확인
```bash
pytest tests/test_workflow_router.py --cov=routers.v1.graph.workflow_router --cov-report=html
```

## 📋 테스트 케이스 목록

### ✅ 성공 케이스
1. **test_create_simple_workflow_success**: 정상적인 워크플로우 생성
2. **test_create_simple_workflow_without_description**: description 없이 생성
3. **test_create_simple_workflow_extra_fields**: 추가 필드가 포함된 요청

### ❌ 실패 케이스
1. **test_create_simple_workflow_missing_name**: name 필드 누락
2. **test_create_simple_workflow_empty_name**: 빈 name 필드
3. **test_create_simple_workflow_service_error**: GraphService 에러
4. **test_create_simple_workflow_invalid_json**: 잘못된 JSON 형식

### 🔍 통합 테스트
1. **test_create_simple_workflow_async_client**: AsyncClient를 사용한 비동기 테스트

### 📝 DTO 검증 테스트
1. **test_simple_workflow_request_valid**: 유효한 요청 객체 생성
2. **test_simple_workflow_request_default_description**: 기본 description 값
3. **test_simple_workflow_request_invalid_name**: 잘못된 name 타입
4. **test_simple_workflow_request_empty_name**: 빈 문자열 name

## 🛠️ 테스트 설정

### Mock 사용
- `GraphService`의 `create_simple_workflow` 메서드를 Mock으로 처리
- 실제 데이터베이스 연결 없이 테스트 가능
- 다양한 응답 시나리오 테스트 가능

### 의존성 주입
- `get_graph_service` 의존성을 Mock으로 대체
- 각 테스트에서 독립적인 Mock 인스턴스 사용

## 📊 예상 결과

### 성공 응답 예시
```json
{
  "success": true,
  "graph_id": 1,
  "message": "간단한 워크플로우가 성공적으로 생성되었습니다",
  "workflow": {
    "name": "Test Simple Workflow",
    "description": "This is a test simple workflow",
    "vertices": [...],
    "edges": [...]
  }
}
```

### 실패 응답 예시
```json
{
  "detail": "Database connection failed"
}
```

## 🔧 문제 해결

### 일반적인 문제들

1. **ImportError**: 필요한 패키지가 설치되지 않은 경우
   ```bash
   pip install pytest httpx requests
   ```

2. **Mock 관련 오류**: Mock 설정이 잘못된 경우
   - `patch` 경로 확인
   - Mock 객체의 `spec` 설정 확인

3. **테스트 실패**: 실제 서비스와 Mock 응답이 다른 경우
   - Mock 응답 데이터를 실제 서비스 응답과 일치시키기

## 📚 추가 리소스

- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)


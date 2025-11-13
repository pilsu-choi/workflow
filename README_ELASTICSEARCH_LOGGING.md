# 워크플로우 로그 시스템 (Elasticsearch)

모든 워크플로우 실행 로그가 **Elasticsearch**에 저장되고 관리됩니다.

## 🚀 빠른 시작

### 1. Elasticsearch 설치

```bash
# docker-compose.yml에 이미 포함되어 있습니다
docker-compose up -d elasticsearch kibana
```

### 2. Python 패키지 설치

```bash
uv add elasticsearch
```

### 3. 인덱스 초기화

```bash
uv run python scripts/init_elasticsearch.py
```

### 4. 애플리케이션 실행

```bash
uv run uvicorn main:app --reload
```

### 5. 테스트

```bash
# 워크플로우 실행
curl -X POST http://localhost:8000/v1/workflows/1/execute \
  -H "Content-Type: application/json" \
  -d '{"initial_inputs": {"text": "Hello"}}'

# 로그 조회
curl http://localhost:8000/v1/workflows/logs
```

## 📊 API 엔드포인트

### 로그 조회

```bash
# 전체 로그 목록
GET /v1/workflows/logs?limit=100&offset=0

# 특정 워크플로우의 로그
GET /v1/workflows/{graph_id}/logs?limit=100&offset=0

# 특정 실행 로그 상세
GET /v1/workflows/logs/{execution_id}?include_messages=true
```

### 로그 검색 (전문 검색)

```bash
# "timeout" 검색
GET /v1/workflows/{graph_id}/logs/search?query=timeout

# 에러 로그만
GET /v1/workflows/{graph_id}/logs/search?level=ERROR

# 복합 검색
GET /v1/workflows/{graph_id}/logs/search?query=노드&level=ERROR&limit=50
```

### 로그 삭제

```bash
DELETE /v1/workflows/logs/{execution_id}
```

## 📖 데이터 구조

### 메타데이터 문서

```json
{
  "doc_type": "execution_metadata",
  "execution_id": "uuid",
  "graph_id": 1,
  "start_time": "2025-11-06T12:00:00Z",
  "end_time": "2025-11-06T12:00:02Z",
  "execution_time": 2.5,
  "status": "success",
  "success": true,
  "execution_order": ["1", "2"],
  "node_results": {...},
  "errors": [],
  "log_count": 15
}
```

### 로그 메시지 문서

```json
{
  "doc_type": "log_message",
  "execution_id": "uuid",
  "graph_id": 1,
  "timestamp": "2025-11-06T12:00:01Z",
  "level": "INFO",
  "message": "노드 1 실행 시작",
  "node_id": "1",
  "sequence": 5
}
```

## 🔍 Kibana 사용

### 접속

```
http://localhost:5601
```

### Index Pattern 생성

1. Management → Index Patterns
2. Create index pattern: `workflow-logs*`
3. Time field: `timestamp`

### 로그 검색

- Discover 메뉴 사용
- 쿼리 예시:
  - `level: ERROR`
  - `node_id: 1`
  - `message: timeout`

## 🛠️ 환경 변수

```bash
# .env
ELASTICSEARCH_ENABLED=true
ELASTICSEARCH_URL=http://localhost:9200
```

## 📚 자세한 문서

- **`ELASTICSEARCH_SETUP.md`** - 상세 설정 가이드
- **`ELASTICSEARCH_MIGRATION_SUMMARY.md`** - 마이그레이션 요약

## ✨ 주요 기능

- ✅ 자동 로그 저장
- ✅ 전문 검색 (Full-text Search)
- ✅ 로그 레벨 자동 감지
- ✅ 노드 정보 자동 추출
- ✅ Kibana 시각화
- ✅ Graceful Degradation

## 🎯 장점

| 기능 | PostgreSQL | Elasticsearch |
|------|-----------|---------------|
| 전문 검색 | ❌ | ✅ |
| 확장성 | ⚠️ | ✅ |
| 검색 속도 | ⚠️ | ✅ |
| 시각화 | ❌ | ✅ Kibana |

Happy logging! 🚀


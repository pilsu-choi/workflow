# Elasticsearch 로그 시스템 설정 가이드

모든 워크플로우 실행 로그가 Elasticsearch에 저장되고 관리됩니다.

## 📋 목차

1. [Elasticsearch 설치](#elasticsearch-설치)
2. [인덱스 초기화](#인덱스-초기화)
3. [환경 변수 설정](#환경-변수-설정)
4. [API 사용법](#api-사용법)
5. [데이터 구조](#데이터-구조)

## Elasticsearch 설치

### Docker Compose로 설치 (추천)

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    # ... 기존 PostgreSQL 설정 ...

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: workflow-elasticsearch
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      - xpack.security.enabled=false  # 개발환경용
    ports:
      - "9200:9200"
      - "9300:9300"
    volumes:
      - es_data:/usr/share/elasticsearch/data
    networks:
      - workflow-network

  # 선택적: Kibana (데이터 시각화)
  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    container_name: workflow-kibana
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    depends_on:
      - elasticsearch
    networks:
      - workflow-network

volumes:
  es_data:
    driver: local

networks:
  workflow-network:
    driver: bridge
```

### Docker Compose 실행

```bash
# Elasticsearch 시작
docker-compose up -d elasticsearch

# Elasticsearch 상태 확인
curl http://localhost:9200

# 응답 예시:
# {
#   "name" : "...",
#   "cluster_name" : "docker-cluster",
#   "version" : { "number" : "8.11.0", ... }
# }
```

### Python 패키지 설치

```bash
# Elasticsearch 클라이언트 설치
pip install elasticsearch

# 또는 uv 사용
uv add elasticsearch
```

## 인덱스 초기화

### 자동 초기화 (애플리케이션 시작 시)

```python
# scripts/init_elasticsearch.py
import asyncio
from services.elasticsearch.es_client import ElasticsearchClient

async def init_elasticsearch():
    """Elasticsearch 인덱스 초기화"""
    es_client = ElasticsearchClient(enabled=True)
    await es_client.create_index()
    print("✅ Elasticsearch 인덱스 초기화 완료")
    await es_client.close()

if __name__ == "__main__":
    asyncio.run(init_elasticsearch())
```

```bash
# 실행
cd /home/pschoi/tests/workflow_scratch_2/backend
uv run python scripts/init_elasticsearch.py
```

### 수동 인덱스 생성

```bash
# workflow-logs 인덱스 생성
curl -X PUT "localhost:9200/workflow-logs" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "doc_type": { "type": "keyword" },
      "execution_id": { "type": "keyword" },
      "graph_id": { "type": "integer" },
      "timestamp": { "type": "date" },
      "level": { "type": "keyword" },
      "message": { "type": "text" },
      "node_id": { "type": "keyword" },
      "node_type": { "type": "keyword" },
      "error": { "type": "text" },
      "stack_trace": { "type": "text" },
      "status": { "type": "keyword" },
      "success": { "type": "boolean" },
      "execution_time": { "type": "float" },
      "execution_order": { "type": "keyword" },
      "node_results": { "type": "object", "enabled": false },
      "errors": { "type": "text" },
      "sequence": { "type": "integer" },
      "created_at": { "type": "date" }
    }
  }
}'

# 인덱스 확인
curl "localhost:9200/workflow-logs/_mapping?pretty"
```

## 환경 변수 설정

```bash
# .env 파일
ELASTICSEARCH_ENABLED=true
ELASTICSEARCH_URL=http://localhost:9200
# ELASTICSEARCH_USER=elastic  # 인증 사용 시
# ELASTICSEARCH_PASSWORD=changeme
```

### Elasticsearch 비활성화

Elasticsearch 없이도 애플리케이션이 동작하도록 설계되었습니다:

```bash
# .env
ELASTICSEARCH_ENABLED=false
```

이 경우 로그 저장/조회는 동작하지 않지만 애플리케이션은 정상 작동합니다.

## API 사용법

### 1. 워크플로우 실행 (로그 자동 저장)

```bash
# 워크플로우 실행
curl -X POST http://localhost:8000/v1/workflows/1/execute \
  -H "Content-Type: application/json" \
  -d '{
    "initial_inputs": {
      "text": "Hello World"
    }
  }'

# 응답
{
  "success": true,
  "execution_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "execution_time": 2.5,
  "node_results": {...},
  "errors": [],
  "execution_order": ["1", "2"]
}
```

### 2. 로그 조회

#### 전체 로그 목록

```bash
curl "http://localhost:8000/v1/workflows/logs?limit=10"
```

#### 특정 워크플로우의 로그

```bash
curl "http://localhost:8000/v1/workflows/1/logs?limit=10"
```

#### 특정 실행 로그 상세 조회

```bash
# 메타데이터 + 상세 로그 메시지
curl "http://localhost:8000/v1/workflows/logs/a1b2c3d4-e5f6-7890-abcd-ef1234567890"

# 메타데이터만
curl "http://localhost:8000/v1/workflows/logs/a1b2c3d4-e5f6-7890-abcd-ef1234567890?include_messages=false"
```

### 3. 로그 검색 (전문 검색)

```bash
# "timeout"이 포함된 로그 검색
curl "http://localhost:8000/v1/workflows/1/logs/search?query=timeout"

# 에러 로그만 검색
curl "http://localhost:8000/v1/workflows/1/logs/search?level=ERROR"

# 복합 검색
curl "http://localhost:8000/v1/workflows/1/logs/search?query=노드%20실행&level=ERROR"
```

### 4. 로그 삭제

```bash
curl -X DELETE "http://localhost:8000/v1/workflows/logs/a1b2c3d4-e5f6-7890-abcd-ef1234567890"
```

## 데이터 구조

### Elasticsearch 문서 타입

#### 1. execution_metadata (실행 메타데이터)

```json
{
  "doc_type": "execution_metadata",
  "execution_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "graph_id": 1,
  "start_time": "2025-11-06T12:00:00.000Z",
  "end_time": "2025-11-06T12:00:02.500Z",
  "execution_time": 2.5,
  "status": "success",
  "success": true,
  "execution_order": ["1", "2", "3"],
  "node_results": {
    "1": {"output": "..."},
    "2": {"result": "..."}
  },
  "errors": [],
  "created_at": "2025-11-06T12:00:02.500Z",
  "log_count": 15
}
```

#### 2. log_message (개별 로그 메시지)

```json
{
  "doc_type": "log_message",
  "execution_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "graph_id": 1,
  "timestamp": "2025-11-06T12:00:01.234Z",
  "level": "INFO",
  "message": "노드 1 실행 시작",
  "node_id": "1",
  "sequence": 5
}
```

#### 3. log_message (에러)

```json
{
  "doc_type": "log_message",
  "execution_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "graph_id": 1,
  "timestamp": "2025-11-06T12:00:02.456Z",
  "level": "ERROR",
  "message": "노드 2 실행 실패: timeout exceeded",
  "error": "노드 2 실행 실패: timeout exceeded",
  "node_id": "2",
  "sequence": 12
}
```

## Kibana로 로그 확인

### Kibana 접속

```bash
# 브라우저에서 접속
http://localhost:5601
```

### Index Pattern 생성

1. Management → Stack Management → Index Patterns
2. "Create index pattern" 클릭
3. Index pattern name: `workflow-logs*`
4. Time field: `timestamp` 선택
5. Create

### 로그 검색

1. Analytics → Discover
2. 시간 범위 선택
3. 검색:
   - `level: ERROR` - 에러 로그만
   - `node_id: 1` - 특정 노드
   - `message: timeout` - 메시지 검색

### 대시보드 생성

1. Analytics → Dashboard
2. Create dashboard
3. 추가 가능한 시각화:
   - 시간대별 로그 수 (Line chart)
   - 레벨별 분포 (Pie chart)
   - 워크플로우별 실행 통계 (Data table)
   - 에러 발생 추이 (Area chart)

## 고급 기능

### 1. 직접 Elasticsearch 쿼리

```python
import requests

# Elasticsearch에 직접 쿼리
response = requests.post(
    "http://localhost:9200/workflow-logs/_search",
    json={
        "query": {
            "bool": {
                "must": [
                    {"term": {"graph_id": 1}},
                    {"match": {"message": "timeout"}}
                ]
            }
        },
        "sort": [{"timestamp": "desc"}],
        "size": 10
    }
)

results = response.json()
for hit in results["hits"]["hits"]:
    print(hit["_source"])
```

### 2. 집계 쿼리 (통계)

```bash
# 워크플로우별 실행 통계
curl -X POST "localhost:9200/workflow-logs/_search" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "query": {
    "term": {"doc_type": "execution_metadata"}
  },
  "aggs": {
    "by_graph": {
      "terms": {"field": "graph_id"},
      "aggs": {
        "avg_time": {"avg": {"field": "execution_time"}},
        "success_rate": {
          "value_count": {"field": "success"}
        }
      }
    }
  }
}
'
```

### 3. 인덱스 정리 (오래된 로그 삭제)

```bash
# 30일 이상 오래된 로그 삭제
curl -X POST "localhost:9200/workflow-logs/_delete_by_query" -H 'Content-Type: application/json' -d'
{
  "query": {
    "range": {
      "created_at": {
        "lt": "now-30d"
      }
    }
  }
}
'
```

## 문제 해결

### Elasticsearch 연결 실패

```bash
# Elasticsearch 상태 확인
curl http://localhost:9200/_cluster/health

# 컨테이너 로그 확인
docker logs workflow-elasticsearch
```

### 인덱스 초기화 실패

```bash
# 기존 인덱스 삭제 후 재생성
curl -X DELETE "localhost:9200/workflow-logs"
uv run python scripts/init_elasticsearch.py
```

### 메모리 부족

```yaml
# docker-compose.yml에서 메모리 증가
environment:
  - "ES_JAVA_OPTS=-Xms1g -Xmx1g"  # 1GB로 증가
```

## 성능 최적화

### 1. 벌크 인덱싱

현재 구현은 이미 벌크 인덱싱을 사용합니다 (`bulk_index_logs`).

### 2. 인덱스 설정 최적화

```bash
curl -X PUT "localhost:9200/workflow-logs/_settings" -H 'Content-Type: application/json' -d'
{
  "index": {
    "refresh_interval": "30s",
    "number_of_replicas": 0
  }
}
'
```

### 3. 인덱스 라이프사이클 관리

```bash
# 30일 후 자동 삭제 정책
curl -X PUT "localhost:9200/_ilm/policy/workflow-logs-policy" -H 'Content-Type: application/json' -d'
{
  "policy": {
    "phases": {
      "delete": {
        "min_age": "30d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
'
```

## 결론

✅ **완전한 Elasticsearch 기반 로그 시스템**
- PostgreSQL 테이블 불필요
- 강력한 전문 검색
- 확장성 우수
- Kibana로 시각화

**시작하기:**
```bash
# 1. Elasticsearch 시작
docker-compose up -d elasticsearch

# 2. 인덱스 초기화
uv run python scripts/init_elasticsearch.py

# 3. 애플리케이션 실행
uv run uvicorn main:app --reload
```

이제 모든 로그는 Elasticsearch에 저장되고 관리됩니다! 🚀


"""
Elasticsearch 클라이언트
워크플로우 로그를 Elasticsearch에 저장하고 검색하는 기능 제공
"""

# mypy: ignore-errors
# FIXME: mypy 오류 정정하기
from datetime import datetime
from typing import Any, Dict, List

from elasticsearch import AsyncElasticsearch

from setting.logger import get_logger

logger = get_logger(__name__)


class ElasticsearchClient:
    """Elasticsearch 클라이언트 (선택적 기능)"""

    def __init__(self, enabled: bool = False):
        """
        Args:
            enabled: Elasticsearch 사용 여부
                    False면 모든 메서드가 동작하지 않음 (graceful degradation)
        """
        self.enabled = enabled
        self.client: AsyncElasticsearch | None = None
        self.index_name: str = "workflow-logs"

        if enabled:
            try:
                # elasticsearch 패키지가 설치되어 있는 경우에만 import

                self.client = AsyncElasticsearch(
                    ["http://localhost:9200"],
                    # 프로덕션에서는 환경 변수로 설정
                    # http_auth=(os.getenv("ES_USER"), os.getenv("ES_PASSWORD"))
                )
                logger.info("Elasticsearch 클라이언트 초기화 완료")
            except ImportError:
                logger.warning(
                    "elasticsearch 패키지가 설치되지 않았습니다. "
                    "pip install elasticsearch 를 실행하세요."
                )
                self.enabled = False
            except Exception as e:
                logger.error(f"Elasticsearch 연결 실패: {str(e)}", exc_info=True)
                self.enabled = False

    async def create_index(self):
        """인덱스 생성 (매핑 정의)"""
        if not self.enabled:
            return

        try:
            mapping = {
                "mappings": {
                    "properties": {
                        "execution_id": {"type": "keyword"},
                        "graph_id": {"type": "integer"},
                        "timestamp": {"type": "date"},
                        "level": {"type": "keyword"},
                        "message": {"type": "text"},
                        "node_id": {"type": "keyword"},
                        "node_type": {"type": "keyword"},
                        "error": {"type": "text"},
                        "stack_trace": {"type": "text"},
                        "duration_ms": {"type": "float"},
                    }
                }
            }

            if not await self.client.indices.exists(index=self.index_name):
                await self.client.indices.create(index=self.index_name, body=mapping)
                logger.info(f"Elasticsearch 인덱스 생성: {self.index_name}")
        except Exception as e:
            logger.error(f"인덱스 생성 실패: {str(e)}", exc_info=True)

    async def index_log(self, execution_id: str, log_entry: Dict[str, Any]):
        """단일 로그 인덱싱"""
        if not self.enabled:
            return

        try:
            await self.client.index(index=self.index_name, body=log_entry)
        except Exception as e:
            logger.error(f"로그 인덱싱 실패: {str(e)}", exc_info=True)

    async def bulk_index_logs(
        self, execution_id: str, log_entries: List[Dict[str, Any]]
    ):
        """배치 로그 인덱싱"""
        if not self.enabled or not log_entries:
            return

        try:
            from elasticsearch.helpers import async_bulk

            actions = [
                {"_index": self.index_name, "_source": {**entry}}
                for entry in log_entries
            ]

            success, failed = await async_bulk(self.client, actions)
            logger.info(
                f"ES 배치 인덱싱: {success}개 성공, {failed}개 실패 "
                f"(execution_id={execution_id})"
            )
        except Exception as e:
            logger.error(f"배치 인덱싱 실패: {str(e)}", exc_info=True)

    async def search_logs(
        self,
        execution_id: str | None = None,
        query: str | None = None,
        level: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        size: int = 100,
    ) -> List[Dict[str, Any]]:
        """로그 검색"""
        if not self.enabled:
            logger.warning("Elasticsearch가 비활성화되어 있습니다")
            return []

        try:
            must_conditions = []

            if execution_id:
                must_conditions.append({"term": {"execution_id": execution_id}})

            if query:
                must_conditions.append(
                    {
                        "multi_match": {
                            "query": query,
                            "fields": ["message", "error", "stack_trace"],
                        }
                    }
                )

            if level:
                must_conditions.append({"term": {"level": level}})

            if start_time or end_time:
                time_range = {}
                if start_time:
                    time_range["gte"] = start_time.isoformat()
                if end_time:
                    time_range["lte"] = end_time.isoformat()
                must_conditions.append({"range": {"timestamp": time_range}})

            search_body = {
                "query": (
                    {"bool": {"must": must_conditions}}
                    if must_conditions
                    else {"match_all": {}}
                ),
                "sort": [{"timestamp": {"order": "asc"}}],
                "size": size,
            }

            result = await self.client.search(index=self.index_name, body=search_body)

            return [hit["_source"] for hit in result["hits"]["hits"]]
        except Exception as e:
            logger.error(f"로그 검색 실패: {str(e)}", exc_info=True)
            return []

    async def delete_logs_by_execution_id(self, execution_id: str):
        """특정 실행의 모든 로그 삭제"""
        if not self.enabled:
            return

        try:
            await self.client.delete_by_query(
                index=self.index_name,
                body={"query": {"term": {"execution_id": execution_id}}},
            )
            logger.info(f"ES 로그 삭제: execution_id={execution_id}")
        except Exception as e:
            logger.error(f"로그 삭제 실패: {str(e)}", exc_info=True)

    async def get_log_stats(self, graph_id: int | None = None) -> Dict[str, Any]:
        """로그 통계 조회"""
        if not self.enabled:
            return {}

        try:
            query = {"match_all": {}}
            if graph_id:
                query = {"term": {"graph_id": graph_id}}

            aggs = {
                "level_distribution": {"terms": {"field": "level"}},
                "logs_over_time": {
                    "date_histogram": {"field": "timestamp", "calendar_interval": "1h"}
                },
            }

            result = await self.client.search(
                index=self.index_name,
                body={"query": query, "aggs": aggs, "size": 0},
            )

            return {
                "total_logs": result["hits"]["total"]["value"],
                "level_distribution": [
                    {"level": bucket["key"], "count": bucket["doc_count"]}
                    for bucket in result["aggregations"]["level_distribution"][
                        "buckets"
                    ]
                ],
                "timeline": [
                    {
                        "timestamp": bucket["key_as_string"],
                        "count": bucket["doc_count"],
                    }
                    for bucket in result["aggregations"]["logs_over_time"]["buckets"]
                ],
            }
        except Exception as e:
            logger.error(f"통계 조회 실패: {str(e)}", exc_info=True)
            return {}

    async def close(self):
        """클라이언트 종료"""
        if self.enabled and self.client:
            await self.client.close()
            logger.info("Elasticsearch 클라이언트 종료")

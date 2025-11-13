from typing import List

from fastapi import APIRouter, Depends, HTTPException

from dto.log.log_dto import ExecutionLogResponse, ExecutionLogSearchResponse
from dto.workflow.workflow_dto import WorkflowDeleteResponse
from helpers.utils.dependencies import get_workflow_log_service
from services.workflow.workflow_log_service import WorkflowLogService

router = APIRouter(prefix="/v1/logs", tags=["logs"])


# === 워크플로우 실행 로그 조회 엔드포인트 (Elasticsearch) ===
@router.get("/logs", response_model=List[ExecutionLogResponse])
async def get_all_execution_logs(
    limit: int = 100,
    offset: int = 0,
    log_service: WorkflowLogService = Depends(get_workflow_log_service),
):
    """모든 워크플로우 실행 로그 조회 (Elasticsearch)"""
    try:
        logs = await log_service.get_all_logs(limit=limit, offset=offset)
        return [ExecutionLogResponse(**log) for log in logs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{graph_id}/logs", response_model=List[ExecutionLogResponse])
async def get_workflow_execution_logs(
    graph_id: int,
    limit: int = 100,
    offset: int = 0,
    log_service: WorkflowLogService = Depends(get_workflow_log_service),
):
    """특정 워크플로우의 실행 로그 목록 조회 (Elasticsearch)"""
    try:
        logs = await log_service.get_logs_by_graph_id(
            graph_id=graph_id, limit=limit, offset=offset
        )
        return [ExecutionLogResponse(**log) for log in logs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/logs/{execution_id}", response_model=ExecutionLogResponse)
async def get_execution_log_by_id(
    execution_id: str,
    include_messages: bool = True,
    log_service: WorkflowLogService = Depends(get_workflow_log_service),
):
    """
    실행 ID로 특정 워크플로우 실행 로그 조회 (Elasticsearch)

    Args:
        execution_id: 실행 ID
        include_messages: 상세 로그 메시지 포함 여부 (기본: True)
    """
    try:
        log = await log_service.get_log_by_execution_id(
            execution_id, include_messages=include_messages
        )
        if not log:
            raise HTTPException(status_code=404, detail="로그를 찾을 수 없습니다")
        return ExecutionLogResponse(**log)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{graph_id}/logs/search", response_model=ExecutionLogSearchResponse)
async def search_workflow_logs(
    graph_id: int,
    query: str | None = None,
    level: str | None = None,
    limit: int = 100,
    log_service: WorkflowLogService = Depends(get_workflow_log_service),
):
    """
    워크플로우 로그 전문 검색 (Elasticsearch)

    Args:
        graph_id: 워크플로우 ID
        query: 검색어 (로그 메시지 내 전문 검색)
        level: 로그 레벨 (INFO, ERROR, WARNING, DEBUG)
        limit: 결과 개수 제한

    예시:
        - /workflows/1/logs/search?query=timeout
        - /workflows/1/logs/search?level=ERROR
        - /workflows/1/logs/search?query=노드 실행&level=ERROR
    """
    try:
        results = await log_service.search_logs(
            graph_id=graph_id, query=query, level=level, limit=limit
        )
        return ExecutionLogSearchResponse(**results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/logs/{execution_id}", response_model=WorkflowDeleteResponse)
async def delete_execution_log(
    execution_id: str,
    log_service: WorkflowLogService = Depends(get_workflow_log_service),
):
    """실행 ID로 워크플로우 실행 로그 삭제 (Elasticsearch)"""
    try:
        result = await log_service.delete_log(execution_id)
        if not result.get("success"):
            raise HTTPException(
                status_code=404, detail=result.get("message", "로그를 찾을 수 없습니다")
            )
        return WorkflowDeleteResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

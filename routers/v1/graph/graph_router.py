from fastapi import APIRouter, Depends, HTTPException

from dto.graph.graph_dto import GraphMetadataResponse
from dto.workflow.workflow_dto import WorkflowDeleteResponse
from helpers.utils.dependencies import get_graph_service
from services.graph.graph_service import GraphService

router = APIRouter(prefix="/v1/graphs", tags=["graphs"])


# === Graph 메타데이터 전용 엔드포인트 ===
@router.get("/{graph_id}/metadata", response_model=GraphMetadataResponse)
async def get_graph_metadata(
    graph_id: int, graph_service: GraphService = Depends(get_graph_service)
):
    """그래프 메타데이터만 조회 (워크플로우 구조는 제외)"""
    try:
        graph = await graph_service.get_graph(graph_id)
        if not graph:
            raise HTTPException(status_code=404, detail="그래프를 찾을 수 없습니다")

        return GraphMetadataResponse(
            id=graph.id,
            name=graph.name,
            description=graph.description,
            properties=graph.properties,
            created_at=graph.created_at.isoformat() if graph.created_at else None,
            updated_at=graph.updated_at.isoformat() if graph.updated_at else None,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{graph_id}/metadata", response_model=WorkflowDeleteResponse)
async def delete_graph_metadata(
    graph_id: int, graph_service: GraphService = Depends(get_graph_service)
):
    """그래프 메타데이터만 삭제 (워크플로우는 유지)"""
    try:
        result = await graph_service.delete_graph_metadata(graph_id)
        return WorkflowDeleteResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

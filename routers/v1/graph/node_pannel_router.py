from typing import List

from fastapi import APIRouter, HTTPException

from dto.workflow.node_dto import NodePanelResponse
from helpers.node.node_templates.llm import temp_model_map
from services.workflow.node_panel_service import NodePanelService

router = APIRouter(prefix="/v1/node-pannel", tags=["node-pannel"])


@router.get("/node-types/", response_model=NodePanelResponse)
async def get_node_types():
    """사용 가능한 노드 타입들 조회"""
    try:
        return NodePanelService().get_node_types()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models/{provider}", response_model=List[str])
def get_models(provider: str):
    return temp_model_map[provider]

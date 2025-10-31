from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException

from database.graph.edge import Edge
from database.graph.graph import Graph
from database.graph.vertex import Vertex
from dto.workflow.workflow_dto import (
    WorkflowCreateRequest,
    WorkflowCreateResponse,
    WorkflowExecuteRequest,
    WorkflowUpdateRequest,
)
from helpers.node.node_base import NodeType
from helpers.utils.dependencies import (
    get_graph_service,
    get_workflow_execution_service,
    get_workflow_persistence_service,
)
from services.graph.graph_service import GraphService
from services.workflow.workflow_execution_service import WorkflowExecutionService
from services.workflow.workflow_persistence_service import WorkflowPersistenceService

router = APIRouter(prefix="/v1/workflows", tags=["workflows"])


@router.post("/", response_model=WorkflowCreateResponse)
async def create_workflow(
    request: WorkflowCreateRequest,
    persistence_service: WorkflowPersistenceService = Depends(
        get_workflow_persistence_service
    ),
):
    """워크플로우 생성"""
    try:
        # 그래프 생성
        graph = Graph(name=request.name, description=request.description)

        # 버텍스들 생성
        vertices: list[Vertex] = []
        vertex_temp_ids: list[int] = []  # 클라이언트의 임시 ID 저장
        for vertex_data in request.vertices:
            vertices.append(
                Vertex(type=vertex_data.type, properties=vertex_data.properties)
            )
            # 임시 ID가 제공된 경우 저장 (없으면 인덱스 사용)
            if vertex_data.id is not None:
                vertex_temp_ids.append(vertex_data.id)
            else:
                vertex_temp_ids.append(len(vertex_temp_ids))

        # 엣지들 생성
        edges: list[Edge] = []
        for edge_data in request.edges:
            edges.append(
                Edge(
                    source_id=edge_data.source_id,
                    target_id=edge_data.target_id,
                    type=edge_data.type,
                    source_properties=edge_data.source_properties,
                    target_properties=edge_data.target_properties,
                )
            )

        # 워크플로우 저장
        saved_graph = await persistence_service.save(
            graph, vertices, edges, vertex_temp_ids
        )

        return {
            "success": True,
            "graph_id": saved_graph.id,
            "message": "워크플로우가 성공적으로 생성되었습니다",
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[Dict[str, Any]])
async def get_workflows(graph_service: GraphService = Depends(get_graph_service)):
    """모든 워크플로우 조회"""
    try:
        graphs = await graph_service.get_graphs()
        return [
            {
                "id": graph.id,
                "name": graph.name,
                "description": graph.description,
                "created_at": (
                    graph.created_at.isoformat() if graph.created_at else None
                ),
                "updated_at": (
                    graph.updated_at.isoformat() if graph.updated_at else None
                ),
            }
            for graph in graphs
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{graph_id}", response_model=Dict[str, Any])
async def get_workflow(
    graph_id: int,
    persistence_service: WorkflowPersistenceService = Depends(
        get_workflow_persistence_service
    ),
):
    """특정 워크플로우 조회"""
    try:
        graph, vertices, edges = await persistence_service.load(graph_id)

        return {
            "graph": {
                "id": graph.id,
                "name": graph.name,
                "description": graph.description,
                "properties": graph.properties,
                "created_at": (
                    graph.created_at.isoformat() if graph.created_at else None
                ),
                "updated_at": (
                    graph.updated_at.isoformat() if graph.updated_at else None
                ),
            },
            "vertices": [
                {
                    "id": vertex.id,
                    "type": vertex.type,
                    "properties": vertex.properties,
                    "created_at": (
                        vertex.created_at.isoformat() if vertex.created_at else None
                    ),
                    "updated_at": (
                        vertex.updated_at.isoformat() if vertex.updated_at else None
                    ),
                }
                for vertex in vertices
            ],
            "edges": [
                {
                    "id": edge.id,
                    "source_id": edge.source_id,
                    "target_id": edge.target_id,
                    "type": edge.type,
                    "source_properties": edge.source_properties,
                    "target_properties": edge.target_properties,
                    "created_at": (
                        edge.created_at.isoformat() if edge.created_at else None
                    ),
                    "updated_at": (
                        edge.updated_at.isoformat() if edge.updated_at else None
                    ),
                }
                for edge in edges
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{graph_id}/execute", response_model=Dict[str, Any])
async def execute_workflow(
    graph_id: int,
    request: WorkflowExecuteRequest,
    execution_service: WorkflowExecutionService = Depends(
        get_workflow_execution_service
    ),
):
    """워크플로우 실행"""
    try:
        result = await execution_service.execute_workflow(
            graph_id, request.initial_inputs
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{graph_id}/status", response_model=Dict[str, Any])
async def get_workflow_status(
    graph_id: int,
    execution_service: WorkflowExecutionService = Depends(
        get_workflow_execution_service
    ),
):
    """워크플로우 상태 조회"""
    try:
        status = await execution_service.get_workflow_status(graph_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{graph_id}", response_model=Dict[str, Any])
async def delete_workflow(
    graph_id: int,
    persistence_service: WorkflowPersistenceService = Depends(
        get_workflow_persistence_service
    ),
):
    """워크플로우 삭제"""
    try:
        result = await persistence_service.delete(graph_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/node-types/", response_model=List[Dict[str, Any]])
async def get_node_types():
    """사용 가능한 노드 타입들 조회"""
    return [
        {
            "type": node_type.value,
            "name": node_type.name,
            "description": f"{node_type.name} 노드",
        }
        for node_type in NodeType
    ]


# === Graph 메타데이터 전용 엔드포인트 ===
@router.get("/{graph_id}/metadata", response_model=Dict[str, Any])
async def get_graph_metadata(
    graph_id: int, graph_service: GraphService = Depends(get_graph_service)
):
    """그래프 메타데이터만 조회 (워크플로우 구조는 제외)"""
    try:
        graph = await graph_service.get_graph(graph_id)
        if not graph:
            raise HTTPException(status_code=404, detail="그래프를 찾을 수 없습니다")

        return {
            "id": graph.id,
            "name": graph.name,
            "description": graph.description,
            "properties": graph.properties,
            "created_at": graph.created_at.isoformat() if graph.created_at else None,
            "updated_at": graph.updated_at.isoformat() if graph.updated_at else None,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{graph_id}/metadata", response_model=Dict[str, Any])
async def delete_graph_metadata(
    graph_id: int, graph_service: GraphService = Depends(get_graph_service)
):
    """그래프 메타데이터만 삭제 (워크플로우는 유지)"""
    try:
        result = await graph_service.delete_graph_metadata(graph_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === 노드 상태 조회 엔드포인트 ===
@router.get("/{graph_id}/nodes/{node_id}/status", response_model=Dict[str, Any])
async def get_node_status(
    graph_id: int,
    node_id: str,
    execution_service: WorkflowExecutionService = Depends(
        get_workflow_execution_service
    ),
):
    """특정 노드의 상태 조회"""
    try:
        status = await execution_service.get_node_status(graph_id, node_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{graph_id}", response_model=Dict[str, Any])
async def update_workflow(
    graph_id: int,
    request: WorkflowUpdateRequest,
    persistence_service: WorkflowPersistenceService = Depends(
        get_workflow_persistence_service
    ),
):
    """워크플로우 업데이트"""
    try:
        # 그래프 메타데이터 업데이트
        graph_updates = {}
        if request.name is not None:
            graph_updates["name"] = request.name
        if request.description is not None:
            graph_updates["description"] = request.description

        # 버텍스들 생성 (제공된 경우)
        vertices = None
        vertex_temp_ids = None
        if request.vertices is not None:
            vertices = []
            vertex_temp_ids = []
            for vertex_data in request.vertices:
                vertices.append(
                    Vertex(
                        type=vertex_data.type,
                        properties=vertex_data.properties,
                    )
                )
                # 임시 ID가 제공된 경우 저장 (없으면 인덱스 사용)
                if vertex_data.id is not None:
                    vertex_temp_ids.append(vertex_data.id)
                else:
                    vertex_temp_ids.append(len(vertex_temp_ids))

        # 엣지들 생성 (제공된 경우)
        edges = None
        if request.edges is not None:
            edges = []
            for edge_data in request.edges:
                edges.append(
                    Edge(
                        source_id=edge_data.source_id,
                        target_id=edge_data.target_id,
                        type=edge_data.type,
                        source_properties=edge_data.source_properties,
                        target_properties=edge_data.target_properties,
                    )
                )

        # 워크플로우 업데이트
        updated_graph = await persistence_service.update(
            graph_id=graph_id,
            graph_updates=graph_updates if graph_updates else None,
            vertices=vertices,
            edges=edges,
            vertex_temp_ids=vertex_temp_ids,
        )

        return {
            "success": True,
            "graph_id": updated_graph.id,
            "message": "워크플로우가 성공적으로 업데이트되었습니다",
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# TODO: websocket 연결 엔드포인트 구성

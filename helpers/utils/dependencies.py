from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.setup import get_async_db
from repositories.graph.edge_repository import EdgeRepository
from repositories.graph.graph_repository import GraphRepository
from repositories.graph.vertex_repository import VertexRepository
from services.graph.edge_service import EdgeService
from services.graph.graph_service import GraphService
from services.graph.vertex_service import VertexService
from services.workflow.workflow_execution_service import WorkflowExecutionService
from services.workflow.workflow_persistence_service import WorkflowPersistenceService


async def get_graph_repository(
    db: AsyncSession = Depends(get_async_db),
) -> GraphRepository:
    return GraphRepository(db)


async def get_vertex_repository(
    db: AsyncSession = Depends(get_async_db),
) -> VertexRepository:
    return VertexRepository(db)


async def get_edge_repository(
    db: AsyncSession = Depends(get_async_db),
) -> EdgeRepository:
    return EdgeRepository(db)


async def get_vertex_service(
    vertex_repository: VertexRepository = Depends(get_vertex_repository),
) -> VertexService:
    return VertexService(vertex_repository)


async def get_edge_service(
    edge_repository: EdgeRepository = Depends(get_edge_repository),
) -> EdgeService:
    return EdgeService(edge_repository)


async def get_workflow_persistence_service(
    graph_repository: GraphRepository = Depends(get_graph_repository),
    vertex_service: VertexService = Depends(get_vertex_service),
    edge_service: EdgeService = Depends(get_edge_service),
    vertex_repository: VertexRepository = Depends(get_vertex_repository),
    edge_repository: EdgeRepository = Depends(get_edge_repository),
) -> WorkflowPersistenceService:
    """워크플로우 영속성 서비스 의존성"""
    return WorkflowPersistenceService(
        graph_repository=graph_repository,
        vertex_service=vertex_service,
        edge_service=edge_service,
        vertex_repository=vertex_repository,
        edge_repository=edge_repository,
    )


async def get_workflow_execution_service(
    persistence_service: WorkflowPersistenceService = Depends(
        get_workflow_persistence_service
    ),
) -> WorkflowExecutionService:
    """워크플로우 실행 서비스 의존성"""
    return WorkflowExecutionService(persistence_service=persistence_service)


async def get_graph_service(
    graph_repository: GraphRepository = Depends(get_graph_repository),
) -> GraphService:
    """그래프 서비스 의존성 - Graph 메타데이터 관리만 담당"""
    return GraphService(graph_repository=graph_repository)

import asyncio
import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.setup import create_tables, validate
from routers.v1.graph.graph_router import router as graph_router
from routers.v1.graph.node_pannel_router import router as node_panel_router
from routers.v1.graph.workflow_router import router as workflow_router
from routers.v1.log.log_router import router as log_router
from routers.v1.websocket.websocket_router import router as websocket_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 시 테이블 생성
    await create_tables()
    yield
    # 서버 종료 시 정리 작업 (필요한 경우)


app = FastAPI(
    title="Workflow Agent Platform",
    description="""
    ## Workflow Agent Platform API
    
    Langflow와 같은 워크플로우 기반 에이전트 생성 플랫폼입니다.
    
    ### 주요 기능
    * 워크플로우 생성 및 관리
    * 노드 기반 그래프 구성
    * 워크플로우 실행 및 모니터링
    * 워크플로우 가져오기/내보내기
    
    ### API 사용법
    1. 워크플로우를 생성합니다
    2. 노드와 엣지를 정의합니다
    3. 워크플로우를 실행합니다
    4. 결과를 확인합니다
    """,
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@workflow-platform.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],  # React 개발 서버 (포트 5173과 5174 모두 허용)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)


@app.get("/")
def read_root():
    return {
        "message": "Workflow Agent Platform에 오신 것을 환영합니다!",
        "docs": "/docs",
        "workflows": "/workflows",
    }


# 워크플로우 라우터 추가
app.include_router(workflow_router, prefix="/api")

# 워크플로우 실행 로그 라우터 추가
app.include_router(log_router, prefix="/api")

# 그래프 라우터 추가
app.include_router(graph_router, prefix="/api")

# 노드 패널 라우터 추가
app.include_router(node_panel_router, prefix="/api")

# WebSocket 라우터 추가
app.include_router(websocket_router, prefix="/api")
if __name__ == "__main__":

    db_validate = asyncio.run(validate())
    if not db_validate:
        raise Exception("Database connection failed")

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))

    uvicorn.run(app, host=host, port=port)

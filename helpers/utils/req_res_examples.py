"""
API 요청/응답 예시 데이터 정의
프론트엔드 개발을 위한 Swagger/OpenAPI 문서에 표시될 예시 데이터
"""

from typing import Any, Dict

# === Node Properties 예시 ===

EXAMPLE_LLM_NODE_PROPERTIES: Dict[str, Any] = {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 1000,
    "system_prompt": "You are a helpful assistant.",
    "user_prompt": "Explain quantum computing in simple terms.",
}

EXAMPLE_API_NODE_PROPERTIES: Dict[str, Any] = {
    "url": "https://api.example.com/data",
    "method": "POST",
    "headers": {"Authorization": "Bearer token123", "Content-Type": "application/json"},
    "body": {"query": "search term", "limit": 10},
}

EXAMPLE_TRANSFORM_NODE_PROPERTIES: Dict[str, Any] = {
    "operation": "filter",
    "condition": "value > 100",
    "output_format": "json",
}

EXAMPLE_START_NODE_PROPERTIES: Dict[str, Any] = {
    "initial_data": {"user_id": "123", "request_type": "analysis"},
}

# === Edge Properties 예시 ===

EXAMPLE_EDGE_SOURCE_PROPERTIES: Dict[str, Any] = {
    "output_key": "result",
    "transform": "json",
}

EXAMPLE_EDGE_TARGET_PROPERTIES: Dict[str, Any] = {
    "input_key": "input_data",
    "required": True,
}

# === Graph Properties 예시 ===

EXAMPLE_GRAPH_PROPERTIES: Dict[str, Any] = {
    "version": "1.0.0",
    "author": "admin",
    "tags": ["data-processing", "ai"],
    "timeout": 300,
}

# === Execution Result 예시 ===

EXAMPLE_NODE_RESULTS: Dict[str, Any] = {
    "node_1": {"status": "completed", "output": "Analysis complete", "duration": 1.5},
    "node_2": {
        "status": "completed",
        "output": {"data": [1, 2, 3], "count": 3},
        "duration": 0.8,
    },
    "node_3": {"status": "completed", "output": "Final result", "duration": 2.1},
}

EXAMPLE_INITIAL_INPUTS: Dict[str, Any] = {
    "start_node": {"data": "input data", "parameters": {"mode": "fast"}},
}

# === 완전한 Request 예시 ===

EXAMPLE_VERTEX_CREATE_REQUEST = {
    "id": 1,
    "type": "llm_node",
    "properties": EXAMPLE_LLM_NODE_PROPERTIES,
}

EXAMPLE_EDGE_CREATE_REQUEST = {
    "source_id": 1,
    "target_id": 2,
    "type": "default",
    "source_properties": EXAMPLE_EDGE_SOURCE_PROPERTIES,
    "target_properties": EXAMPLE_EDGE_TARGET_PROPERTIES,
}

EXAMPLE_WORKFLOW_CREATE_REQUEST = {
    "name": "AI Data Processing Pipeline",
    "description": "워크플로우 예시: 데이터 수집 -> LLM 분석 -> 결과 저장",
    "vertices": [
        {"id": 1, "type": "start_node", "properties": EXAMPLE_START_NODE_PROPERTIES},
        {"id": 2, "type": "llm_node", "properties": EXAMPLE_LLM_NODE_PROPERTIES},
        {"id": 3, "type": "api_node", "properties": EXAMPLE_API_NODE_PROPERTIES},
    ],
    "edges": [
        {
            "source_id": 1,
            "target_id": 2,
            "type": "default",
            "source_properties": {"output_key": "data"},
            "target_properties": {"input_key": "input"},
        },
        {
            "source_id": 2,
            "target_id": 3,
            "type": "default",
            "source_properties": {"output_key": "result"},
            "target_properties": {"input_key": "analysis_result"},
        },
    ],
}

EXAMPLE_WORKFLOW_EXECUTE_REQUEST = {
    "initial_inputs": EXAMPLE_INITIAL_INPUTS,
}

EXAMPLE_WORKFLOW_UPDATE_REQUEST = {
    "name": "Updated Pipeline Name",
    "description": "Updated description",
    "vertices": [
        {"id": 1, "type": "start_node", "properties": EXAMPLE_START_NODE_PROPERTIES},
        {"id": 2, "type": "llm_node", "properties": EXAMPLE_LLM_NODE_PROPERTIES},
    ],
    "edges": [
        {
            "source_id": 1,
            "target_id": 2,
            "type": "default",
            "source_properties": {},
            "target_properties": {},
        }
    ],
}

# === Response 예시 ===

EXAMPLE_WORKFLOW_CREATE_RESPONSE = {
    "success": True,
    "graph_id": 123,
    "message": "워크플로우가 성공적으로 생성되었습니다",
}

EXAMPLE_WORKFLOW_SUMMARY_RESPONSE = {
    "id": 123,
    "name": "AI Data Processing Pipeline",
    "description": "워크플로우 예시: 데이터 수집 -> LLM 분석 -> 결과 저장",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T14:20:00Z",
}

EXAMPLE_GRAPH_DETAIL_RESPONSE = {
    "id": 123,
    "name": "AI Data Processing Pipeline",
    "description": "워크플로우 예시",
    "properties": EXAMPLE_GRAPH_PROPERTIES,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T14:20:00Z",
}

EXAMPLE_VERTEX_DETAIL_RESPONSE = {
    "id": 1,
    "type": "llm_node",
    "properties": EXAMPLE_LLM_NODE_PROPERTIES,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T14:20:00Z",
}

EXAMPLE_EDGE_DETAIL_RESPONSE = {
    "id": 1,
    "source_id": 1,
    "target_id": 2,
    "type": "default",
    "source_properties": EXAMPLE_EDGE_SOURCE_PROPERTIES,
    "target_properties": EXAMPLE_EDGE_TARGET_PROPERTIES,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T14:20:00Z",
}

EXAMPLE_WORKFLOW_DETAIL_RESPONSE = {
    "graph": EXAMPLE_GRAPH_DETAIL_RESPONSE,
    "vertices": [
        {
            "id": 1,
            "type": "start_node",
            "properties": EXAMPLE_START_NODE_PROPERTIES,
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
        },
        {
            "id": 2,
            "type": "llm_node",
            "properties": EXAMPLE_LLM_NODE_PROPERTIES,
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
        },
    ],
    "edges": [
        {
            "id": 1,
            "source_id": 1,
            "target_id": 2,
            "type": "default",
            "source_properties": EXAMPLE_EDGE_SOURCE_PROPERTIES,
            "target_properties": EXAMPLE_EDGE_TARGET_PROPERTIES,
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
        }
    ],
}

EXAMPLE_WORKFLOW_EXECUTE_RESPONSE = {
    "success": True,
    "result": EXAMPLE_NODE_RESULTS,
    "errors": [],
    "execution_order": ["node_1", "node_2", "node_3"],
    "execution_time": 4.5,
    "start_time": "2024-01-15T10:35:00Z",
    "end_time": "2024-01-15T10:35:04.5Z",
}

EXAMPLE_WORKFLOW_STATUS_RESPONSE = {
    "graph_id": 123,
    "status": "running",
    "execution_id": "exec_abc123def456",
    "current_node": "node_2",
    "progress": 0.66,
    "message": "노드 2 실행 중...",
}

EXAMPLE_NODE_STATUS_RESPONSE = {
    "node_id": "node_2",
    "status": "completed",
    "progress": 1.0,
    "result": {"output": "Analysis complete", "confidence": 0.95},
    "error": None,
    "started_at": "2024-01-15T10:35:01Z",
    "completed_at": "2024-01-15T10:35:02.5Z",
}

EXAMPLE_WORKFLOW_DELETE_RESPONSE = {
    "success": True,
    "message": "워크플로우가 성공적으로 삭제되었습니다",
    "graph_id": 123,
}

EXAMPLE_WORKFLOW_UPDATE_RESPONSE = {
    "success": True,
    "graph_id": 123,
    "message": "워크플로우가 성공적으로 업데이트되었습니다",
}

EXAMPLE_GRAPH_METADATA_RESPONSE = {
    "id": 123,
    "name": "AI Data Processing Pipeline",
    "description": "워크플로우 예시",
    "properties": EXAMPLE_GRAPH_PROPERTIES,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T14:20:00Z",
}

EXAMPLE_EXECUTION_LOG_MESSAGE_RESPONSE = {
    "timestamp": "2024-01-15T10:35:01.234Z",
    "level": "INFO",
    "message": "노드 1 실행 시작",
    "node_id": "node_1",
}

EXAMPLE_EXECUTION_LOG_RESPONSE = {
    "execution_id": "exec_abc123def456",
    "graph_id": 123,
    "status": "completed",
    "started_at": "2024-01-15T10:35:00Z",
    "completed_at": "2024-01-15T10:35:04.5Z",
    "execution_time": 4.5,
    "success": True,
    "error": None,
    "node_results": EXAMPLE_NODE_RESULTS,
    "execution_order": ["node_1", "node_2", "node_3"],
    "messages": [
        {
            "timestamp": "2024-01-15T10:35:00.100Z",
            "level": "INFO",
            "message": "워크플로우 실행 시작",
            "node_id": None,
        },
        {
            "timestamp": "2024-01-15T10:35:01.234Z",
            "level": "INFO",
            "message": "노드 1 실행 완료",
            "node_id": "node_1",
        },
        {
            "timestamp": "2024-01-15T10:35:03.456Z",
            "level": "INFO",
            "message": "노드 2 실행 완료",
            "node_id": "node_2",
        },
    ],
}

EXAMPLE_EXECUTION_LOG_SEARCH_RESPONSE = {
    "total": 15,
    "logs": [EXAMPLE_EXECUTION_LOG_RESPONSE],
    "query": "error",
    "level": "ERROR",
}

EXAMPLE_NODE_INPUTS = [
    {
        "name": "user_prompt",
        "type": "TEXT",
        "description": "LLM에 전달할 프롬프트",
    }
]

EXAMPLE_NODE_OUTPUTS = [
    {
        "name": "response",
        "type": "TEXT",
        "description": "LLM 응답",
    }
]

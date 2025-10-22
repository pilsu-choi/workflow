# from unittest.mock import AsyncMock, patch

# import pytest
# from fastapi.testclient import TestClient
# from httpx import AsyncClient

# from main import app
# from services.graph.graph_service import GraphService


# class TestCreateSimpleWorkflow:
#     """create_simple_workflow() 함수에 대한 테스트 클래스"""

#     def setup_method(self):
#         """각 테스트 메서드 실행 전 설정"""
#         self.client = TestClient(app)
#         self.test_workflow_name = "Test Simple Workflow"
#         self.test_workflow_description = "This is a test simple workflow"

#     def test_create_simple_workflow_success(self):
#         """성공적인 간단한 워크플로우 생성 테스트"""
#         # Mock GraphService의 create_simple_workflow 메서드
#         mock_result = {
#             "success": True,
#             "graph_id": 1,
#             "message": "간단한 워크플로우가 성공적으로 생성되었습니다",
#             "workflow": {
#                 "name": self.test_workflow_name,
#                 "description": self.test_workflow_description,
#                 "vertices": [
#                     {"id": 1, "type": "start", "properties": {}},
#                     {
#                         "id": 2,
#                         "type": "process",
#                         "properties": {"action": "test_action"},
#                     },
#                     {"id": 3, "type": "end", "properties": {}},
#                 ],
#                 "edges": [
#                     {"id": 1, "source_id": 1, "target_id": 2, "type": "default"},
#                     {"id": 2, "source_id": 2, "target_id": 3, "type": "default"},
#                 ],
#             },
#         }

#         with patch(
#             "routers.v1.graph.workflow_router.get_graph_service"
#         ) as mock_get_service:
#             # Mock GraphService 인스턴스 생성
#             mock_graph_service = AsyncMock(spec=GraphService)
#             mock_graph_service.create_simple_workflow.return_value = mock_result
#             mock_get_service.return_value = mock_graph_service

#             # 테스트 요청 데이터
#             request_data = {
#                 "name": self.test_workflow_name,
#                 "description": self.test_workflow_description,
#             }

#             # API 호출
#             response = self.client.post("/workflows/simple", json=request_data)

#             # 응답 검증
#             assert response.status_code == 200
#             response_data = response.json()
#             assert response_data["success"] is True
#             assert response_data["graph_id"] == 1
#             assert "message" in response_data
#             assert "workflow" in response_data

#             # GraphService 메서드가 올바른 파라미터로 호출되었는지 확인
#             mock_graph_service.create_simple_workflow.assert_called_once_with(
#                 self.test_workflow_name, self.test_workflow_description
#             )

#     def test_create_simple_workflow_missing_name(self):
#         """name 필드가 누락된 경우 테스트"""
#         request_data = {"description": self.test_workflow_description}

#         response = self.client.post("/workflows/simple", json=request_data)
#         assert response.status_code == 422  # Validation error

#     def test_create_simple_workflow_empty_name(self):
#         """빈 name 필드 테스트"""
#         request_data = {"name": "", "description": self.test_workflow_description}

#         response = self.client.post("/workflows/simple", json=request_data)
#         assert response.status_code == 422  # Validation error

#     def test_create_simple_workflow_without_description(self):
#         """description 필드 없이 테스트 (선택적 필드)"""
#         mock_result = {
#             "success": True,
#             "graph_id": 2,
#             "message": "간단한 워크플로우가 성공적으로 생성되었습니다",
#         }

#         with patch(
#             "routers.v1.graph.workflow_router.get_graph_service"
#         ) as mock_get_service:
#             mock_graph_service = AsyncMock(spec=GraphService)
#             mock_graph_service.create_simple_workflow.return_value = mock_result
#             mock_get_service.return_value = mock_graph_service

#             request_data = {"name": self.test_workflow_name}

#             response = self.client.post("/workflows/simple", json=request_data)
#             assert response.status_code == 200
#             response_data = response.json()
#             assert response_data["success"] is True

#             # description이 빈 문자열로 전달되는지 확인
#             mock_graph_service.create_simple_workflow.assert_called_once_with(
#                 self.test_workflow_name, ""
#             )

#     def test_create_simple_workflow_service_error(self):
#         """GraphService에서 에러가 발생한 경우 테스트"""
#         with patch(
#             "routers.v1.graph.workflow_router.get_graph_service"
#         ) as mock_get_service:
#             mock_graph_service = AsyncMock(spec=GraphService)
#             mock_graph_service.create_simple_workflow.side_effect = Exception(
#                 "Database connection failed"
#             )
#             mock_get_service.return_value = mock_graph_service

#             request_data = {
#                 "name": self.test_workflow_name,
#                 "description": self.test_workflow_description,
#             }

#             response = self.client.post("/workflows/simple", json=request_data)
#             assert response.status_code == 400
#             response_data = response.json()
#             assert "detail" in response_data
#             assert "Database connection failed" in response_data["detail"]

#     def test_create_simple_workflow_invalid_json(self):
#         """잘못된 JSON 형식 테스트"""
#         response = self.client.post(
#             "/workflows/simple",
#             data="invalid json",
#             headers={"Content-Type": "application/json"},
#         )
#         assert response.status_code == 422

#     def test_create_simple_workflow_extra_fields(self):
#         """추가 필드가 포함된 요청 테스트 (Pydantic이 무시해야 함)"""
#         mock_result = {
#             "success": True,
#             "graph_id": 3,
#             "message": "간단한 워크플로우가 성공적으로 생성되었습니다",
#         }

#         with patch(
#             "routers.v1.graph.workflow_router.get_graph_service"
#         ) as mock_get_service:
#             mock_graph_service = AsyncMock(spec=GraphService)
#             mock_graph_service.create_simple_workflow.return_value = mock_result
#             mock_get_service.return_value = mock_graph_service

#             request_data = {
#                 "name": self.test_workflow_name,
#                 "description": self.test_workflow_description,
#                 "extra_field": "should_be_ignored",
#                 "another_field": 123,
#             }

#             response = self.client.post("/workflows/simple", json=request_data)
#             assert response.status_code == 200
#             response_data = response.json()
#             assert response_data["success"] is True

#             # 추가 필드는 무시되고 기본 필드만 전달되는지 확인
#             mock_graph_service.create_simple_workflow.assert_called_once_with(
#                 self.test_workflow_name, self.test_workflow_description
#             )


# class TestCreateSimpleWorkflowIntegration:
#     """create_simple_workflow() 통합 테스트 클래스"""

#     @pytest.mark.asyncio
#     async def test_create_simple_workflow_async_client(self):
#         """AsyncClient를 사용한 비동기 통합 테스트"""
#         async with AsyncClient(app=app, base_url="http://test") as ac:
#             mock_result = {
#                 "success": True,
#                 "graph_id": 4,
#                 "message": "간단한 워크플로우가 성공적으로 생성되었습니다",
#             }

#             with patch(
#                 "routers.v1.graph.workflow_router.get_graph_service"
#             ) as mock_get_service:
#                 mock_graph_service = AsyncMock(spec=GraphService)
#                 mock_graph_service.create_simple_workflow.return_value = mock_result
#                 mock_get_service.return_value = mock_graph_service

#                 request_data = {
#                     "name": "Async Test Workflow",
#                     "description": "Async integration test",
#                 }

#                 response = await ac.post("/workflows/simple", json=request_data)
#                 assert response.status_code == 200
#                 response_data = response.json()
#                 assert response_data["success"] is True
#                 assert response_data["graph_id"] == 4


# class TestSimpleWorkflowRequestValidation:
#     """SimpleWorkflowRequest DTO 검증 테스트"""

#     def test_simple_workflow_request_valid(self):
#         """유효한 SimpleWorkflowRequest 생성 테스트"""
#         request = SimpleWorkflowRequest(
#             name="Valid Workflow", description="Valid description"
#         )
#         assert request.name == "Valid Workflow"
#         assert request.description == "Valid description"

#     def test_simple_workflow_request_default_description(self):
#         """기본 description 값 테스트"""
#         request = SimpleWorkflowRequest(name="Test Workflow")
#         assert request.name == "Test Workflow"
#         assert request.description == ""

#     def test_simple_workflow_request_invalid_name(self):
#         """잘못된 name 타입 테스트"""
#         with pytest.raises(ValueError):
#             SimpleWorkflowRequest(name=None, description="Test")

#     def test_simple_workflow_request_empty_name(self):
#         """빈 문자열 name 테스트"""
#         with pytest.raises(ValueError):
#             SimpleWorkflowRequest(name="", description="Test")


# if __name__ == "__main__":
#     # 테스트 실행을 위한 간단한 스크립트
#     pytest.main([__file__, "-v"])

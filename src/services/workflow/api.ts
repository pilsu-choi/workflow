import axios from "axios";
import type {
  Graph,
  WorkflowDetail,
  WorkflowCreateRequest,
  WorkflowCreateResponse,
  WorkflowExecuteRequest,
  WorkflowExecuteResponse,
  WorkflowStatus,
  NodeStatus,
  NodeType,
} from "../../types/workflow";

const API_BASE_URL = "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Workflow API
export const workflowApi = {
  // Get all workflows (returns list of graphs)
  getWorkflows: () => api.get<Graph[]>("/v1/workflows/"),

  // Get workflow by ID (returns graph with vertices and edges)
  getWorkflow: (graphId: number) =>
    api.get<WorkflowDetail>(`/v1/workflows/${graphId}`),

  // Create workflow
  createWorkflow: (data: WorkflowCreateRequest) =>
    api.post<WorkflowCreateResponse>("/v1/workflows/", data),

  // Update workflow
  updateWorkflow: (graphId: number, data: WorkflowCreateRequest) =>
    api.put<WorkflowCreateResponse>(`/v1/workflows/${graphId}`, data),

  // Delete workflow
  deleteWorkflow: (graphId: number) =>
    api.delete<{ success: boolean; message: string }>(
      `/v1/workflows/${graphId}`
    ),

  // Get graph metadata only (without vertices and edges)
  getGraphMetadata: (graphId: number) =>
    api.get<Graph>(`/v1/workflows/${graphId}/metadata`),

  // Delete graph metadata only
  deleteGraphMetadata: (graphId: number) =>
    api.delete<{ success: boolean; message: string }>(
      `/v1/workflows/${graphId}/metadata`
    ),

  // Get available node types
  getNodeTypes: () => api.get<NodeType[]>("/v1/workflows/node-types/"),

  // Execute workflow
  executeWorkflow: (graphId: number, data: WorkflowExecuteRequest) =>
    api.post<WorkflowExecuteResponse>(`/v1/workflows/${graphId}/execute`, data),

  // Get workflow status
  getWorkflowStatus: (graphId: number) =>
    api.get<WorkflowStatus>(`/v1/workflows/${graphId}/status`),

  // Get specific node status
  getNodeStatus: (graphId: number, nodeId: string) =>
    api.get<NodeStatus>(`/v1/workflows/${graphId}/nodes/${nodeId}/status`),
};

export default api;

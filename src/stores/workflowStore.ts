import { create } from "zustand";
import { devtools } from "zustand/middleware";
import { addEdge, applyNodeChanges, applyEdgeChanges } from "@xyflow/react";
import type {
  Connection,
  EdgeChange,
  NodeChange,
  OnNodesChange,
  OnEdgesChange,
  OnConnect,
} from "@xyflow/react";
import type { Workflow, WorkflowNode, WorkflowEdge, NodeData } from "../types";

interface WorkflowState {
  // 현재 워크플로우
  currentWorkflow: Workflow | null;

  // ReactFlow 노드 및 엣지
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];

  // 선택된 노드
  selectedNode: WorkflowNode | null;

  // 사이드바 상태
  isSidebarOpen: boolean;

  // 변경 사항 추적
  isDirty: boolean;

  // Actions
  setCurrentWorkflow: (workflow: Workflow | null) => void;
  setNodes: (nodes: WorkflowNode[]) => void;
  setEdges: (edges: WorkflowEdge[]) => void;
  onNodesChange: OnNodesChange;
  onEdgesChange: OnEdgesChange;
  onConnect: OnConnect;
  addNode: (node: WorkflowNode) => void;
  updateNode: (id: string, data: Partial<NodeData>) => void;
  deleteNode: (id: string) => void;
  setSelectedNode: (node: WorkflowNode | null) => void;
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  resetWorkflow: () => void;
  setIsDirty: (dirty: boolean) => void;
}

export const useWorkflowStore = create<WorkflowState>()(
  devtools(
    (set, get) => ({
      // Initial state
      currentWorkflow: null,
      nodes: [],
      edges: [],
      selectedNode: null,
      isSidebarOpen: true,
      isDirty: false,

      // Set current workflow
      setCurrentWorkflow: (workflow) => {
        set({
          currentWorkflow: workflow,
          nodes: workflow?.nodes || [],
          edges: workflow?.edges || [],
          isDirty: false,
        });
      },

      // Set nodes
      setNodes: (nodes) => {
        set({ nodes, isDirty: true });
      },

      // Set edges
      setEdges: (edges) => {
        set({ edges, isDirty: true });
      },

      // Handle node changes
      onNodesChange: (changes: NodeChange[]) => {
        set({
          nodes: applyNodeChanges(changes, get().nodes),
          isDirty: true,
        });
      },

      // Handle edge changes
      onEdgesChange: (changes: EdgeChange[]) => {
        set({
          edges: applyEdgeChanges(changes, get().edges),
          isDirty: true,
        });
      },

      // Handle connection
      onConnect: (connection: Connection) => {
        set({
          edges: addEdge(connection, get().edges),
          isDirty: true,
        });
      },

      // Add node
      addNode: (node) => {
        set({
          nodes: [...get().nodes, node],
          isDirty: true,
        });
      },

      // Update node
      updateNode: (id, data) => {
        set({
          nodes: get().nodes.map((node) =>
            node.id === id ? { ...node, data: { ...node.data, ...data } } : node
          ),
          isDirty: true,
        });
      },

      // Delete node
      deleteNode: (id) => {
        set({
          nodes: get().nodes.filter((node) => node.id !== id),
          edges: get().edges.filter(
            (edge) => edge.source !== id && edge.target !== id
          ),
          selectedNode:
            get().selectedNode?.id === id ? null : get().selectedNode,
          isDirty: true,
        });
      },

      // Set selected node
      setSelectedNode: (node) => {
        set({ selectedNode: node });
      },

      // Toggle sidebar
      toggleSidebar: () => {
        set({ isSidebarOpen: !get().isSidebarOpen });
      },

      // Set sidebar open
      setSidebarOpen: (open) => {
        set({ isSidebarOpen: open });
      },

      // Reset workflow
      resetWorkflow: () => {
        set({
          currentWorkflow: null,
          nodes: [],
          edges: [],
          selectedNode: null,
          isDirty: false,
        });
      },

      // Set dirty flag
      setIsDirty: (dirty) => {
        set({ isDirty: dirty });
      },
    }),
    { name: "workflow-store" }
  )
);

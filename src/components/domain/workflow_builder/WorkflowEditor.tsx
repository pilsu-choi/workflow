import React, { useState, useCallback, useEffect, useRef } from "react";
import {
  ReactFlow,
  type Node,
  addEdge,
  type Connection,
  useNodesState,
  useEdgesState,
  Controls,
  Background,
  MiniMap,
  type NodeTypes,
  BackgroundVariant,
  type ReactFlowInstance,
  applyEdgeChanges,
  type EdgeChange,
  ReactFlowProvider,
} from "@xyflow/react";
import { Box, CircularProgress } from "@mui/material";
import "@xyflow/react/dist/style.css";

import {
  type FlowNode,
  type FlowEdge,
  type Graph,
  type Vertex,
  type Edge as WorkflowEdge,
  type NodeTypeDefinition,
} from "../../../types/workflow";
import { workflowApi } from "../../../services/workflow/api";
import CustomNode from "./CustomNode";
import NodePanel from "./NodePanel";
import WorkflowToolbar from "./WorkflowToolbar";
import NodePalette from "./NodePalette";
const nodeTypes: NodeTypes = {
  custom: CustomNode,
};

const WorkflowEditor: React.FC<{ workflowId: number }> = ({ workflowId }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState<Node>([]);
  const [edges, setEdges] = useEdgesState([]);
  const [workflow, setWorkflow] = useState<Graph | null>(null);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [vertices, setVertices] = useState<Vertex[]>([]);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [workflowEdges, setWorkflowEdges] = useState<WorkflowEdge[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [reactFlowInstance, setReactFlowInstance] =
    useState<ReactFlowInstance | null>(null);
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const nextTempId = useRef(-1); // For temporary IDs before saving
  const [saving, setSaving] = useState(false);
  const [NODE_TYPES, setNODE_TYPES] = useState<NodeTypeDefinition[]>([]);

  // Load node types first
  useEffect(() => {
    const loadNodeTypes = async () => {
      try {
        const nodeTypesResponse = await workflowApi.getNodeTypes();
        setNODE_TYPES(nodeTypesResponse.data);
      } catch (error) {
        console.error("Failed to load node types:", error);
      }
    };
    loadNodeTypes();
  }, []);

  const loadWorkflowData = useCallback(async () => {
    // Wait for NODE_TYPES to be loaded
    if (NODE_TYPES.length === 0) return;

    try {
      setLoading(true);
      const response = await workflowApi.getWorkflow(workflowId);
      const {
        graph,
        vertices: loadedVertices,
        edges: loadedEdges,
      } = response.data;

      setWorkflow(graph);
      setVertices(loadedVertices);
      setWorkflowEdges(loadedEdges);

      // Convert vertices to React Flow nodes
      const flowNodes: FlowNode[] = loadedVertices.map((vertex) => {
        const nodeDefinition = NODE_TYPES.find(
          (n: NodeTypeDefinition) => n.type === vertex.type
        );
        const position = vertex.properties?.position || { x: 100, y: 100 };

        return {
          id: vertex.id?.toString() || `temp-${nextTempId.current--}`,
          type: "custom",
          position: { x: position.x, y: position.y },
          data: {
            label: vertex.properties?.label || vertex.type,
            nodeType: vertex.type,
            config: vertex.properties.config || {},
            originalId: vertex.id,
            category: nodeDefinition?.category,
            inputs: nodeDefinition?.inputs,
            outputs: nodeDefinition?.outputs,
          },
        };
      });

      // Convert edges to React Flow edges
      const flowEdges: FlowEdge[] = loadedEdges.map((edge) => ({
        id: edge.id?.toString() || `temp-edge-${nextTempId.current--}`,
        source: edge.source_id.toString(),
        target: edge.target_id.toString(),
        sourceHandle:
          edge.source_properties?.source_id ||
          edge.source_properties?.handle ||
          undefined,
        targetHandle:
          edge.target_properties?.target_id ||
          edge.target_properties?.handle ||
          undefined,
        originalId: edge.id,
      }));

      setNodes(flowNodes);
      setEdges(flowEdges);
    } catch (error) {
      console.error("Failed to load workflow data:", error);
    } finally {
      setLoading(false);
    }
  }, [workflowId, NODE_TYPES]);

  // Load workflow data after NODE_TYPES is loaded
  useEffect(() => {
    if (NODE_TYPES.length > 0) {
      loadWorkflowData();
    }
  }, [workflowId, loadWorkflowData, NODE_TYPES]);

  const onConnect = useCallback(
    (params: Connection) => {
      if (!params.source || !params.target) return;

      // Create edge locally (will be saved when workflow is saved)
      const newEdge: FlowEdge = {
        id: `temp-edge-${nextTempId.current--}`,
        source: params.source,
        target: params.target,
        sourceHandle: params.sourceHandle || undefined,
        targetHandle: params.targetHandle || undefined,
      };

      setEdges((eds) => addEdge(newEdge, eds));

      // Update workflowEdges state
      // Find the actual node IDs (handle temp IDs)
      const sourceNode = nodes.find((n) => n.id === params.source);
      const targetNode = nodes.find((n) => n.id === params.target);

      // Use originalId if available, otherwise parse the ID
      const sourceId = sourceNode?.data.originalId ?? parseInt(params.source);
      const targetId = targetNode?.data.originalId ?? parseInt(params.target);

      const newWorkflowEdge: WorkflowEdge = {
        source_id: sourceId,
        target_id: targetId,
        type: "default",
        source_properties: {
          name: params.sourceHandle || undefined,
        },
        target_properties: {
          name: params.targetHandle || undefined,
        },
      };
      setWorkflowEdges((edges) => [...edges, newWorkflowEdge]);
    },
    [setEdges, nodes]
  );

  const onNodeClick = useCallback((_event: React.MouseEvent, node: Node) => {
    setSelectedNode(node);
  }, []);

  const onPaneClick = useCallback(() => {
    setSelectedNode(null);
  }, []);

  const handleNodeUpdate = useCallback((nodeId: string, updates: any) => {
    // Update locally (will be saved when workflow is saved)
    setNodes((nds: Node[]) =>
      nds.map((node: Node) => {
        const matches = String(node.id) === String(nodeId);

        if (matches) {
          return {
            ...node,
            data: { ...node.data },
            position:
              updates.position_x !== undefined &&
              updates.position_y !== undefined
                ? { x: updates.position_x, y: updates.position_y }
                : node.position,
            node_config: updates.node_config || {},
          };
        } else {
          return node;
        }
      })
    );

    // Update vertices state
    setVertices((verts) =>
      verts.map((vertex) =>
        vertex.id?.toString() === nodeId
          ? {
              ...vertex,
              properties: {
                ...vertex.properties,
                ...updates,
              },
            }
          : vertex
      )
    );
  }, []);

  // Handle node position changes
  const handleNodesChange = useCallback(
    (changes: any[]) => {
      onNodesChange(changes);
      // Note: vertices positions will be synced when saving, not during drag
      // This prevents performance issues during node dragging
    },
    [onNodesChange]
  );

  // Handle edge changes while preserving sourceHandle and targetHandle
  const handleEdgesChange = useCallback(
    (changes: EdgeChange[]) => {
      setEdges((eds) => {
        // Apply changes while preserving edge properties
        const updatedEdges = applyEdgeChanges(changes, eds);

        // Restore sourceHandle and targetHandle for all edges
        return updatedEdges.map((edge) => {
          const originalEdge = eds.find((e) => e.id === edge.id);
          if (originalEdge) {
            return {
              ...edge,
              sourceHandle: originalEdge.sourceHandle,
              targetHandle: originalEdge.targetHandle,
            };
          }
          return edge;
        });
      });
    },
    [setEdges]
  );

  const handleNodeDelete = useCallback((nodeId: string) => {
    // Delete locally (will be saved when workflow is saved)
    setNodes((nds) => nds.filter((node) => node.id !== nodeId));
    setEdges((eds) =>
      eds.filter((edge) => edge.source !== nodeId && edge.target !== nodeId)
    );

    // Update vertices state
    setVertices((verts) =>
      verts.filter((vertex) => vertex.id?.toString() !== nodeId)
    );

    // Update workflowEdges state
    const nodeIdNum = parseInt(nodeId);
    setWorkflowEdges((edges) =>
      edges.filter(
        (edge) => edge.source_id !== nodeIdNum && edge.target_id !== nodeIdNum
      )
    );

    setSelectedNode(null);
  }, []);

  const handleAddNode = useCallback(
    (nodeType: string, position?: { x: number; y: number }) => {
      const nodeDefinition = NODE_TYPES.find((node) => node.type === nodeType);
      if (!nodeDefinition) {
        console.error("Node type not found:", nodeType);
        return;
      }

      // Use provided position or generate random position
      const nodePosition = position || {
        x: 100 + Math.random() * 200,
        y: 100 + Math.random() * 200,
      };

      // Generate temporary ID
      const tempId = nextTempId.current--;
      const nodeId = `temp-${tempId}`;

      // Create new vertex
      const newVertex: Vertex = {
        type: nodeType,
        properties: {
          label: nodeDefinition.label,
          position: {
            x: Math.round(nodePosition.x),
            y: Math.round(nodePosition.y),
          },
          // config: {}, //nodeDefinition,
        },
      };

      // Add to vertices state
      setVertices((verts) => [...verts, newVertex]);

      // Add the new node to the flow
      const newNode: FlowNode = {
        id: nodeId,
        type: "custom",
        position: nodePosition,
        data: {
          label: nodeDefinition.label,
          nodeType: nodeType,
          // config: {}, //nodeDefinition,
          originalId: tempId,
          category: nodeDefinition.category,
          inputs: nodeDefinition.inputs,
          outputs: nodeDefinition.outputs,
        },
      };

      setNodes((nds) => [...nds, newNode]);
    },
    [] // Empty deps - only uses state setters which are stable
  );

  const handleDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();

      const nodeType = event.dataTransfer.getData("application/reactflow");

      if (!nodeType || !reactFlowInstance || !reactFlowWrapper.current) {
        return;
      }

      // Get the position relative to the ReactFlow viewport
      const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect();
      const position = reactFlowInstance.project({
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      });

      handleAddNode(nodeType, position);
    },
    [reactFlowInstance, handleAddNode]
  );

  const handleDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
  }, []);

  const handleSaveWorkflow = useCallback(async () => {
    if (!workflow) return;

    try {
      setSaving(true);

      // Convert React Flow nodes to vertices
      const vertices = nodes.map((node) => {
        // Remove label and position from config to avoid duplicates
        let cleanConfig = {};
        const nodeConfig = (node as any).node_config;

        if (nodeConfig === undefined || nodeConfig === null) {
          // If node_config is not set, use data.config
          cleanConfig = node.data.config || {};
        } else {
          // Destructure and remove label, position, config fields
          const { label, position, config, ...rest } = nodeConfig;
          cleanConfig = rest;
        }

        return {
          id: node.data.originalId, // Include the original ID for backend mapping
          type: node.data.nodeType,
          properties: {
            label: node.data.label,
            position: {
              x: Math.round(node.position.x),
              y: Math.round(node.position.y),
            },
            config: { ...cleanConfig }, // Spread the rest of config without label and position
          },
        };
      });

      // Convert React Flow edges to workflow edges
      const workflowEdges = edges.map((edge) => {
        // Find the actual node IDs (handle temp IDs)
        const sourceNode = nodes.find((n) => n.id === edge.source);
        const targetNode = nodes.find((n) => n.id === edge.target);

        // Use originalId if available, otherwise parse the ID
        const sourceId = sourceNode?.data.originalId ?? parseInt(edge.source);
        const targetId = targetNode?.data.originalId ?? parseInt(edge.target);

        // Get source config without mutating original
        const sourceNodeConfig = (sourceNode as any)?.node_config || {};
        const { config: sourceConfigToRemove, ...src_config } =
          sourceNodeConfig;

        // Get target config without mutating original
        const targetNodeConfig = (targetNode as any)?.node_config || {};
        const { config: targetConfigToRemove, ...tg_config } = targetNodeConfig;

        let source_props = {
          name: edge.sourceHandle,
          config: src_config,
        };

        let target_props = {
          name: edge.targetHandle,
          config: tg_config,
        };

        return {
          source_id: sourceId,
          target_id: targetId,
          type: "default",
          source_properties: source_props,
          target_properties: target_props,
        };
      });

      await workflowApi.updateWorkflow(workflow.id, {
        name: workflow.name,
        description: workflow.description,
        vertices,
        edges: workflowEdges,
      });

      // Reload workflow data to get updated IDs
      await loadWorkflowData();
    } catch (error) {
      console.error("Failed to save workflow:", error);
    } finally {
      setSaving(false);
    }
  }, [workflow, nodes, edges, loadWorkflowData]);

  // WorkflowEditor.tsx에 추가할 수 있는 헬퍼 함수
  const identifyStartNodes = () => {
    // 방법 1: 타입으로 찾기
    const startNodesByType = nodes.filter(
      (node) => node.data.nodeType === "chat_input"
    );

    // 방법 2: 입력 엣지가 없는 노드 찾기
    const targetNodeIds = new Set(edges.map((edge) => edge.target));
    const startNodesByEdges = nodes.filter(
      (node) => !targetNodeIds.has(node.id)
    );

    // 방법 3: inputs 배열이 비어있는 노드 찾기
    const startNodesByInputs = nodes.filter((node) => {
      const nodeDefinition = NODE_TYPES.find(
        (n) => n.type === node.data.nodeType
      );
      return nodeDefinition?.inputs.length === 0;
    });

    return startNodesByType; // 가장 명확한 방법 사용
  };

  if (loading) {
    return (
      <Box
        sx={{
          flex: 1,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <ReactFlowProvider>
      <Box sx={{ display: "flex", height: "100vh" }}>
        <NodePalette onAddNode={handleAddNode} nodeTypes={NODE_TYPES} />
        <Box sx={{ flex: 1, display: "flex", flexDirection: "column" }}>
          <WorkflowToolbar
            workflow={workflow}
            onRefresh={loadWorkflowData}
            onSave={handleSaveWorkflow}
            isSaving={saving}
          />
          <Box
            ref={reactFlowWrapper}
            sx={{ flex: 1 }}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
          >
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={handleNodesChange}
              onEdgesChange={handleEdgesChange}
              onConnect={onConnect}
              onNodeClick={onNodeClick}
              onPaneClick={onPaneClick}
              onInit={setReactFlowInstance}
              nodeTypes={nodeTypes}
              fitView
              deleteKeyCode={["Delete", "Backspace"]}
              multiSelectionKeyCode={null}
              nodesDraggable={true}
              nodesConnectable={true}
              elementsSelectable={true}
              zoomOnScroll={true}
              panOnScroll={false}
              zoomOnDoubleClick={false}
              selectNodesOnDrag={false}
              // Performance optimizations
              elevateNodesOnSelect={false}
              elevateEdgesOnSelect={false}
              autoPanOnConnect={false}
              autoPanOnNodeDrag={false}
              panActivationKeyCode={null}
            >
              <Controls />
              <MiniMap />
              <Background variant={BackgroundVariant.Dots} gap={12} size={1} />
            </ReactFlow>
          </Box>
        </Box>

        <NodePanel
          selectedNode={selectedNode}
          onNodeUpdate={handleNodeUpdate}
          onNodeDelete={handleNodeDelete}
          onClose={() => setSelectedNode(null)}
        />
      </Box>
    </ReactFlowProvider>
  );
};

export default WorkflowEditor;

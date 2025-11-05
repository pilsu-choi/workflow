import React, { useCallback, useRef, useState } from "react";
import {
  ReactFlow,
  addEdge,
  Background,
  Controls,
  MiniMap,
  NodeToolbar,
  ReactFlowProvider,
  useEdgesState,
  useNodesState,
  MarkerType,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

// Default node types (you can replace these with custom nodes)

type NodeItem = {
  id: string;
  type?: string;
  data: { label: string };
  position: { x: number; y: number };
};

export default function WorkflowEditor(): JSX.Element {
  const reactFlowWrapper = useRef<HTMLDivElement | null>(null);
  const [nodes, setNodes, onNodesChange] = useNodesState<NodeItem>([
    {
      id: "1",
      data: { label: "Start" },
      position: { x: 0, y: 50 },
    },
    {
      id: "2",
      data: { label: "End" },
      position: { x: 300, y: 50 },
    },
  ]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedNode, setSelectedNode] = useState<NodeItem | null>(null);

  const nodeTypes = {};

  const onConnect = useCallback(
    (params) =>
      setEdges((eds) =>
        addEdge({ ...params, markerEnd: { type: MarkerType.Arrow } }, eds)
      ),
    [setEdges]
  );

  // toolbar actions
  const handleFitView = useCallback((instance) => instance.fitView(), []);

  // add node from sidebar (simple click-based)
  const addNodeFromSidebar = (type: string) => {
    const id = String(Date.now());
    const newNode: NodeItem = {
      id,
      type: undefined,
      data: { label: type },
      position: { x: Math.random() * 400 + 50, y: Math.random() * 200 + 50 },
    };
    setNodes((nds) => nds.concat(newNode));
  };

  const onNodeClick = (_event, node) => {
    setSelectedNode(node as NodeItem);
  };

  const updateSelectedNodeLabel = (label: string) => {
    if (!selectedNode) return;
    setNodes((nds) =>
      nds.map((n) =>
        n.id === selectedNode.id ? { ...n, data: { ...n.data, label } } : n
      )
    );
    setSelectedNode((s) => (s ? { ...s, data: { ...s.data, label } } : s));
  };

  // save / load
  const exportToJson = () => {
    const dataStr = JSON.stringify({ nodes, edges }, null, 2);
    const blob = new Blob([dataStr], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "workflow.json";
    a.click();
    URL.revokeObjectURL(a.href);
  };

  const importFromJson = (file: File | null) => {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (evt) => {
      try {
        const parsed = JSON.parse(String(evt.target?.result));
        if (parsed.nodes && parsed.edges) {
          setNodes(parsed.nodes);
          setEdges(parsed.edges);
          setSelectedNode(null);
        } else {
          alert("Invalid workflow JSON");
        }
      } catch (e) {
        alert("Failed to parse JSON: " + e);
      }
    };
    reader.readAsText(file);
  };

  // quick localStorage save / load
  const saveToLocal = () => {
    localStorage.setItem("workflow", JSON.stringify({ nodes, edges }));
    alert("Saved to localStorage");
  };
  const loadFromLocal = () => {
    const raw = localStorage.getItem("workflow");
    if (!raw) return alert("No saved workflow in localStorage");
    try {
      const parsed = JSON.parse(raw);
      setNodes(parsed.nodes || []);
      setEdges(parsed.edges || []);
      setSelectedNode(null);
    } catch (e) {
      alert("Invalid saved data");
    }
  };

  const clearAll = () => {
    if (!confirm("정말로 모든 노드와 엣지를 삭제하시겠습니까?")) return;
    setNodes([]);
    setEdges([]);
    setSelectedNode(null);
  };

  return (
    <div className="h-screen flex bg-gray-50">
      {/* Left sidebar: node library */}
      <aside className="w-56 border-r p-3 bg-white">
        <h3 className="text-lg font-semibold mb-3">Nodes</h3>
        <div className="space-y-2">
          {["Start", "Action", "Decision", "End"].map((t) => (
            <button
              key={t}
              onClick={() => addNodeFromSidebar(t)}
              className="w-full text-left p-2 rounded shadow-sm hover:shadow-md bg-white"
            >
              {t}
            </button>
          ))}
        </div>

        <div className="mt-6">
          <h4 className="font-medium mb-2">File</h4>
          <div className="flex flex-col gap-2">
            <button
              onClick={exportToJson}
              className="p-2 rounded bg-blue-600 text-white"
            >
              Export JSON
            </button>
            <label className="p-2 rounded bg-gray-100 text-sm cursor-pointer text-center">
              Import JSON
              <input
                type="file"
                accept="application/json"
                onChange={(e) => importFromJson(e.target.files?.[0] ?? null)}
                className="hidden"
              />
            </label>
            <button
              onClick={saveToLocal}
              className="p-2 rounded bg-green-600 text-white"
            >
              Save (local)
            </button>
            <button
              onClick={loadFromLocal}
              className="p-2 rounded bg-yellow-500 text-white"
            >
              Load (local)
            </button>
            <button
              onClick={clearAll}
              className="p-2 rounded bg-red-600 text-white"
            >
              Clear
            </button>
          </div>
        </div>
      </aside>

      {/* Canvas */}
      <div ref={reactFlowWrapper} className="flex-1 relative">
        <ReactFlowProvider>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onNodeClick={onNodeClick}
            fitView
            nodeTypes={nodeTypes}
            style={{ width: "100%", height: "100%" }}
          >
            <Controls />
            <MiniMap />
            <Background />
          </ReactFlow>
        </ReactFlowProvider>

        {/* Top toolbar */}
        <div className="absolute left-1/2 -translate-x-1/2 top-3 z-10 bg-white/80 backdrop-blur rounded shadow p-2 flex gap-2">
          <button
            onClick={() => {
              // find reactflow instance and fit view
              const rf = (document.querySelector(".react-flow") as any)
                ?.__reactFlowInstance;
              if (rf) rf.fitView();
            }}
            className="px-3 py-1 rounded border"
          >
            Fit view
          </button>
          <button onClick={exportToJson} className="px-3 py-1 rounded border">
            Export
          </button>
          <button onClick={saveToLocal} className="px-3 py-1 rounded border">
            Save
          </button>
        </div>
      </div>

      {/* Right sidebar: properties */}
      <aside className="w-64 border-l p-4 bg-white">
        <h3 className="text-lg font-semibold mb-3">Properties</h3>
        {selectedNode ? (
          <div className="space-y-3">
            <div>
              <label className="text-sm block mb-1">Node ID</label>
              <div className="text-xs text-gray-600">{selectedNode.id}</div>
            </div>
            <div>
              <label className="text-sm block mb-1">Label</label>
              <input
                value={String(selectedNode.data?.label ?? "")}
                onChange={(e) => updateSelectedNodeLabel(e.target.value)}
                className="w-full p-2 border rounded"
              />
            </div>
            <div>
              <label className="text-sm block mb-1">Position</label>
              <div className="text-xs text-gray-600">
                x: {Math.round(selectedNode.position.x)}, y:{" "}
                {Math.round(selectedNode.position.y)}
              </div>
            </div>
          </div>
        ) : (
          <div className="text-sm text-gray-600">
            노드를 선택하면 속성이 표시됩니다.
          </div>
        )}

        <div className="mt-6">
          <h4 className="font-medium mb-2">Help</h4>
          <ul className="text-sm text-gray-600 list-disc pl-4 space-y-1">
            <li>왼쪽의 노드 버튼을 눌러 캔버스에 노드를 추가합니다.</li>
            <li>노드를 드래그하여 위치 변경, 노드를 클릭해 속성 편집.</li>
            <li>노드들 사이를 연결하려면 노드의 포인트에서 끌어 연결하세요.</li>
          </ul>
        </div>
      </aside>
    </div>
  );
}

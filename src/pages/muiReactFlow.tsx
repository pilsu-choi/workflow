import React, { useCallback, useRef } from "react";
import {
  Background,
  ReactFlow,
  useNodesState,
  useEdgesState,
  addEdge,
  useReactFlow,
  ReactFlowProvider,
  BackgroundVariant,
} from "@xyflow/react";
import {
  Box,
  Paper,
  Typography,
  AppBar,
  Toolbar,
  Container,
  Chip,
  Stack,
} from "@mui/material";
import {
  AccountTree as AccountTreeIcon,
  Info as InfoIcon,
} from "@mui/icons-material";

import "@xyflow/react/dist/style.css";

const initialNodes = [
  {
    id: "0",
    type: "input",
    data: { label: "Node" },
    position: { x: 0, y: 50 },
  },
];

let id = 1;
const getId = () => `${id++}`;
const nodeOrigin: [number, number] = [0.5, 0];

const MuiReactFlow = () => {
  const reactFlowWrapper = useRef<HTMLDivElement>(null);

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const { screenToFlowPosition } = useReactFlow();

  const onConnect = useCallback(
    (params: any) => setEdges((eds) => addEdge(params, eds)),
    []
  );

  const onConnectEnd = useCallback(
    (event: any, connectionState: any) => {
      // when a connection is dropped on the pane it's not valid
      if (!connectionState.isValid) {
        const newId = getId();
        const { clientX, clientY } =
          "changedTouches" in event ? event.changedTouches[0] : event;
        const newNode = {
          id: newId,
          position: screenToFlowPosition({
            x: clientX,
            y: clientY,
          }),
          data: { label: `Node ${newId}` },
          origin: [0.5, 0.0] as [number, number],
        };

        setNodes((nds) => nds.concat(newNode));
        setEdges((eds) =>
          eds.concat({
            id: newId,
            source: connectionState.fromNode.id,
            target: newId,
          })
        );
      }
    },
    [screenToFlowPosition, setNodes, setEdges]
  );

  return (
    <Box sx={{ display: "flex", flexDirection: "column", height: "100vh" }}>
      {/* AppBar */}
      <AppBar position="static" elevation={2}>
        <Toolbar>
          <AccountTreeIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            MUI React Flow Editor
          </Typography>
          <Stack direction="row" spacing={1}>
            <Chip
              icon={<InfoIcon />}
              label={`${nodes.length} Nodes`}
              color="primary"
              variant="outlined"
              sx={{ color: "white", borderColor: "white" }}
            />
            <Chip
              label={`${edges.length} Edges`}
              color="primary"
              variant="outlined"
              sx={{ color: "white", borderColor: "white" }}
            />
          </Stack>
        </Toolbar>
      </AppBar>

      {/* Main Content */}
      <Box sx={{ flexGrow: 1, position: "relative", overflow: "hidden" }}>
        <Paper
          elevation={0}
          sx={{
            width: "100%",
            height: "100%",
            borderRadius: 0,
          }}
        >
          <Box
            ref={reactFlowWrapper}
            sx={{
              width: "100%",
              height: "100%",
            }}
          >
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onConnect={onConnect}
              onConnectEnd={onConnectEnd}
              fitView
              fitViewOptions={{ padding: 2 }}
              nodeOrigin={nodeOrigin}
              style={{
                background: "#fafafa",
              }}
            >
              <Background
                variant={BackgroundVariant.Dots}
                gap={12}
                size={1}
                color="#e0e0e0"
              />
            </ReactFlow>
          </Box>
        </Paper>
      </Box>

      {/* Footer Info */}
      <Box
        sx={{
          position: "absolute",
          bottom: 16,
          left: 16,
          zIndex: 5,
        }}
      >
        <Paper
          elevation={3}
          sx={{
            p: 2,
            backgroundColor: "rgba(255, 255, 255, 0.95)",
          }}
        >
          <Typography variant="body2" color="text.secondary">
            <strong>Tip:</strong> Drag from a node handle and drop on the canvas
            to create a new connected node
          </Typography>
        </Paper>
      </Box>
    </Box>
  );
};

export default () => (
  <ReactFlowProvider>
    <MuiReactFlow />
  </ReactFlowProvider>
);

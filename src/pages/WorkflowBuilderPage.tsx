import React, { useState } from "react";
import {
  Box,
  Button,
  IconButton,
  AppBar,
  Toolbar,
  Typography,
} from "@mui/material";
import {
  ArrowBack as ArrowBackIcon,
  Home as HomeIcon,
} from "@mui/icons-material";
import WorkflowEditor from "../components/domain/workflow_builder/WorkflowEditor";
import NodePalette from "../components/domain/workflow_builder/NodePalette";

interface WorkflowBuilderPageProps {
  workflowId: number;
  onGoBack: () => void;
  onGoHome: () => void;
}

const WorkflowBuilderPage: React.FC<WorkflowBuilderPageProps> = ({
  workflowId,
  onGoBack,
  onGoHome,
}) => {
  const [showNodePalette] = useState(false);

  const handleAddNode = (nodeType: string) => {
    // This will be handled by WorkflowEditor component
    console.log("Add node:", nodeType);
  };

  return (
    <Box sx={{ display: "flex", flexDirection: "column", height: "100vh" }}>
      {/* Top Navigation Bar */}
      <AppBar position="static" elevation={1}>
        <Toolbar>
          <IconButton
            edge="start"
            color="inherit"
            onClick={onGoBack}
            sx={{ mr: 2 }}
          >
            <ArrowBackIcon />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Workflow Builder
          </Typography>
          <Button color="inherit" startIcon={<HomeIcon />} onClick={onGoHome}>
            Home
          </Button>
        </Toolbar>
      </AppBar>

      {/* Main Content Area */}
      <Box sx={{ display: "flex", flex: 1, overflow: "hidden" }}>
        <Box sx={{ flex: 1 }}>
          <WorkflowEditor workflowId={workflowId} />
        </Box>
      </Box>
    </Box>
  );
};

export default WorkflowBuilderPage;

import React, { useState, useCallback } from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Chip,
  IconButton,
  LinearProgress,
} from "@mui/material";
import {
  Refresh as RefreshIcon,
  PlayArrow as PlayIcon,
  Stop as StopIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  Chat as ChatIcon,
  History as HistoryIcon,
  Save as SaveIcon,
} from "@mui/icons-material";
import type { Graph, WorkflowExecuteRequest } from "../../../types/workflow";
import { workflowApi } from "../../../services/workflow/api";
import ChatModal from "./modals/ChatModal";
import LogModal from "./modals/LogModal";

interface WorkflowToolbarProps {
  workflow: Graph | null;
  onRefresh: () => void;
  onSave: () => Promise<void>;
  isSaving: boolean;
}

const WorkflowToolbar: React.FC<WorkflowToolbarProps> = ({
  workflow,
  onRefresh,
  onSave,
  isSaving,
}) => {
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionStatus, setExecutionStatus] = useState<string | null>(null);
  const [chatModalOpen, setChatModalOpen] = useState(false);
  const [logModalOpen, setLogModalOpen] = useState(false);

  const handleExecute = useCallback(async () => {
    if (!workflow) return;

    try {
      setIsExecuting(true);
      setExecutionStatus("Executing...");

      let test_body: WorkflowExecuteRequest = {
        initial_inputs: {
          prompt: "What is the capital of France?",
          model: "gpt-4.1",
        },
      };

      const response = await workflowApi.executeWorkflow(
        workflow.id,
        test_body
      );

      if (response.data.success) {
        setExecutionStatus(
          `Execution ${response.data.result ? "completed" : "started"}`
        );

        // Poll for execution status
        const pollStatus = async () => {
          try {
            const statusResponse = await workflowApi.getWorkflowStatus(
              workflow.id
            );
            const status = statusResponse.data.status;

            if (
              status === "completed" ||
              status === "failed" ||
              status === "cancelled"
            ) {
              setExecutionStatus(`Execution ${status}`);
              setIsExecuting(false);
            } else {
              setTimeout(pollStatus, 1000);
            }
          } catch (error) {
            console.error("Failed to poll execution status:", error);
            setExecutionStatus("Failed to get execution status");
            setIsExecuting(false);
          }
        };

        setTimeout(pollStatus, 1000);
      } else {
        setExecutionStatus("Execution failed");
        setIsExecuting(false);
      }
    } catch (error) {
      console.error("Failed to execute workflow:", error);
      setExecutionStatus("Failed to execute workflow");
      setIsExecuting(false);
    }
  }, [workflow]);

  const handleCancel = useCallback(async () => {
    // Implementation for canceling execution
    setExecutionStatus(null);
    setIsExecuting(false);
  }, []);

  const handleOpenChat = useCallback(() => {
    setChatModalOpen(true);
  }, []);

  const handleCloseChat = useCallback(() => {
    setChatModalOpen(false);
  }, []);

  const handleOpenLog = useCallback(() => {
    setLogModalOpen(true);
  }, []);

  const handleCloseLog = useCallback(() => {
    setLogModalOpen(false);
  }, []);

  const getStatusColor = useCallback((status: string) => {
    switch (status) {
      case "completed":
        return "success";
      case "failed":
        return "error";
      case "cancelled":
        return "default";
      default:
        return "info";
    }
  }, []);

  const getStatusIcon = useCallback((status: string) => {
    switch (status) {
      case "completed":
        return <CheckIcon />;
      case "failed":
        return <ErrorIcon />;
      default:
        return undefined;
    }
  }, []);

  if (!workflow) return null;

  return (
    <AppBar position="static" color="default" elevation={1}>
      <Toolbar>
        <Box sx={{ flexGrow: 1 }}>
          <Typography variant="h6" component="div" sx={{ mr: 2 }}>
            {workflow.name}
          </Typography>
          {workflow.description && (
            <Typography
              variant="body2"
              color="text.secondary"
              title={workflow.description}
            >
              {workflow.description.length > 20
                ? `${workflow.description.substring(0, 20)}...`
                : workflow.description}
            </Typography>
          )}
        </Box>

        <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
          {executionStatus && (
            <Chip
              icon={getStatusIcon(executionStatus)}
              label={`Status: ${executionStatus}`}
              color={getStatusColor(executionStatus)}
              variant="outlined"
            />
          )}

          <IconButton onClick={onRefresh} color="inherit">
            <RefreshIcon />
          </IconButton>

          <Button
            variant="contained"
            color="success"
            startIcon={<SaveIcon />}
            onClick={onSave}
            disabled={isSaving}
            sx={{ mr: 1 }}
          >
            {isSaving ? "Saving..." : "Save"}
          </Button>

          <Button
            variant="contained"
            color="secondary"
            startIcon={<ChatIcon />}
            onClick={handleOpenChat}
            sx={{ mr: 1 }}
          >
            Chat
          </Button>

          <Button
            variant="contained"
            color="info"
            startIcon={<HistoryIcon />}
            onClick={handleOpenLog}
            sx={{ mr: 1 }}
          >
            Log
          </Button>

          {isExecuting ? (
            <Button
              variant="contained"
              color="error"
              startIcon={<StopIcon />}
              onClick={handleCancel}
            >
              Cancel
            </Button>
          ) : (
            <Button
              variant="contained"
              color="primary"
              startIcon={<PlayIcon />}
              onClick={handleExecute}
            >
              Execute
            </Button>
          )}
        </Box>
      </Toolbar>
      {isExecuting && <LinearProgress />}
      <ChatModal
        open={chatModalOpen}
        onClose={handleCloseChat}
        workflowId={workflow.id}
        workflowName={workflow.name}
      />
      <LogModal
        open={logModalOpen}
        onClose={handleCloseLog}
        workflowId={workflow.id}
        workflowName={workflow.name}
      />
    </AppBar>
  );
};

// Wrap with React.memo to prevent unnecessary re-renders when parent re-renders
export default React.memo(WorkflowToolbar);

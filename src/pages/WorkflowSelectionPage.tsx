import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  CardActions,
  TextField,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
  Paper,
  Container,
  Grid,
} from "@mui/material";
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
} from "@mui/icons-material";
import type { Graph } from "../types/workflow";
import type { AxiosError } from "axios";
import { workflowApi } from "../services/workflow/api";

interface WorkflowSelectionPageProps {
  onSelectWorkflow: (workflowId: number) => void;
  onGoHome: () => void;
}

const WorkflowSelectionPage: React.FC<WorkflowSelectionPageProps> = ({
  onSelectWorkflow,
}) => {
  const [workflows, setWorkflows] = useState<Graph[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newWorkflow, setNewWorkflow] = useState({
    name: "",
    description: "",
  });

  useEffect(() => {
    loadWorkflows();
  }, []);

  const loadWorkflows = async () => {
    try {
      setLoading(true);
      const response = await workflowApi.getWorkflows();
      setWorkflows(response.data);
    } catch (error) {
      console.error("Failed to load workflows:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateWorkflow = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await workflowApi.createWorkflow({
        name: newWorkflow.name,
        description: newWorkflow.description,
        vertices: [],
        edges: [],
      });
      if (response.data.success) {
        // Reload workflows to get the newly created one
        await loadWorkflows();
        setNewWorkflow({ name: "", description: "" });
        setShowCreateForm(false);
        onSelectWorkflow(response.data.graph_id);
      }
    } catch (error) {
      console.error("Failed to create workflow:", error);
    }
  };

  const handleDeleteWorkflow = async (workflowId: number) => {
    const workflow = workflows.find((w) => w.id === workflowId);
    const workflowName = workflow?.name || `ID: ${workflowId}`;

    if (
      window.confirm(
        `Are you sure you want to delete workflow "${workflowName}"?`
      )
    ) {
      try {
        console.log(
          `Attempting to delete workflow: ${workflowName} (ID: ${workflowId})`
        );
        const response = await workflowApi.deleteWorkflow(workflowId);
        console.log("Delete response:", response);

        setWorkflows((prev) => prev.filter((w) => w.id !== workflowId));
        console.log(`Workflow "${workflowName}" deleted successfully`);
      } catch (error) {
        console.error("Failed to delete workflow:", error);
        const axiosError = error as AxiosError;
        console.error(
          "Error details:",
          axiosError.response?.data || axiosError.message
        );
        alert(
          `Failed to delete workflow "${workflowName}". Please check the console for details.`
        );
      }
    }
  };

  if (loading) {
    return (
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          height: "100vh",
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            mb: 2,
          }}
        >
          <Typography variant="h4" component="h1">
            Workflow Selection
          </Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setShowCreateForm(true)}
            size="large"
          >
            Create New Workflow
          </Button>
        </Box>
        <Typography variant="body1" color="text.secondary">
          Select a workflow to edit or create a new one to get started.
        </Typography>
      </Box>

      {workflows.length === 0 ? (
        <Paper
          elevation={1}
          sx={{
            p: 6,
            textAlign: "center",
            bgcolor: "background.paper",
          }}
        >
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No workflows found
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Create your first workflow to get started with automation.
          </Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setShowCreateForm(true)}
          >
            Create Your First Workflow
          </Button>
        </Paper>
      ) : (
        <Grid container spacing={3}>
          {workflows.map((workflow) => (
            <Grid size={{ xs: 12, sm: 6, md: 4 }} key={workflow.id}>
              <Card
                sx={{
                  height: "100%",
                  display: "flex",
                  flexDirection: "column",
                  cursor: "pointer",
                  transition: "all 0.2s ease-in-out",
                  "&:hover": {
                    boxShadow: 4,
                    transform: "translateY(-2px)",
                  },
                }}
                onClick={() => onSelectWorkflow(workflow.id)}
              >
                <CardContent sx={{ flexGrow: 1 }}>
                  <Box
                    sx={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "flex-start",
                      mb: 2,
                    }}
                  >
                    <Typography variant="h6" component="h3" gutterBottom>
                      {workflow.name}
                    </Typography>
                  </Box>

                  {workflow.description && (
                    <Typography
                      variant="body2"
                      color="text.secondary"
                      sx={{ mb: 2 }}
                      title={workflow.description}
                    >
                      {workflow.description.length > 100
                        ? `${workflow.description.substring(0, 100)}...`
                        : workflow.description}
                    </Typography>
                  )}

                  {workflow.created_at && (
                    <Typography variant="caption" color="text.secondary">
                      Created:{" "}
                      {new Date(workflow.created_at).toLocaleDateString()}
                    </Typography>
                  )}
                </CardContent>

                <CardActions
                  sx={{ justifyContent: "space-between", px: 2, pb: 2 }}
                >
                  <Button
                    size="small"
                    startIcon={<EditIcon />}
                    onClick={(e) => {
                      e.stopPropagation();
                      onSelectWorkflow(workflow.id);
                    }}
                  >
                    Edit
                  </Button>
                  <IconButton
                    size="small"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteWorkflow(workflow.id);
                    }}
                    color="error"
                  >
                    <DeleteIcon />
                  </IconButton>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      <Dialog
        open={showCreateForm}
        onClose={() => setShowCreateForm(false)}
        maxWidth="sm"
        fullWidth
      >
        <form onSubmit={handleCreateWorkflow}>
          <DialogTitle>Create New Workflow</DialogTitle>
          <DialogContent>
            <TextField
              autoFocus
              margin="dense"
              label="Workflow Name"
              fullWidth
              variant="outlined"
              value={newWorkflow.name}
              onChange={(e) =>
                setNewWorkflow((prev) => ({ ...prev, name: e.target.value }))
              }
              required
              sx={{ mb: 2 }}
            />
            <TextField
              margin="dense"
              label="Description"
              fullWidth
              multiline
              rows={3}
              variant="outlined"
              value={newWorkflow.description}
              onChange={(e) =>
                setNewWorkflow((prev) => ({
                  ...prev,
                  description: e.target.value,
                }))
              }
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setShowCreateForm(false)}>Cancel</Button>
            <Button type="submit" variant="contained">
              Create
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Container>
  );
};

export default WorkflowSelectionPage;

import React from "react";
import {
  Box,
  Typography,
  Paper,
  Button,
  Container,
  Grid,
  Card,
  CardContent,
} from "@mui/material";
import {
  PlayArrow as PlayIcon,
  Add as AddIcon,
  Settings as SettingsIcon,
} from "@mui/icons-material";

interface HomePageProps {
  onSelectWorkflows: () => void;
}

const HomePage: React.FC<HomePageProps> = ({ onSelectWorkflows }) => {
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ textAlign: "center", mb: 6 }}>
        <Typography
          variant="h3"
          component="h1"
          gutterBottom
          sx={{ fontWeight: "bold", color: "primary.main" }}
        >
          Workflow Automation Engine
        </Typography>
        <Typography
          variant="h6"
          component="p"
          color="text.secondary"
          sx={{ maxWidth: 600, mx: "auto", mb: 4 }}
        >
          Create, manage, and execute automated workflows with our powerful
          visual workflow builder.
        </Typography>
        <Button
          variant="contained"
          size="large"
          startIcon={<PlayIcon />}
          onClick={onSelectWorkflows}
          sx={{ px: 4, py: 1.5 }}
        >
          Get Started
        </Button>
      </Box>

      <Grid container spacing={4}>
        <Grid item xs={12} md={4}>
          <Card
            sx={{
              height: "100%",
              textAlign: "center",
              p: 3,
              transition: "transform 0.2s ease-in-out",
              "&:hover": {
                transform: "translateY(-4px)",
                boxShadow: 4,
              },
            }}
          >
            <CardContent>
              <Box
                sx={{
                  width: 64,
                  height: 64,
                  borderRadius: "50%",
                  bgcolor: "primary.light",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  mx: "auto",
                  mb: 2,
                }}
              >
                <AddIcon sx={{ fontSize: 32, color: "primary.contrastText" }} />
              </Box>
              <Typography variant="h6" gutterBottom>
                Create Workflows
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Design custom automation workflows using our intuitive visual
                builder with drag-and-drop functionality.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card
            sx={{
              height: "100%",
              textAlign: "center",
              p: 3,
              transition: "transform 0.2s ease-in-out",
              "&:hover": {
                transform: "translateY(-4px)",
                boxShadow: 4,
              },
            }}
          >
            <CardContent>
              <Box
                sx={{
                  width: 64,
                  height: 64,
                  borderRadius: "50%",
                  bgcolor: "secondary.light",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  mx: "auto",
                  mb: 2,
                }}
              >
                <PlayIcon
                  sx={{ fontSize: 32, color: "secondary.contrastText" }}
                />
              </Box>
              <Typography variant="h6" gutterBottom>
                Execute & Monitor
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Run your workflows and monitor their execution in real-time with
                detailed logs and status tracking.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card
            sx={{
              height: "100%",
              textAlign: "center",
              p: 3,
              transition: "transform 0.2s ease-in-out",
              "&:hover": {
                transform: "translateY(-4px)",
                boxShadow: 4,
              },
            }}
          >
            <CardContent>
              <Box
                sx={{
                  width: 64,
                  height: 64,
                  borderRadius: "50%",
                  bgcolor: "success.light",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  mx: "auto",
                  mb: 2,
                }}
              >
                <SettingsIcon
                  sx={{ fontSize: 32, color: "success.contrastText" }}
                />
              </Box>
              <Typography variant="h6" gutterBottom>
                Manage & Configure
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Organize your workflows, configure settings, and manage
                permissions with our comprehensive management tools.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default HomePage;

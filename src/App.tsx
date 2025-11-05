import React, { useState } from "react";
import { Box } from "@mui/material";
import HomePage from "./pages/HomePage";
import WorkflowSelectionPage from "./pages/WorkflowSelectionPage";
import WorkflowBuilderPage from "./pages/WorkflowBuilderPage";
import SimpleReactFlow from "./pages/simpleReactFlow";
type AppPage = "home" | "selection" | "builder" | "simpleReactFlow";

function App() {
  const [currentPage, setCurrentPage] = useState<AppPage>("home");
  const [selectedWorkflowId, setSelectedWorkflowId] = useState<number | null>(
    null
  );

  const handleGoToSelection = () => {
    setCurrentPage("selection");
  };

  const handleSelectWorkflow = (workflowId: number) => {
    setSelectedWorkflowId(workflowId);
    setCurrentPage("builder");
  };

  const handleGoBack = () => {
    setCurrentPage("selection");
  };

  const handleGoHome = () => {
    setCurrentPage("home");
    setSelectedWorkflowId(null);
  };

  const renderCurrentPage = () => {
    switch (currentPage) {
      case "home":
        return <HomePage onSelectWorkflows={handleGoToSelection} />;
      case "selection":
        return (
          <WorkflowSelectionPage
            onSelectWorkflow={handleSelectWorkflow}
            onGoHome={handleGoHome}
          />
        );
      case "builder":
        return selectedWorkflowId ? (
          <WorkflowBuilderPage
            workflowId={selectedWorkflowId}
            onGoBack={handleGoBack}
            onGoHome={handleGoHome}
          />
        ) : null;
      case "simpleReactFlow":
        return <SimpleReactFlow />;
      default:
        return <HomePage onSelectWorkflows={handleGoToSelection} />;
    }
  };

  return (
    <Box sx={{ height: "100vh", overflow: "hidden" }}>
      {renderCurrentPage()}
    </Box>
  );
}

export default App;

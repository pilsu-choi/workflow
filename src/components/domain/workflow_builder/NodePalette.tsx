import React, { useState, useMemo } from "react";
import {
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  CardActionArea,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  TextField,
  InputAdornment,
} from "@mui/material";
import {
  ExpandMore as ExpandMoreIcon,
  Search as SearchIcon,
  Webhook as WebhookIcon,
  Schedule as ScheduleIcon,
  PlayArrow as PlayArrowIcon,
  SmartToy as SmartToyIcon,
  Psychology as PsychologyIcon,
  Storage as StorageIcon,
  AccountTree as AccountTreeIcon,
  TableChart as TableChartIcon,
  Code as CodeIcon,
  FilterList as FilterListIcon,
  BarChart as BarChartIcon,
  Http as HttpIcon,
  Email as EmailIcon,
  Message as MessageIcon,
  HelpOutline as ConditionIcon,
  CallMerge as CallMergeIcon,
  CallSplit as CallSplitIcon,
  Description as LogIcon,
  Edit as EditIcon,
  Visibility as VisibilityIcon,
  Save as SaveIcon,
  Reply as ReplyIcon,
  Loop as LoopIcon,
  Transform as TransformIcon,
} from "@mui/icons-material";
import { NODE_TYPES, NODE_CATEGORIES } from "../../../types/workflow";

interface NodePaletteProps {
  onAddNode: (nodeType: string) => void;
}

// Icon mapping
const iconMap: { [key: string]: React.ReactElement } = {
  Webhook: <WebhookIcon />,
  Schedule: <ScheduleIcon />,
  PlayArrow: <PlayArrowIcon />,
  SmartToy: <SmartToyIcon />,
  Psychology: <PsychologyIcon />,
  Storage: <StorageIcon />,
  AccountTree: <AccountTreeIcon />,
  TableChart: <TableChartIcon />,
  Code: <CodeIcon />,
  FilterList: <FilterListIcon />,
  BarChart: <BarChartIcon />,
  Http: <HttpIcon />,
  Email: <EmailIcon />,
  Message: <MessageIcon />,
  HelpOutline: <ConditionIcon />,
  CallMerge: <CallMergeIcon />,
  // CallSplit: <CallSplitIcon />,
  Description: <LogIcon />,
  Edit: <EditIcon />,
  Visibility: <VisibilityIcon />,
  Save: <SaveIcon />,
  Reply: <ReplyIcon />,
  Loop: <LoopIcon />,
  Transform: <TransformIcon />,
  Condition: <CallSplitIcon />,
  Input: <EditIcon />,
};

// Category labels
const categoryLabels: { [key: string]: string } = {
  [NODE_CATEGORIES.AI_ML]: "AI/ML",
  [NODE_CATEGORIES.DATA_PROCESSING]: "Data Processing",
  [NODE_CATEGORIES.LOGIC]: "Logic",
  [NODE_CATEGORIES.INPUT_OUTPUT]: "Input/Output",
};

const NodePalette: React.FC<NodePaletteProps> = ({ onAddNode }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [expandedCategories, setExpandedCategories] = useState<string[]>([
    NODE_CATEGORIES.AI_ML,
    NODE_CATEGORIES.DATA_PROCESSING,
    NODE_CATEGORIES.LOGIC,
    NODE_CATEGORIES.INPUT_OUTPUT,
  ]);

  const handleDragStart = (event: React.DragEvent, nodeType: string) => {
    console.log("Drag started for node type:", nodeType);
    event.dataTransfer.setData("application/reactflow", nodeType);
    event.dataTransfer.effectAllowed = "move";
  };

  // Group nodes by category - memoized to avoid recalculation on every render
  const nodesByCategory = useMemo(() => {
    return NODE_TYPES.reduce((acc, node) => {
      if (!acc[node.category]) {
        acc[node.category] = [];
      }
      acc[node.category].push(node);
      return acc;
    }, {} as { [key: string]: typeof NODE_TYPES });
  }, []); // Empty deps - only compute once since NODE_TYPES is static

  // Filter nodes based on search term - memoized to only recompute when search changes
  const filteredNodesByCategory = useMemo(() => {
    return Object.keys(nodesByCategory).reduce((acc, category) => {
      const filteredNodes = nodesByCategory[category].filter(
        (node) =>
          node.label.toLowerCase().includes(searchTerm.toLowerCase()) ||
          node.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
          node.type.toLowerCase().includes(searchTerm.toLowerCase())
      );
      if (filteredNodes.length > 0) {
        acc[category] = filteredNodes;
      }
      return acc;
    }, {} as { [key: string]: typeof NODE_TYPES });
  }, [nodesByCategory, searchTerm]);

  const handleCategoryToggle = (category: string) => {
    setExpandedCategories((prev) =>
      prev.includes(category)
        ? prev.filter((c) => c !== category)
        : [...prev, category]
    );
  };

  return (
    <Paper
      elevation={1}
      sx={{
        width: 320,
        height: "100%",
        display: "flex",
        flexDirection: "column",
        borderRight: 1,
        borderColor: "divider",
      }}
    >
      <Box sx={{ p: 2, borderBottom: 1, borderColor: "divider" }}>
        <Typography variant="h6" component="h3">
          Node Palette
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          Drag nodes to the canvas
        </Typography>
        <TextField
          size="small"
          placeholder="Search nodes..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
          fullWidth
        />
      </Box>

      <Box sx={{ flex: 1, overflow: "auto" }}>
        {Object.keys(filteredNodesByCategory).map((category) => (
          <Accordion
            key={category}
            expanded={expandedCategories.includes(category)}
            onChange={() => handleCategoryToggle(category)}
            sx={{ boxShadow: "none", "&:before": { display: "none" } }}
          >
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              sx={{
                minHeight: 48,
                "&.Mui-expanded": { minHeight: 48 },
                borderBottom: 1,
                borderColor: "divider",
                backgroundColor: "grey.50",
              }}
            >
              <Typography variant="subtitle2" fontWeight="bold">
                {categoryLabels[category]} (
                {filteredNodesByCategory[category].length})
              </Typography>
            </AccordionSummary>
            <AccordionDetails sx={{ p: 1 }}>
              <Box sx={{ display: "flex", flexDirection: "column", gap: 1 }}>
                {filteredNodesByCategory[category].map((node) => (
                  <Card
                    key={node.type}
                    draggable
                    onDragStart={(event) => handleDragStart(event, node.type)}
                    sx={{
                      cursor: "grab",
                      "&:hover": {
                        boxShadow: 2,
                        transform: "translateY(-1px)",
                      },
                      "&:active": {
                        cursor: "grabbing",
                      },
                      transition: "all 0.2s ease-in-out",
                      border: `1px solid ${node.color}30`,
                    }}
                    onClick={() => onAddNode(node.type)}
                  >
                    <CardActionArea>
                      <CardContent sx={{ p: 1.5 }}>
                        <Box
                          sx={{
                            display: "flex",
                            alignItems: "center",
                            gap: 1.5,
                          }}
                        >
                          <Box
                            sx={{
                              color: node.color,
                              display: "flex",
                              alignItems: "center",
                            }}
                          >
                            {iconMap[node.icon] || <HttpIcon />}
                          </Box>
                          <Box sx={{ flex: 1, minWidth: 0 }}>
                            <Typography
                              variant="subtitle2"
                              component="div"
                              noWrap
                            >
                              {node.label}
                            </Typography>
                            <Typography
                              variant="caption"
                              color="text.secondary"
                              noWrap
                              title={node.description}
                            >
                              {node.description.length > 40
                                ? `${node.description.substring(0, 40)}...`
                                : node.description}
                            </Typography>
                          </Box>
                        </Box>
                      </CardContent>
                    </CardActionArea>
                  </Card>
                ))}
              </Box>
            </AccordionDetails>
          </Accordion>
        ))}
      </Box>
    </Paper>
  );
};

// Wrap with React.memo to prevent unnecessary re-renders when parent re-renders
export default React.memo(NodePalette);

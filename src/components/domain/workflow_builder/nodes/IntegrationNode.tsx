import React from "react";
import { Handle, Position } from "@xyflow/react";
import type { NodeProps } from "@xyflow/react";
import { Box, Typography, Chip } from "@mui/material";
import {
  Http as HttpIcon,
  Storage as DatabaseIcon,
  Email as EmailIcon,
  Message as MessageIcon,
} from "@mui/icons-material";

const IntegrationNode: React.FC<NodeProps> = (props) => {
  const { data, selected } = props;
  const getNodeIcon = (nodeType: string) => {
    switch (nodeType) {
      case "http_request":
        return <HttpIcon />;
      case "database_query":
        return <DatabaseIcon />;
      case "email_sender":
        return <EmailIcon />;
      case "slack_message":
        return <MessageIcon />;
      default:
        return <HttpIcon />;
    }
  };

  const getNodeColor = (nodeType: string) => {
    switch (nodeType) {
      case "http_request":
        return "#01579b";
      case "database_query":
        return "#3f51b5";
      case "email_sender":
        return "#e91e63";
      case "slack_message":
        return "#4a148c";
      default:
        return "#01579b";
    }
  };

  const color = getNodeColor(data.nodeType);
  const icon = getNodeIcon(data.nodeType);

  return (
    <Box
      sx={{
        px: 3,
        py: 2,
        minWidth: 160,
        borderRadius: 2,
        border: `2px solid ${selected ? "#ff6b6b" : color}`,
        backgroundColor: "white",
        boxShadow: selected ? 3 : 1,
        transition: "all 0.2s ease-in-out",
        "&:hover": {
          boxShadow: 2,
        },
      }}
    >
      {/* Input handles */}
      {data.inputs && data.inputs.length > 0 ? (
        data.inputs.map((input: string, index: number) => (
          <Handle
            key={`input-${input}`}
            type="target"
            position={Position.Top}
            id={input}
            style={{
              left: `${(index + 1) * (100 / (data.inputs.length + 1))}%`,
              transform: "translateX(-50%)",
              backgroundColor: color,
              border: `2px solid white`,
            }}
            className="w-4 h-4"
          />
        ))
      ) : (
        <Handle
          type="target"
          id="input"
          position={Position.Top}
          style={{
            backgroundColor: color,
            border: `2px solid white`,
          }}
          className="w-4 h-4"
        />
      )}

      <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 1 }}>
        <Box sx={{ color, display: "flex", alignItems: "center" }}>{icon}</Box>
        <Typography variant="subtitle2" fontWeight="bold" sx={{ color }}>
          {data.label}
        </Typography>
      </Box>

      <Typography
        variant="caption"
        sx={{ color: "text.secondary", display: "block", mb: 1 }}
      >
        {data.nodeType.replace("_", " ").toUpperCase()}
      </Typography>

      {data.config && Object.keys(data.config).length > 0 && (
        <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5, mb: 1 }}>
          {Object.entries(data.config)
            .slice(0, 2)
            .map(([key, value]) => (
              <Chip
                key={key}
                label={`${key}: ${String(value).slice(0, 10)}${
                  String(value).length > 10 ? "..." : ""
                }`}
                size="small"
                sx={{
                  backgroundColor: `${color}20`,
                  color: color,
                  fontSize: "0.65rem",
                  height: 20,
                }}
              />
            ))}
        </Box>
      )}

      {/* Output handles */}
      {data.outputs && data.outputs.length > 0 ? (
        data.outputs.map((output: string, index: number) => (
          <Handle
            key={`output-${output}`}
            type="source"
            position={Position.Bottom}
            id={output}
            style={{
              left: `${(index + 1) * (100 / (data.outputs.length + 1))}%`,
              transform: "translateX(-50%)",
              backgroundColor: color,
              border: `2px solid white`,
            }}
            className="w-4 h-4"
          />
        ))
      ) : (
        <Handle
          type="source"
          id="output"
          position={Position.Bottom}
          style={{
            backgroundColor: color,
            border: `2px solid white`,
          }}
          className="w-4 h-4"
        />
      )}
    </Box>
  );
};

export default IntegrationNode;

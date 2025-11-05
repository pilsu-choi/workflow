import React from "react";
import { Handle, Position } from "@xyflow/react";
import type { NodeProps } from "@xyflow/react";
import { Box, Typography, Chip } from "@mui/material";
import { SmartToy as LanguageModelIcon } from "@mui/icons-material";

const LanguageModelNode: React.FC<NodeProps> = (props) => {
  const { data, selected } = props;
  const color = "#9c27b0";

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
      {/* Input handle */}
      <Handle
        type="target"
        id={data.inputs?.[0] || "input"}
        position={Position.Top}
        style={{
          backgroundColor: color,
          border: `2px solid white`,
        }}
        className="w-4 h-4"
      />

      <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 1 }}>
        <Box sx={{ color, display: "flex", alignItems: "center" }}>
          <LanguageModelIcon />
        </Box>
        <Typography variant="subtitle2" fontWeight="bold" sx={{ color }}>
          {data.label}
        </Typography>
      </Box>

      <Typography
        variant="caption"
        sx={{ color: "text.secondary", display: "block", mb: 1 }}
      >
        LANGUAGE MODEL
      </Typography>

      {data.config && Object.keys(data.config).length > 0 && (
        <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5, mb: 1 }}>
          {data.config.provider && (
            <Chip
              label={`Provider: ${data.config.provider}`}
              size="small"
              sx={{
                backgroundColor: `${color}20`,
                color: color,
                fontSize: "0.65rem",
                height: 20,
              }}
            />
          )}
          {data.config.model_name && (
            <Chip
              label={`Model: ${data.config.model_name}`}
              size="small"
              sx={{
                backgroundColor: `${color}20`,
                color: color,
                fontSize: "0.65rem",
                height: 20,
              }}
            />
          )}
        </Box>
      )}

      {/* Output handle */}
      <Handle
        type="source"
        id={data.outputs?.[0] || "output"}
        position={Position.Bottom}
        style={{
          backgroundColor: color,
          border: `2px solid white`,
        }}
        className="w-4 h-4"
      />
    </Box>
  );
};

export default LanguageModelNode;

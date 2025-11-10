import React from "react";
import { Handle, Position } from "@xyflow/react";
import type { NodeProps } from "@xyflow/react";
import { Box, Typography, Chip } from "@mui/material";
import { SmartToy as LanguageModelIcon } from "@mui/icons-material";
import type { FlowNode, NodeInputOutput } from "../../../../types/workflow";

const LanguageModelNode: React.FC<NodeProps<FlowNode>> = (props) => {
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
      {(data.inputs as NodeInputOutput[])?.length > 0 ? (
        (data.inputs as NodeInputOutput[]).map(
          (input: NodeInputOutput, index: number) => {
            const handleId =
              typeof input === "string"
                ? input
                : String(input?.id || input?.name || `input-${index}`);

            return (
              <Handle
                key={`input-${index}-${handleId}`}
                type="target"
                position={Position.Top}
                id={handleId}
                style={{
                  left: `${
                    (index + 1) *
                    (100 / ((data.inputs as NodeInputOutput[]).length + 1))
                  }%`,
                  transform: "translateX(-50%)",
                  backgroundColor: color,
                  border: `2px solid white`,
                }}
                className="w-4 h-4"
              />
            );
          }
        )
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
        <Box sx={{ color, display: "flex", alignItems: "center" }}>
          <LanguageModelIcon />
        </Box>
        <Typography variant="subtitle2" fontWeight="bold" sx={{ color }}>
          {data.nodeType}
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
      {data.outputs && data.outputs.length > 0 ? (
        data.outputs.map((output: NodeInputOutput, index: number) => {
          const handleId =
            typeof output === "string"
              ? output
              : String(output?.id || output?.name || `output-${index}`);

          return (
            <Handle
              key={`output-${index}-${handleId}`}
              type="source"
              id={handleId}
              position={Position.Bottom}
              style={{
                left: `${
                  (index + 1) *
                  (100 / ((data.outputs as NodeInputOutput[]).length + 1))
                }%`,
                transform: "translateX(-50%)",
                backgroundColor: color,
                border: `2px solid white`,
              }}
              className="w-4 h-4"
            />
          );
        })
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

export default LanguageModelNode;

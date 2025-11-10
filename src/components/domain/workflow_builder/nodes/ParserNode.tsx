import React from "react";
import { Handle, Position } from "@xyflow/react";
import type { NodeProps } from "@xyflow/react";
import { Box, Typography, Chip } from "@mui/material";
import { Code as ParserIcon } from "@mui/icons-material";
import type { FlowNode, NodeInputOutput } from "../../../../types";

const ParserNode: React.FC<NodeProps<FlowNode>> = (props) => {
  const { data, selected } = props;
  const color = "#2196f3";

  const getOperationLabel = (operationType: string) => {
    switch (operationType) {
      case "serialize":
        return "JSON → Text";
      case "extract_value":
        return "Extract Value";
      case "extract_fields":
        return "Extract Fields";
      case "add_fields":
        return "Add Fields";
      default:
        return "Parse";
    }
  };

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
      {data.inputs && data.inputs.length > 0 ? (
        data.inputs.map((input: NodeInputOutput, index: number) => {
          const handleId =
            typeof input === "string"
              ? input
              : String(input?.id || input?.name || `input-${index}`);

          return (
            <Handle
              key={`input-${index}-${handleId}`}
              type="target"
              id={handleId}
              position={Position.Top}
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
        })
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
          <ParserIcon />
        </Box>
        <Typography variant="subtitle2" fontWeight="bold" sx={{ color }}>
          {data.label}
        </Typography>
      </Box>

      <Typography
        variant="caption"
        sx={{ color: "text.secondary", display: "block", mb: 1 }}
      >
        PARSER
      </Typography>

      {data.config && Object.keys(data.config).length > 0 && (
        <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5, mb: 1 }}>
          {data.config.operation_type && (
            <Chip
              label={getOperationLabel(data.config.operation_type)}
              size="small"
              sx={{
                backgroundColor: `${color}20`,
                color: color,
                fontSize: "0.65rem",
                height: 20,
              }}
            />
          )}
          {data.config.field_path && (
            <Chip
              label={`Path: ${data.config.field_path}`}
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
        (data.outputs as NodeInputOutput[]).map(
          (output: NodeInputOutput, index: number) => {
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
          }
        )
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

export default ParserNode;

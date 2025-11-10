import React from "react";
import { Handle, Position } from "@xyflow/react";
import type { NodeProps } from "@xyflow/react";
import { Box, Typography, Chip } from "@mui/material";
import {
  HelpOutline as ConditionIcon,
  AccountTree as SwitchIcon,
  CallMerge as MergeIcon,
  CallSplit as SplitIcon,
  Repeat as LoopIcon,
} from "@mui/icons-material";
import type { FlowNode, NodeInputOutput } from "../../../../types";

const LogicNode: React.FC<NodeProps<FlowNode>> = (props) => {
  const { data, selected } = props;

  const getNodeIcon = (nodeType: string) => {
    switch (nodeType) {
      case "if_else":
        return <ConditionIcon />;
      case "loop":
        return <LoopIcon />;
      default:
        return <ConditionIcon />;
    }
  };

  const getNodeColor = (nodeType: string) => {
    switch (nodeType) {
      case "if_else":
        return "#e65100";
      case "loop":
        return "#673ab7";
      default:
        return "#e65100";
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
        data.inputs.map((input: NodeInputOutput, index: number) => {
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
        <Box sx={{ color, display: "flex", alignItems: "center" }}>{icon}</Box>
        <Typography variant="subtitle2" fontWeight="bold" sx={{ color }}>
          {data.label}
        </Typography>
      </Box>

      <Typography
        variant="caption"
        sx={{ color: "text.secondary", display: "block", mb: 1 }}
      >
        {data.nodeType === "if_else" ? "IF/ELSE" : data.nodeType.toUpperCase()}
      </Typography>

      {data.config && Object.keys(data.config).length > 0 && (
        <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5, mb: 1 }}>
          {data.nodeType === "loop" && data.config.loop_type && (
            <Chip
              label={`Type: ${data.config.loop_type.replace("_", " ")}`}
              size="small"
              sx={{
                backgroundColor: `${color}20`,
                color: color,
                fontSize: "0.65rem",
                height: 20,
              }}
            />
          )}
          {data.nodeType === "loop" && data.config.loop_action && (
            <Chip
              label={`Action: ${data.config.loop_action.replace("_", " ")}`}
              size="small"
              sx={{
                backgroundColor: `${color}20`,
                color: color,
                fontSize: "0.65rem",
                height: 20,
              }}
            />
          )}
          {data.nodeType === "if_else" && data.config.operator && (
            <Chip
              label={`Op: ${data.config.operator.replace("_", " ")}`}
              size="small"
              sx={{
                backgroundColor: `${color}20`,
                color: color,
                fontSize: "0.65rem",
                height: 20,
              }}
            />
          )}
          {data.nodeType === "if_else" && data.config.compare_value && (
            <Chip
              label={`Value: ${String(data.config.compare_value).slice(0, 8)}${
                String(data.config.compare_value).length > 8 ? "..." : ""
              }`}
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

      {/* Output handles */}
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

export default LogicNode;

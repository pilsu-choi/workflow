import React from "react";
import { Handle, Position } from "@xyflow/react";
import type { NodeProps } from "@xyflow/react";
import { Box, Typography, Chip } from "@mui/material";
import { Input as ChatInputIcon } from "@mui/icons-material";

const ChatInputNode: React.FC<NodeProps> = (props) => {
  const { data, selected } = props;
  const color = "#ff5722";

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
      <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 1 }}>
        <Box sx={{ color, display: "flex", alignItems: "center" }}>
          <ChatInputIcon />
        </Box>
        <Typography variant="subtitle2" fontWeight="bold" sx={{ color }}>
          {data.label}
        </Typography>
      </Box>

      <Typography
        variant="caption"
        sx={{ color: "text.secondary", display: "block", mb: 1 }}
      >
        CHAT INPUT
      </Typography>

      <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5, mb: 1 }}>
        <Chip
          label="User Input"
          size="small"
          sx={{
            backgroundColor: `${color}20`,
            color: color,
            fontSize: "0.65rem",
            height: 20,
          }}
        />
      </Box>

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

export default ChatInputNode;

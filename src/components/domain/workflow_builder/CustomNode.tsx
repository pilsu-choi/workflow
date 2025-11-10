import React, { useMemo } from "react";
import { Handle, Position } from "@xyflow/react";
import type { NodeProps } from "@xyflow/react";
import LanguageModelNode from "./nodes/LanguageModelNode";
import ParserNode from "./nodes/ParserNode";
import LogicNode from "./nodes/LogicNode";
import ChatInputNode from "./nodes/ChatInputNode";
import ChatOutputNode from "./nodes/ChatOutputNode";
import type { NodeTypeDefinition, FlowNode } from "../../../types/workflow";

// Get node style by type
const getNodeStyle = (nodeType: string, category?: string) => {
  // Use category color if available
  if (category) {
    const categoryColors: Record<string, string> = {
      "AI/ML": "#8b5cf6",
      "Data Processing": "#3b82f6",
      Logic: "#f59e0b",
      "I/O": "#10b981",
      Integration: "#06b6d4",
    };

    const color = categoryColors[category] || "#6b7280";
    return {
      background: "white",
      border: color,
      color: color,
    };
  }

  // Fallback styles for legacy nodes
  const legacyStyles = {
    http_request: {
      background: "white",
      border: "#01579b",
      color: "#01579b",
    },
    data_transform: {
      background: "white",
      border: "#4a148c",
      color: "#4a148c",
    },
    condition: {
      background: "white",
      border: "#e65100",
      color: "#e65100",
    },
    delay: {
      background: "white",
      border: "#2e7d32",
      color: "#2e7d32",
    },
    log: {
      background: "white",
      border: "#c2185b",
      color: "#c2185b",
    },
  };

  return (
    legacyStyles[nodeType as keyof typeof legacyStyles] ||
    legacyStyles.http_request
  );
};

const CustomNode: React.FC<NodeProps<FlowNode>> = React.memo((props) => {
  const { data, selected } = props;

  // data already contains category, inputs, outputs from WorkflowEditor
  const nodeDefinition: NodeTypeDefinition | undefined = data.category
    ? ({
        type: data.nodeType,
        category: data.category,
        inputs: data.inputs || [],
        outputs: data.outputs || [],
      } as NodeTypeDefinition)
    : undefined;

  // Debug: Log inputs/outputs to check their structure
  // if (data.inputs || data.outputs) {
  //   console.log("Node handles:", {
  //     nodeType: data.nodeType,
  //     inputs: data.inputs,
  //     outputs: data.outputs,
  //   });
  // }

  // Memoize style calculation
  const style = useMemo(
    () => getNodeStyle(data.nodeType, data.category),
    [data.nodeType, data.category]
  );

  // Use specialized components based on node type
  if (nodeDefinition) {
    switch (data.nodeType) {
      case "LLM_NODE":
        return <LanguageModelNode {...props} />;
      case "PARSER_NODE":
        return <ParserNode {...props} />;
      case "CONDITION":
      case "loop":
        return <LogicNode {...props} />;
      case "CHAT_INPUT":
        return <ChatInputNode {...props} />;
      case "CHAT_OUTPUT":
        return <ChatOutputNode {...props} />;
      default:
        break;
    }
  }

  // Fallback to generic node for other categories

  return (
    <div
      className="px-4 py-2 shadow-md rounded-md border-2 min-w-[120px]"
      style={{
        backgroundColor: style.background,
        borderColor: selected ? "#ff6b6b" : style.border,
        color: style.color,
      }}
    >
      {/* Input handles */}
      {nodeDefinition?.inputs && nodeDefinition.inputs.length > 0 ? (
        nodeDefinition.inputs.map((input, index) => {
          // Ensure id is a string
          const handleId =
            typeof input === "string"
              ? input
              : typeof input === "object" && input !== null
              ? String(input.name || input.id || `input-${index}`)
              : `input-${index}`;

          return (
            <Handle
              key={`input-${index}-${handleId}`}
              type="target"
              position={Position.Top}
              id={handleId}
              style={{
                left: `${
                  (index + 1) * (100 / (nodeDefinition.inputs.length + 1))
                }%`,
                transform: "translateX(-50%)",
              }}
              className="w-3 h-3"
            />
          );
        })
      ) : (
        <Handle
          type="target"
          id="input"
          position={Position.Top}
          className="w-3 h-3"
        />
      )}

      <div className="font-bold text-sm">{String(data.label)}</div>
      <div className="text-xs opacity-70">{String(data.nodeType)}</div>
      {nodeDefinition?.category && (
        <div className="text-xs opacity-50 capitalize">
          {nodeDefinition.category.replace("_", " ")}
        </div>
      )}

      {/* Output handles */}
      {nodeDefinition?.outputs && nodeDefinition.outputs.length > 0 ? (
        nodeDefinition.outputs.map((output, index) => {
          // Ensure id is a string
          const handleId =
            typeof output === "string"
              ? output
              : typeof output === "object" && output !== null
              ? String(output.name || output.id || `output-${index}`)
              : `output-${index}`;

          return (
            <Handle
              key={`output-${index}-${handleId}`}
              type="source"
              position={Position.Bottom}
              id={handleId}
              style={{
                left: `${
                  (index + 1) * (100 / (nodeDefinition.outputs.length + 1))
                }%`,
                transform: "translateX(-50%)",
              }}
              className="w-3 h-3"
            />
          );
        })
      ) : (
        <Handle
          type="source"
          id="output"
          position={Position.Bottom}
          className="w-3 h-3"
        />
      )}
    </div>
  );
});

CustomNode.displayName = "CustomNode";

export default CustomNode;

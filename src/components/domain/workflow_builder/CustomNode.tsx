import React, { useMemo } from "react";
import { Handle, Position } from "@xyflow/react";
import type { NodeProps } from "@xyflow/react";
import { NODE_TYPES } from "../../../types/workflow";
import LanguageModelNode from "./nodes/LanguageModelNode";
import ParserNode from "./nodes/ParserNode";
import LogicNode from "./nodes/LogicNode";
import ChatInputNode from "./nodes/ChatInputNode";
import ChatOutputNode from "./nodes/ChatOutputNode";

// Get node style by type
const getNodeStyle = (nodeType: string) => {
  const nodeDefinition = NODE_TYPES.find((node) => node.type === nodeType);
  if (nodeDefinition) {
    return {
      background: "white",
      border: nodeDefinition.color,
      color: nodeDefinition.color,
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

const CustomNode: React.FC<NodeProps> = React.memo((props) => {
  const { data, selected } = props;

  // Memoize nodeDefinition to avoid repeated find operations
  const nodeDefinition = useMemo(
    () => NODE_TYPES.find((node) => node.type === data.nodeType),
    [data.nodeType]
  );

  // Memoize style calculation
  const style = useMemo(() => getNodeStyle(data.nodeType), [data.nodeType]);

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
        nodeDefinition.inputs.map((input, index) => (
          <Handle
            key={`input-${input}`}
            type="target"
            position={Position.Top}
            id={input}
            style={{
              left: `${
                (index + 1) * (100 / (nodeDefinition.inputs.length + 1))
              }%`,
              transform: "translateX(-50%)",
            }}
            className="w-3 h-3"
          />
        ))
      ) : (
        <Handle
          type="target"
          id="input"
          position={Position.Top}
          className="w-3 h-3"
        />
      )}

      <div className="font-bold text-sm">{data.label}</div>
      <div className="text-xs opacity-70">{data.nodeType}</div>
      {nodeDefinition?.category && (
        <div className="text-xs opacity-50 capitalize">
          {nodeDefinition.category.replace("_", " ")}
        </div>
      )}

      {/* Output handles */}
      {nodeDefinition?.outputs && nodeDefinition.outputs.length > 0 ? (
        nodeDefinition.outputs.map((output, index) => (
          <Handle
            key={`output-${output}`}
            type="source"
            position={Position.Bottom}
            id={output}
            style={{
              left: `${
                (index + 1) * (100 / (nodeDefinition.outputs.length + 1))
              }%`,
              transform: "translateX(-50%)",
            }}
            className="w-3 h-3"
          />
        ))
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

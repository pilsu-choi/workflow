// Backend API types
export interface Graph {
  id: number;
  name: string;
  description?: string;
  properties?: Record<string, any>;
  created_at?: string;
  updated_at?: string;
}

export interface Vertex {
  id?: number;
  type: string;
  properties: Record<string, any>;
  created_at?: string;
  updated_at?: string;
}

export interface Edge {
  id?: number;
  source_id: number;
  target_id: number;
  type?: string;
  source_properties?: Record<string, any>;
  target_properties?: Record<string, any>;
  created_at?: string;
  updated_at?: string;
}

export interface WorkflowDetail {
  graph: Graph;
  vertices: Vertex[];
  edges: Edge[];
}

export interface WorkflowCreateRequest {
  name: string;
  description?: string;
  vertices: Omit<Vertex, "id" | "created_at" | "updated_at">[];
  edges: Omit<Edge, "id" | "created_at" | "updated_at" | "properties">[];
}

export interface WorkflowCreateResponse {
  success: boolean;
  graph_id: number;
  message: string;
}

export interface WorkflowExecuteRequest {
  initial_inputs?: Record<string, any> | null;
}

export interface WorkflowExecuteResponse {
  success: boolean;
  result: Record<string, any>;
  errors: string[];
  execution_order: string[];
  execution_time: number;
  start_time: string;
  end_time: string;
}

export interface NodeStatus {
  node_id: string;
  status: "pending" | "running" | "completed" | "failed" | "skipped";
  input_data?: Record<string, any>;
  output_data?: Record<string, any>;
  error_message?: string;
}

export interface WorkflowStatus {
  graph_id: number;
  status: "pending" | "running" | "completed" | "failed" | "cancelled";
  nodes: Record<string, NodeStatus>;
}

export interface NodeType {
  type: string;
  name: string;
  description: string;
}

// React Flow types
export interface FlowNode {
  id: string;
  type: string;
  position: { x: number; y: number };
  data: {
    label: string;
    nodeType: string;
    config?: Record<string, any>;
    originalId?: number;
    category?: string;
    inputs?: string[];
    outputs?: string[];
  };
}

export interface FlowEdge {
  id: string;
  source: string;
  target: string;
  sourceHandle?: string;
  targetHandle?: string;
  originalId?: number;
}

// Node type definitions
export interface NodeTypeDefinition {
  type: string;
  label: string;
  description: string;
  category: string;
  icon: string;
  color: string;
  inputs: string[];
  outputs: string[];
  configSchema?: Record<string, any>;
}

// Node categories
export const NODE_CATEGORIES = {
  AI_ML: "ai_ml",
  DATA_PROCESSING: "data_processing",
  LOGIC: "logic",
  INPUT_OUTPUT: "input_output",
} as const;

// Node type definitions
export const NODE_TYPES: NodeTypeDefinition[] = [
  // AI/ML
  {
    type: "LLM_NODE",
    label: "Language Model",
    description: "AI language model with configurable provider and prompts",
    category: NODE_CATEGORIES.AI_ML,
    icon: "SmartToy",
    color: "#9c27b0",
    inputs: ["input"],
    outputs: ["response"],
  },

  // Data Processing
  {
    type: "PARSER_NODE",
    label: "Parser",
    description: "Parse and transform JSON data with various operations",
    category: NODE_CATEGORIES.DATA_PROCESSING,
    icon: "Code",
    color: "#2196f3",
    inputs: ["data"],
    outputs: ["output"],
  },

  // Logic
  {
    type: "CONDITION",
    label: "If/Else",
    description: "Conditional logic with comparison operators",
    category: NODE_CATEGORIES.LOGIC,
    icon: "Condition",
    color: "#e65100",
    inputs: ["value"],
    outputs: ["true", "false"],
  },

  // Input/Output
  {
    type: "CHAT_INPUT",
    label: "CHAT INPUT",
    description: "Input node for chat-based workflows",
    category: NODE_CATEGORIES.INPUT_OUTPUT,
    icon: "Input",
    color: "#ff5722",
    inputs: [],
    outputs: ["output"],
  },
  {
    type: "CHAT_OUTPUT",
    label: "CHAT OUTPUT",
    description:
      "Output node for chat-based workflows with configurable formatting",
    category: NODE_CATEGORIES.INPUT_OUTPUT,
    icon: "Reply",
    color: "#4caf50",
    inputs: ["input"],
    outputs: ["output"],
  },
];

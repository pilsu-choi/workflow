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
    inputs?: NodeInputOutput[];
    outputs?: NodeInputOutput[];
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

/**
 * Node Input/Output port types
 */
export const NodeInputOutputType = {
  TEXT: "TEXT",
  JSON: "JSON",
  FILE: "FILE",
  NUMBER: "NUMBER",
  BOOLEAN: "BOOLEAN",
  ARRAY: "ARRAY",
  OBJECT: "OBJECT",
};

/**
 * Node Input/Output port definition
 */
export interface NodeInputOutput {
  /** Port ID (8-character UUID) */
  id: string;
  /** Field name corresponding to the input/output */
  name: string;
  /** Input/Output type */
  type: keyof typeof NodeInputOutputType;
  /** Whether this field is required */
  required: boolean;
  /** Default or current value */
  value?: any;
  /** Description of the field */
  description: string;
}

/**
 * Node type categories
 */
export const NODE_CATEGORIES = {
  AI_ML: "AI_ML",
  DATA_PROCESSING: "DATA_PROCESSING",
  LOGIC: "LOGIC",
  INPUT_OUTPUT: "INPUT_OUTPUT",
};

/**
 * Node type definition
 */
export interface NodeTypeDefinition {
  /** Node type identifier */
  type: keyof typeof NodeType;
  /** Display label */
  label: string;
  /** Description of the node */
  description: string;
  /** Category of the node */
  category: keyof typeof NODE_CATEGORIES;
  /** Icon name (e.g., Material UI icon) */
  icon: string;
  /** Color in hex format */
  color: string;
  /** Input port definitions */
  inputs: NodeInputOutput[];
  /** Output port definitions */
  outputs: NodeInputOutput[];
}

/**
 * Available node types
 */
export const NodeType = {
  // Input/Output nodes
  CHAT_INPUT: "CHAT_INPUT",
  CHAT_OUTPUT: "CHAT_OUTPUT",

  // Processing nodes
  LLM_NODE: "LLM_NODE",
  CONDITION: "CONDITION",
  LOOP: "LOOP",

  // Utility nodes
  PARSER_NODE: "PARSER_NODE",
};

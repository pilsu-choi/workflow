# Workflow Builder Frontend

A visual workflow builder application built with React and TypeScript, enabling users to create, edit, and execute node-based workflows with AI/ML capabilities.

## 🚀 Features

- **Visual Workflow Editor**: Drag-and-drop interface powered by React Flow
- **Multiple Node Types**:
  - 🤖 **AI/ML Nodes**: Language Model (LLM) integration
  - 📊 **Data Processing**: JSON parser and transformer
  - 🔀 **Logic**: Conditional if/else branching
  - 💬 **Input/Output**: Chat input/output nodes
- **Real-time Workflow Execution**: Execute and monitor workflow status
- **Workflow Management**: Create, save, and load workflows
- **Modern UI**: Built with Material-UI and Tailwind CSS
- **Type-Safe**: Full TypeScript support

## 🛠️ Tech Stack

- **Framework**: React 19 + TypeScript
- **Build Tool**: Vite
- **UI Libraries**: 
  - Material-UI (MUI)
  - Tailwind CSS
- **Workflow Visualization**: React Flow (@xyflow/react)
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Routing**: React Router DOM

## 📋 Prerequisites

- Node.js (v18 or higher recommended)
- npm or yarn package manager

## 🏗️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd workflow-fe
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## 📦 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 🏗️ Project Structure

```
workflow-fe/
├── src/
│   ├── components/
│   │   └── domain/
│   │       └── workflow_builder/    # Workflow builder components
│   │           ├── NodePalette.tsx  # Node selection palette
│   │           ├── NodePanel.tsx    # Node configuration panel
│   │           ├── CustomNode.tsx   # Custom node component
│   │           └── nodes/           # Specific node implementations
│   ├── pages/                       # Page components
│   │   ├── HomePage.tsx
│   │   ├── WorkflowSelectionPage.tsx
│   │   └── WorkflowBuilderPage.tsx
│   ├── types/                       # TypeScript type definitions
│   │   └── workflow.ts              # Workflow-related types
│   ├── services/                    # API services
│   ├── stores/                      # Zustand stores
│   ├── hooks/                       # Custom React hooks
│   └── App.tsx                      # Main application component
├── public/                          # Static assets
└── package.json
```

## 🎯 Usage

### Creating a Workflow

1. Navigate to the workflow selection page
2. Create a new workflow or select an existing one
3. Drag nodes from the palette onto the canvas
4. Connect nodes by dragging from output handles to input handles
5. Configure node properties in the side panel
6. Save your workflow

### Node Types

#### AI/ML Nodes
- **Language Model (LLM_NODE)**: Configure AI language models with custom prompts and providers

#### Data Processing Nodes
- **Parser (PARSER_NODE)**: Parse and transform JSON data with various operations

#### Logic Nodes
- **If/Else (CONDITION)**: Conditional branching based on comparison operators

#### Input/Output Nodes
- **Chat Input (CHAT_INPUT)**: Entry point for chat-based workflows
- **Chat Output (CHAT_OUTPUT)**: Output formatting for chat responses

## 🔌 API Integration

The frontend communicates with a backend API for:
- Workflow CRUD operations
- Workflow execution
- Node status monitoring

Ensure the backend API is running and accessible.

## 🎨 Customization

### Adding New Node Types

1. Define the node type in `src/types/workflow.ts`:
```typescript
{
  type: "NEW_NODE_TYPE",
  label: "New Node",
  description: "Description of the new node",
  category: NODE_CATEGORIES.YOUR_CATEGORY,
  icon: "IconName",
  color: "#hexcolor",
  inputs: ["input1"],
  outputs: ["output1"],
}
```

2. Create a component in `src/components/domain/workflow_builder/nodes/`
3. Register the node in the workflow builder

## 🐛 Development

### Type Definitions

The application uses comprehensive TypeScript types defined in `src/types/workflow.ts`:
- `Graph`, `Vertex`, `Edge` - Backend API types
- `FlowNode`, `FlowEdge` - React Flow types
- `NodeTypeDefinition` - Node metadata

### State Management

Zustand stores are used for managing:
- Workflow state
- Node configurations
- Execution status

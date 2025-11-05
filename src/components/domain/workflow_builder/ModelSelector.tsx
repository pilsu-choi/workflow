import React from "react";
import { FormControl, InputLabel, Select, MenuItem } from "@mui/material";

// 모델 데이터 구조 정의
interface ModelData {
  [provider: string]: string[];
}

// 모든 provider의 모델 목록을 중앙화
const MODEL_DATA: ModelData = {
  openai: [
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k",
    "gpt-4",
    "gpt-4-32k",
    "gpt-4-turbo",
    "gpt-4o",
    "gpt-4o-mini",
    "text-davinci-003",
    "text-davinci-002",
    "text-curie-001",
    "text-babbage-001",
    "text-ada-001",
  ],
  anthropic: [
    "claude-3-haiku",
    "claude-3-haiku-20240307",
    "claude-3-sonnet",
    "claude-3-sonnet-20240229",
    "claude-3-opus",
    "claude-3-opus-20240229",
    "claude-2.1",
    "claude-2.0",
    "claude-instant-1.2",
    "claude-instant-1.1",
  ],
  google: [
    "gemini-pro",
    "gemini-pro-vision",
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    "gemini-1.0-pro",
    "text-bison-001",
    "text-bison-32k",
    "chat-bison-001",
    "chat-bison-32k",
    "code-bison-001",
    "code-bison-32k",
  ],
  meta: [
    "llama-2-7b-chat",
    "llama-2-13b-chat",
    "llama-2-70b-chat",
    "llama-3-8b-instruct",
    "llama-3-70b-instruct",
    "codellama-7b-instruct",
    "codellama-13b-instruct",
    "codellama-34b-instruct",
  ],
  cohere: [
    "command",
    "command-light",
    "command-nightly",
    "command-light-nightly",
    "summarize-medium",
    "summarize-xlarge",
    "embed-english-v2.0",
    "embed-multilingual-v2.0",
  ],
  huggingface: [
    "microsoft/DialoGPT-medium",
    "microsoft/DialoGPT-large",
    "facebook/blenderbot-400M-distill",
    "facebook/blenderbot-1B-distill",
    "EleutherAI/gpt-neo-2.7B",
    "EleutherAI/gpt-j-6B",
    "bigscience/bloom-560m",
    "bigscience/bloom-1b7",
  ],
  mistral: [
    "mistral-tiny",
    "mistral-small",
    "mistral-medium",
    "mistral-large",
    "codestral-latest",
    "pixtral-12b-2409",
  ],
  perplexity: [
    "llama-3.1-sonar-small-128k-online",
    "llama-3.1-sonar-small-128k-chat",
    "llama-3.1-sonar-large-128k-online",
    "llama-3.1-sonar-large-128k-chat",
    "llama-3.1-sonar-huge-128k-online",
    "llama-3.1-sonar-huge-128k-chat",
  ],
  groq: [
    "llama3-8b-8192",
    "llama3-70b-8192",
    "llama3-8b-8192-tool-use-preview",
    "llama3-70b-8192-tool-use-preview",
    "mixtral-8x7b-32768",
    "gemma-7b-it",
    "gemma2-9b-it",
    "gemma2-27b-it",
  ],
};

interface ModelSelectorProps {
  provider: string;
  selectedModel: string;
  onModelChange: (model: string) => void;
  disabled?: boolean;
}

const ModelSelector: React.FC<ModelSelectorProps> = ({
  provider,
  selectedModel,
  onModelChange,
  disabled = false,
}) => {
  const models = MODEL_DATA[provider] || [];

  return (
    <FormControl fullWidth size="small">
      <InputLabel>Model Name</InputLabel>
      <Select
        value={selectedModel || ""}
        label="Model Name"
        disabled={disabled || !provider}
      >
        {models.map((model) => (
          <MenuItem
            key={model}
            value={model}
            onClick={() => onModelChange(model)}
          >
            {model}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default ModelSelector;

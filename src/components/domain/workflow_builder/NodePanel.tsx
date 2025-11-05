import React, { useState, useEffect, useCallback, useMemo } from "react";
import {
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  IconButton,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Divider,
  Alert,
} from "@mui/material";
import {
  Close as CloseIcon,
  Save as SaveIcon,
  Delete as DeleteIcon,
  Add as AddIcon,
  Remove as RemoveIcon,
} from "@mui/icons-material";
import type { Node } from "@xyflow/react";
import ModelSelector from "./ModelSelector";

interface NodePanelProps {
  selectedNode: Node | null;
  onNodeUpdate: (nodeId: string, updates: any) => void;
  onNodeDelete: (nodeId: string) => void;
  onClose: () => void;
}

const NodePanel: React.FC<NodePanelProps> = ({
  selectedNode,
  onNodeUpdate,
  onNodeDelete,
  onClose,
}) => {
  const [formData, setFormData] = useState({
    name: "",
    nodeType: "",
    config: {} as Record<string, any>,
  });
  const [jsonError, setJsonError] = useState<string | null>(null);
  const [fieldsToAdd, setFieldsToAdd] = useState<
    Array<{ key: string; value: string }>
  >([]);

  useEffect(() => {
    if (selectedNode) {
      setFormData({
        name: selectedNode.data.label,
        nodeType: selectedNode.data.nodeType,
        config: selectedNode.data.config || {},
      });
      setJsonError(null);

      // Initialize fieldsToAdd from config
      const fieldsToAddConfig = selectedNode.data.config?.fields_to_add || {};
      const fieldsArray = Object.entries(fieldsToAddConfig).map(
        ([key, value]) => ({
          key,
          value: String(value),
        })
      );
      setFieldsToAdd(
        fieldsArray.length > 0 ? fieldsArray : [{ key: "", value: "" }]
      );
    }
  }, [selectedNode]);

  const handleSave = useCallback(() => {
    if (selectedNode) {
      let data = {
        name: formData.name,
        node_type: formData.nodeType,
        node_config: formData.config,
      };
      console.log("data", data);
      onNodeUpdate(selectedNode.id, data);
    }
  }, [selectedNode, formData, onNodeUpdate]);

  const handleDelete = useCallback(() => {
    if (
      selectedNode &&
      window.confirm("Are you sure you want to delete this node?")
    ) {
      onNodeDelete(selectedNode.id);
    }
  }, [selectedNode, onNodeDelete]);

  const updateConfig = useCallback((key: string, value: any) => {
    setFormData((prev) => {
      const newConfig = {
        ...prev.config,
        [key]: value,
      };

      // If provider changes, reset model_name to avoid invalid combinations
      if (key === "provider") {
        newConfig.model_name = "";
      }

      return {
        ...prev,
        config: newConfig,
      };
    });
  }, []);

  const handleJsonChange = useCallback((key: string, value: string) => {
    try {
      const parsed = JSON.parse(value);
      updateConfig(key, parsed);
      setJsonError(null);
    } catch (error) {
      setJsonError("Invalid JSON format");
    }
  }, [updateConfig]);

  const handleFieldKeyChange = useCallback((index: number, key: string) => {
    const newFields = [...fieldsToAdd];
    newFields[index].key = key;
    setFieldsToAdd(newFields);

    // Update config with the new fields
    const fieldsObject = newFields.reduce((acc, field) => {
      if (field.key && field.value) {
        acc[field.key] = field.value;
      }
      return acc;
    }, {} as Record<string, string>);
    updateConfig("fields_to_add", fieldsObject);
  }, [fieldsToAdd, updateConfig]);

  const handleFieldValueChange = useCallback((index: number, value: string) => {
    const newFields = [...fieldsToAdd];
    newFields[index].value = value;
    setFieldsToAdd(newFields);

    // Update config with the new fields
    const fieldsObject = newFields.reduce((acc, field) => {
      if (field.key && field.value) {
        acc[field.key] = field.value;
      }
      return acc;
    }, {} as Record<string, string>);
    updateConfig("fields_to_add", fieldsObject);
  }, [fieldsToAdd, updateConfig]);

  const addField = useCallback(() => {
    setFieldsToAdd([...fieldsToAdd, { key: "", value: "" }]);
  }, [fieldsToAdd]);

  const removeField = useCallback((index: number) => {
    if (fieldsToAdd.length > 1) {
      const newFields = fieldsToAdd.filter((_, i) => i !== index);
      setFieldsToAdd(newFields);

      // Update config with the new fields
      const fieldsObject = newFields.reduce((acc, field) => {
        if (field.key && field.value) {
          acc[field.key] = field.value;
        }
        return acc;
      }, {} as Record<string, string>);
      updateConfig("fields_to_add", fieldsObject);
    }
  }, [fieldsToAdd, updateConfig]);

  const renderNodeConfig = useMemo(() => {
    switch (formData.nodeType) {
      case "language_model":
        return (
          <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
            <FormControl fullWidth size="small">
              <InputLabel>Model Provider</InputLabel>
              <Select
                value={formData.config.provider || "openai"}
                onChange={(e) => updateConfig("provider", e.target.value)}
                label="Model Provider"
              >
                <MenuItem value="openai">OpenAI</MenuItem>
                <MenuItem value="anthropic">Anthropic</MenuItem>
                <MenuItem value="google">Google</MenuItem>
                <MenuItem value="meta">Meta</MenuItem>
                <MenuItem value="cohere">Cohere</MenuItem>
                <MenuItem value="huggingface">Hugging Face</MenuItem>
                <MenuItem value="mistral">Mistral AI</MenuItem>
                <MenuItem value="perplexity">Perplexity</MenuItem>
                <MenuItem value="groq">Groq</MenuItem>
              </Select>
            </FormControl>
            <ModelSelector
              provider={formData.config.provider || "openai"}
              selectedModel={formData.config.model_name || ""}
              onModelChange={(model) => updateConfig("model_name", model)}
              disabled={!formData.config.provider}
            />
            <TextField
              label="API Key"
              type="password"
              value={formData.config.api_key || ""}
              onChange={(e) => updateConfig("api_key", e.target.value)}
              fullWidth
              variant="outlined"
              size="small"
              placeholder="Enter your API key"
            />
            <TextField
              label="User Prompt"
              value={formData.config.user_prompt || ""}
              onChange={(e) => updateConfig("user_prompt", e.target.value)}
              fullWidth
              multiline
              rows={3}
              variant="outlined"
              size="small"
              placeholder="Enter user prompt here. Use {{variable}} for templating."
            />
            <TextField
              label="System Prompt"
              value={formData.config.system_prompt || ""}
              onChange={(e) => updateConfig("system_prompt", e.target.value)}
              fullWidth
              multiline
              rows={3}
              variant="outlined"
              size="small"
              placeholder="Enter system prompt here."
            />
          </Box>
        );

      case "parser":
        return (
          <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
            <FormControl fullWidth size="small">
              <InputLabel>Operation Type</InputLabel>
              <Select
                value={formData.config.operation_type || "serialize"}
                onChange={(e) => updateConfig("operation_type", e.target.value)}
                label="Operation Type"
              >
                <MenuItem value="serialize">JSON 텍스트 변환</MenuItem>
                <MenuItem value="extract_value">JSON 값 추출</MenuItem>
                <MenuItem value="extract_fields">JSON 값 제거</MenuItem>
                <MenuItem value="add_fields">JSON 필드 추가</MenuItem>
              </Select>
            </FormControl>
            {formData.config.operation_type === "extract_value" && (
              <TextField
                label="Field Path"
                value={formData.config.field_path || ""}
                onChange={(e) => updateConfig("field_path", e.target.value)}
                fullWidth
                variant="outlined"
                size="small"
                placeholder="e.g., user.name, data.items[0].title"
              />
            )}
            {formData.config.operation_type === "extract_fields" && (
              <TextField
                label="Fields to Extract"
                value={formData.config.fields_to_extract || ""}
                onChange={(e) =>
                  updateConfig("fields_to_extract", e.target.value)
                }
                fullWidth
                variant="outlined"
                size="small"
                placeholder="e.g., name, email, age (comma-separated)"
              />
            )}
            {formData.config.operation_type === "add_fields" && (
              <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
                <Typography variant="subtitle2">Fields to Add</Typography>
                {fieldsToAdd.map((field, index) => (
                  <Box
                    key={index}
                    sx={{ display: "flex", gap: 1, alignItems: "center" }}
                  >
                    <TextField
                      label="Key"
                      value={field.key}
                      onChange={(e) =>
                        handleFieldKeyChange(index, e.target.value)
                      }
                      variant="outlined"
                      size="small"
                      placeholder="Field name"
                      sx={{ flex: 1 }}
                    />
                    <TextField
                      label="Value"
                      value={field.value}
                      onChange={(e) =>
                        handleFieldValueChange(index, e.target.value)
                      }
                      variant="outlined"
                      size="small"
                      placeholder="Field value"
                      sx={{ flex: 1 }}
                    />
                    <IconButton
                      onClick={() => removeField(index)}
                      disabled={fieldsToAdd.length === 1}
                      size="small"
                      color="error"
                    >
                      <RemoveIcon />
                    </IconButton>
                  </Box>
                ))}
                <Button
                  startIcon={<AddIcon />}
                  onClick={addField}
                  variant="outlined"
                  size="small"
                  sx={{ alignSelf: "flex-start" }}
                >
                  Add Field
                </Button>
              </Box>
            )}
          </Box>
        );

      case "if_else":
        return (
          <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
            <TextField
              label="Input Field"
              value={formData.config.input_field || ""}
              onChange={(e) => updateConfig("input_field", e.target.value)}
              fullWidth
              variant="outlined"
              size="small"
              placeholder="Field to compare (e.g., user.age, data.status)"
            />
            <FormControl fullWidth size="small">
              <InputLabel>Operator</InputLabel>
              <Select
                value={formData.config.operator || ""}
                onChange={(e) => updateConfig("operator", e.target.value)}
                label="Operator"
              >
                <MenuItem value="equal">Equal</MenuItem>
                <MenuItem value="not_equal">Not Equal</MenuItem>
                <MenuItem value="less_than">Less Than</MenuItem>
                <MenuItem value="greater_than">Greater Than</MenuItem>
                <MenuItem value="less_equal">Less than or equal</MenuItem>
                <MenuItem value="greater_equal">Greater than or equal</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Compare Value"
              value={formData.config.compare_value || ""}
              onChange={(e) => updateConfig("compare_value", e.target.value)}
              fullWidth
              variant="outlined"
              size="small"
              placeholder="Value to compare against"
            />
          </Box>
        );

      case "loop":
        return (
          <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
            <FormControl fullWidth size="small">
              <InputLabel>Loop Type</InputLabel>
              <Select
                value={formData.config.loop_type || "for_each"}
                onChange={(e) => updateConfig("loop_type", e.target.value)}
                label="Loop Type"
              >
                <MenuItem value="for_each">For Each (배열 반복)</MenuItem>
                <MenuItem value="while">While (조건 반복)</MenuItem>
                <MenuItem value="count">Count (횟수 반복)</MenuItem>
                <MenuItem value="range">Range (범위 반복)</MenuItem>
              </Select>
            </FormControl>

            {/* For Each 설정 */}
            {formData.config.loop_type === "for_each" && (
              <>
                <TextField
                  label="Input Collection"
                  value={formData.config.input_collection || ""}
                  onChange={(e) =>
                    updateConfig("input_collection", e.target.value)
                  }
                  fullWidth
                  variant="outlined"
                  size="small"
                  placeholder="e.g., data.items, users, products"
                  helperText="반복할 배열이나 리스트의 경로를 입력하세요"
                />
                <FormControl fullWidth size="small">
                  <InputLabel>Loop Action</InputLabel>
                  <Select
                    value={formData.config.loop_action || "process_item"}
                    onChange={(e) =>
                      updateConfig("loop_action", e.target.value)
                    }
                    label="Loop Action"
                  >
                    <MenuItem value="process_item">
                      Process Item (항목 처리)
                    </MenuItem>
                    <MenuItem value="transform_data">
                      Transform Data (데이터 변환)
                    </MenuItem>
                    <MenuItem value="call_api">Call API (API 호출)</MenuItem>
                    <MenuItem value="custom_logic">
                      Custom Logic (사용자 정의)
                    </MenuItem>
                  </Select>
                </FormControl>
              </>
            )}

            {/* While 설정 */}
            {formData.config.loop_type === "while" && (
              <>
                <TextField
                  label="Condition Field"
                  value={formData.config.condition_field || ""}
                  onChange={(e) =>
                    updateConfig("condition_field", e.target.value)
                  }
                  fullWidth
                  variant="outlined"
                  size="small"
                  placeholder="e.g., data.status, user.active"
                  helperText="조건을 확인할 필드 경로"
                />
                <FormControl fullWidth size="small">
                  <InputLabel>Condition Operator</InputLabel>
                  <Select
                    value={formData.config.condition_operator || "equals"}
                    onChange={(e) =>
                      updateConfig("condition_operator", e.target.value)
                    }
                    label="Condition Operator"
                  >
                    <MenuItem value="equals">Equals (==)</MenuItem>
                    <MenuItem value="not_equals">Not Equals (!=)</MenuItem>
                    <MenuItem value="greater_than">
                      Greater Than (&gt;)
                    </MenuItem>
                    <MenuItem value="less_than">Less Than (&lt;)</MenuItem>
                    <MenuItem value="contains">Contains</MenuItem>
                    <MenuItem value="not_contains">Not Contains</MenuItem>
                  </Select>
                </FormControl>
                <TextField
                  label="Condition Value"
                  value={formData.config.condition_value || ""}
                  onChange={(e) =>
                    updateConfig("condition_value", e.target.value)
                  }
                  fullWidth
                  variant="outlined"
                  size="small"
                  placeholder="e.g., active, completed, 100"
                  helperText="조건과 비교할 값"
                />
                <FormControl fullWidth size="small">
                  <InputLabel>Loop Action</InputLabel>
                  <Select
                    value={formData.config.loop_action || "process_item"}
                    onChange={(e) =>
                      updateConfig("loop_action", e.target.value)
                    }
                    label="Loop Action"
                  >
                    <MenuItem value="process_item">
                      Process Item (항목 처리)
                    </MenuItem>
                    <MenuItem value="transform_data">
                      Transform Data (데이터 변환)
                    </MenuItem>
                    <MenuItem value="call_api">Call API (API 호출)</MenuItem>
                    <MenuItem value="custom_logic">
                      Custom Logic (사용자 정의)
                    </MenuItem>
                  </Select>
                </FormControl>
              </>
            )}

            {/* Count 설정 */}
            {formData.config.loop_type === "count" && (
              <>
                <TextField
                  label="Iteration Count"
                  type="number"
                  value={formData.config.iteration_count || 1}
                  onChange={(e) =>
                    updateConfig("iteration_count", parseInt(e.target.value))
                  }
                  fullWidth
                  variant="outlined"
                  size="small"
                  inputProps={{ min: 1, max: 1000 }}
                  helperText="반복할 횟수를 입력하세요 (1-1000)"
                />
                <FormControl fullWidth size="small">
                  <InputLabel>Loop Action</InputLabel>
                  <Select
                    value={formData.config.loop_action || "process_item"}
                    onChange={(e) =>
                      updateConfig("loop_action", e.target.value)
                    }
                    label="Loop Action"
                  >
                    <MenuItem value="process_item">
                      Process Item (항목 처리)
                    </MenuItem>
                    <MenuItem value="transform_data">
                      Transform Data (데이터 변환)
                    </MenuItem>
                    <MenuItem value="call_api">Call API (API 호출)</MenuItem>
                    <MenuItem value="custom_logic">
                      Custom Logic (사용자 정의)
                    </MenuItem>
                  </Select>
                </FormControl>
              </>
            )}

            {/* Range 설정 */}
            {formData.config.loop_type === "range" && (
              <>
                <TextField
                  label="Start Value"
                  type="number"
                  value={formData.config.start_value || 0}
                  onChange={(e) =>
                    updateConfig("start_value", parseInt(e.target.value))
                  }
                  fullWidth
                  variant="outlined"
                  size="small"
                  helperText="시작값"
                />
                <TextField
                  label="End Value"
                  type="number"
                  value={formData.config.end_value || 10}
                  onChange={(e) =>
                    updateConfig("end_value", parseInt(e.target.value))
                  }
                  fullWidth
                  variant="outlined"
                  size="small"
                  helperText="끝값 (포함되지 않음)"
                />
                <TextField
                  label="Step Value"
                  type="number"
                  value={formData.config.step_value || 1}
                  onChange={(e) =>
                    updateConfig("step_value", parseInt(e.target.value))
                  }
                  fullWidth
                  variant="outlined"
                  size="small"
                  inputProps={{ min: 1 }}
                  helperText="증가값 (기본값: 1)"
                />
                <FormControl fullWidth size="small">
                  <InputLabel>Loop Action</InputLabel>
                  <Select
                    value={formData.config.loop_action || "process_item"}
                    onChange={(e) =>
                      updateConfig("loop_action", e.target.value)
                    }
                    label="Loop Action"
                  >
                    <MenuItem value="process_item">
                      Process Item (항목 처리)
                    </MenuItem>
                    <MenuItem value="transform_data">
                      Transform Data (데이터 변환)
                    </MenuItem>
                    <MenuItem value="call_api">Call API (API 호출)</MenuItem>
                    <MenuItem value="custom_logic">
                      Custom Logic (사용자 정의)
                    </MenuItem>
                  </Select>
                </FormControl>
              </>
            )}

            {/* 공통 설정 */}
            <TextField
              label="Output Collection Name"
              value={formData.config.output_collection || ""}
              onChange={(e) =>
                updateConfig("output_collection", e.target.value)
              }
              fullWidth
              variant="outlined"
              size="small"
              placeholder="e.g., processed_items, results"
              helperText="반복 결과를 저장할 컬렉션 이름"
            />
          </Box>
        );

      case "CHAT_INPUT":
        return (
          <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
            <Alert severity="info">
              Chat Input node provides user input for chat-based workflows. No
              additional configuration required.
            </Alert>
          </Box>
        );

      case "CHAT_OUTPUT":
        return (
          <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
            <Alert severity="info">
              Chat Output node provides formatted output for chat-based
              workflows. No additional configuration required.
            </Alert>
          </Box>
        );

      default:
        return (
          <Alert severity="info">
            No configuration available for this node type.
          </Alert>
        );
    }
  }, [
    formData.nodeType,
    formData.config,
    updateConfig,
    fieldsToAdd,
    handleFieldKeyChange,
    handleFieldValueChange,
    removeField,
    addField,
  ]);

  if (!selectedNode) {
    return null;
  }

  return (
    <Paper
      elevation={1}
      sx={{
        width: 320,
        height: "100%",
        display: "flex",
        flexDirection: "column",
        borderLeft: 1,
        borderColor: "divider",
      }}
    >
      <Box sx={{ p: 2, borderBottom: 1, borderColor: "divider" }}>
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <Typography variant="h6" component="h3">
            Node Configuration
          </Typography>
          <IconButton onClick={onClose} size="small">
            <CloseIcon />
          </IconButton>
        </Box>
      </Box>

      <Box sx={{ flex: 1, overflow: "auto", p: 2 }}>
        <Box sx={{ display: "flex", flexDirection: "column", gap: 3 }}>
          <TextField
            label="Name"
            value={formData.name}
            onChange={(e) =>
              setFormData((prev) => ({ ...prev, name: e.target.value }))
            }
            fullWidth
            variant="outlined"
            size="small"
          />

          <FormControl fullWidth size="small">
            <InputLabel>Node Type</InputLabel>
            <Select
              value={formData.nodeType}
              onChange={(e) =>
                setFormData((prev) => ({ ...prev, nodeType: e.target.value }))
              }
              label="Node Type"
            >
              <MenuItem value="language_model">Language Model</MenuItem>
              <MenuItem value="parser">Parser</MenuItem>
              <MenuItem value="if_else">If/Else</MenuItem>
              <MenuItem value="loop">Loop</MenuItem>
              <MenuItem value="chat_input">Chat Input</MenuItem>
              <MenuItem value="chat_output">Chat Output</MenuItem>
            </Select>
          </FormControl>

          <Divider />

          <Box>
            <Typography variant="subtitle2" gutterBottom>
              Configuration
            </Typography>
            {renderNodeConfig}
          </Box>

          <Box sx={{ display: "flex", gap: 1, mt: 2 }}>
            <Button
              variant="contained"
              startIcon={<SaveIcon />}
              onClick={handleSave}
              fullWidth
            >
              Save
            </Button>
            <Button
              variant="outlined"
              color="error"
              startIcon={<DeleteIcon />}
              onClick={handleDelete}
              fullWidth
            >
              Delete
            </Button>
          </Box>
        </Box>
      </Box>
    </Paper>
  );
};

// Wrap with React.memo to prevent unnecessary re-renders when parent re-renders
export default React.memo(NodePanel);

import React, { useState, useRef, useEffect } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Box,
  Typography,
  Paper,
  IconButton,
  CircularProgress,
  Chip,
} from "@mui/material";
import {
  Send as SendIcon,
  Close as CloseIcon,
  Chat as ChatIcon,
} from "@mui/icons-material";
import { workflowApi } from "../../../../services/workflow/api";

interface Message {
  id: string;
  text: string;
  sender: "user" | "bot";
  timestamp: Date;
  isExecuting?: boolean;
}

interface ChatModalProps {
  open: boolean;
  onClose: () => void;
  workflowId: number;
  workflowName: string;
}

const ChatModal: React.FC<ChatModalProps> = ({
  open,
  onClose,
  workflowId,
  workflowName,
}) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      text: `안녕하세요! "${workflowName}" 워크플로우를 테스트해보세요. 메시지를 입력하면 워크플로우가 실행됩니다.`,
      sender: "bot",
      timestamp: new Date(),
    },
  ]);
  const [inputText, setInputText] = useState("");
  const [isExecuting, setIsExecuting] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputText.trim() || isExecuting) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      sender: "user",
      timestamp: new Date(),
    };

    const botMessage: Message = {
      id: (Date.now() + 1).toString(),
      text: "워크플로우를 실행하고 있습니다...",
      sender: "bot",
      timestamp: new Date(),
      isExecuting: true,
    };

    setMessages((prev) => [...prev, userMessage, botMessage]);
    setInputText("");
    setIsExecuting(true);

    try {
      // 워크플로우 실행
      const response = await workflowApi.executeWorkflow(workflowId, {
        initial_inputs: { test_data: inputText, trigger_type: "chat" },
      });

      if (!response.data.success) {
        const errorMessage: Message = {
          id: (Date.now() + 2).toString(),
          text: `워크플로우 실행 실패!\n오류: ${response.data.errors.join(
            ", "
          )}`,
          sender: "bot",
          timestamp: new Date(),
        };

        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === botMessage.id
              ? { ...msg, text: errorMessage.text, isExecuting: false }
              : msg
          )
        );
        setIsExecuting(false);
        return;
      }

      // 실행 상태 폴링
      const pollStatus = async () => {
        try {
          const statusResponse = await workflowApi.getWorkflowStatus(
            workflowId
          );
          const status = statusResponse.data.status;

          if (
            status === "completed" ||
            status === "failed" ||
            status === "cancelled"
          ) {
            const resultMessage: Message = {
              id: (Date.now() + 2).toString(),
              text: `워크플로우 실행 완료! 상태: ${status}${
                response.data.result
                  ? `\n결과: ${JSON.stringify(response.data.result, null, 2)}`
                  : ""
              }`,
              sender: "bot",
              timestamp: new Date(),
            };

            setMessages((prev) =>
              prev.map((msg) =>
                msg.id === botMessage.id
                  ? { ...msg, text: resultMessage.text, isExecuting: false }
                  : msg
              )
            );
            setIsExecuting(false);
          } else {
            setTimeout(pollStatus, 1000);
          }
        } catch (error) {
          console.error("Failed to poll execution status:", error);
          const errorMessage: Message = {
            id: (Date.now() + 2).toString(),
            text: "워크플로우 실행 상태를 확인하는 중 오류가 발생했습니다.",
            sender: "bot",
            timestamp: new Date(),
          };

          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === botMessage.id
                ? { ...msg, text: errorMessage.text, isExecuting: false }
                : msg
            )
          );
          setIsExecuting(false);
        }
      };

      setTimeout(pollStatus, 1000);
    } catch (error) {
      console.error("Failed to execute workflow:", error);
      const errorMessage: Message = {
        id: (Date.now() + 2).toString(),
        text: "워크플로우 실행에 실패했습니다. 다시 시도해주세요.",
        sender: "bot",
        timestamp: new Date(),
      };

      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === botMessage.id
            ? { ...msg, text: errorMessage.text, isExecuting: false }
            : msg
        )
      );
      setIsExecuting(false);
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  const clearChat = () => {
    setMessages([
      {
        id: "1",
        text: `안녕하세요! "${workflowName}" 워크플로우를 테스트해보세요. 메시지를 입력하면 워크플로우가 실행됩니다.`,
        sender: "bot",
        timestamp: new Date(),
      },
    ]);
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="md"
      fullWidth
      PaperProps={{
        sx: { height: "80vh" },
      }}
    >
      <DialogTitle sx={{ display: "flex", alignItems: "center", gap: 1 }}>
        <ChatIcon color="primary" />
        <Typography variant="h6">워크플로우 채팅 테스트</Typography>
        <Chip
          label={workflowName}
          size="small"
          color="primary"
          variant="outlined"
        />
        <Box sx={{ flexGrow: 1 }} />
        <IconButton onClick={onClose} size="small">
          <CloseIcon />
        </IconButton>
      </DialogTitle>

      <DialogContent sx={{ p: 0, display: "flex", flexDirection: "column" }}>
        <Box
          sx={{
            flex: 1,
            overflow: "auto",
            p: 2,
            display: "flex",
            flexDirection: "column",
            gap: 1,
          }}
        >
          {messages.map((message) => (
            <Paper
              key={message.id}
              elevation={1}
              sx={{
                p: 2,
                maxWidth: "80%",
                alignSelf:
                  message.sender === "user" ? "flex-end" : "flex-start",
                bgcolor:
                  message.sender === "user" ? "primary.light" : "grey.100",
                color:
                  message.sender === "user"
                    ? "primary.contrastText"
                    : "text.primary",
              }}
            >
              <Box
                sx={{ display: "flex", alignItems: "center", gap: 1, mb: 1 }}
              >
                <Typography variant="caption" sx={{ fontWeight: "bold" }}>
                  {message.sender === "user" ? "사용자" : "봇"}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {message.timestamp.toLocaleTimeString()}
                </Typography>
                {message.isExecuting && (
                  <CircularProgress size={16} color="inherit" />
                )}
              </Box>
              <Typography
                variant="body2"
                sx={{
                  whiteSpace: "pre-wrap",
                  fontFamily:
                    message.sender === "bot" ? "monospace" : "inherit",
                }}
              >
                {message.text}
              </Typography>
            </Paper>
          ))}
          <div ref={messagesEndRef} />
        </Box>

        <Box sx={{ p: 2, borderTop: 1, borderColor: "divider" }}>
          <Box sx={{ display: "flex", gap: 1, alignItems: "flex-end" }}>
            <TextField
              fullWidth
              multiline
              maxRows={3}
              placeholder="메시지를 입력하세요... (Enter로 전송, Shift+Enter로 줄바꿈)"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={isExecuting}
              variant="outlined"
              size="small"
            />
            <Button
              variant="contained"
              onClick={handleSendMessage}
              disabled={!inputText.trim() || isExecuting}
              startIcon={<SendIcon />}
              sx={{ minWidth: "80px", px: 2, whiteSpace: "nowrap" }}
            >
              전송
            </Button>
          </Box>
        </Box>
      </DialogContent>

      <DialogActions sx={{ p: 2, borderTop: 1, borderColor: "divider" }}>
        <Button onClick={clearChat} color="secondary">
          채팅 초기화
        </Button>
        <Button onClick={onClose} variant="contained">
          닫기
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ChatModal;

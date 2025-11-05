import React, { useState, useEffect } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  Typography,
  Paper,
  IconButton,
  CircularProgress,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Alert,
  Tabs,
  Tab,
  TextField,
  InputAdornment,
} from "@mui/material";
import {
  Close as CloseIcon,
  History as HistoryIcon,
  CheckCircle as SuccessIcon,
  Error as ErrorIcon,
  Schedule as PendingIcon,
  Cancel as CancelledIcon,
  Search as SearchIcon,
  Refresh as RefreshIcon,
} from "@mui/icons-material";
// import { workflowApi } from "../../../services/workflow/api";

interface ExecutionLog {
  id: number;
  workflow_id: number;
  status: "pending" | "running" | "completed" | "failed" | "cancelled";
  started_at: string;
  completed_at?: string;
  result?: any;
  error_message?: string;
  execution_data?: any;
}

interface LogModalProps {
  open: boolean;
  onClose: () => void;
  workflowId: number;
  workflowName: string;
}

const LogModal: React.FC<LogModalProps> = ({
  open,
  onClose,
  workflowId,
  workflowName,
}) => {
  const [logs, setLogs] = useState<ExecutionLog[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedTab, setSelectedTab] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [selectedLog, setSelectedLog] = useState<ExecutionLog | null>(null);

  // 예시 로그 데이터 생성
  const generateMockLogs = (): ExecutionLog[] => {
    const now = new Date();
    const mockLogs: ExecutionLog[] = [
      {
        id: 1001,
        workflow_id: workflowId,
        status: "completed",
        started_at: new Date(now.getTime() - 5 * 60 * 1000).toISOString(), // 5분 전
        completed_at: new Date(now.getTime() - 4 * 60 * 1000).toISOString(), // 4분 전
        result: {
          success: true,
          message: "워크플로우가 성공적으로 실행되었습니다.",
          data: {
            processed_items: 25,
            total_time: "2.3초",
            output_file: "result_20241201_143022.json",
          },
        },
        execution_data: {
          trigger_type: "manual",
          input_data: {
            user_id: "user123",
            request_type: "data_processing",
          },
        },
      },
      {
        id: 1002,
        workflow_id: workflowId,
        status: "failed",
        started_at: new Date(now.getTime() - 15 * 60 * 1000).toISOString(), // 15분 전
        completed_at: new Date(now.getTime() - 14 * 60 * 1000).toISOString(), // 14분 전
        error_message:
          "API 연결 시간 초과: 외부 서비스에 30초 이상 응답이 없습니다. 네트워크 상태를 확인해주세요.",
        execution_data: {
          trigger_type: "webhook",
          input_data: {
            webhook_id: "wh_abc123",
            payload: { action: "process_data", items: [1, 2, 3] },
          },
        },
      },
      {
        id: 1003,
        workflow_id: workflowId,
        status: "running",
        started_at: new Date(now.getTime() - 2 * 60 * 1000).toISOString(), // 2분 전
        execution_data: {
          trigger_type: "schedule",
          input_data: {
            schedule_id: "daily_backup",
            timestamp: now.toISOString(),
          },
        },
      },
      {
        id: 1004,
        workflow_id: workflowId,
        status: "completed",
        started_at: new Date(now.getTime() - 30 * 60 * 1000).toISOString(), // 30분 전
        completed_at: new Date(now.getTime() - 29 * 60 * 1000).toISOString(), // 29분 전
        result: {
          success: true,
          message: "데이터 백업이 완료되었습니다.",
          data: {
            backup_size: "2.4GB",
            files_processed: 1250,
            backup_location: "/backups/2024-12-01_14-00-00.tar.gz",
          },
        },
        execution_data: {
          trigger_type: "schedule",
          input_data: {
            schedule_id: "daily_backup",
            backup_type: "full",
          },
        },
      },
      {
        id: 1005,
        workflow_id: workflowId,
        status: "failed",
        started_at: new Date(now.getTime() - 45 * 60 * 1000).toISOString(), // 45분 전
        completed_at: new Date(now.getTime() - 44 * 60 * 1000).toISOString(), // 44분 전
        error_message:
          "인증 실패: API 키가 유효하지 않습니다. 설정을 확인해주세요.",
        execution_data: {
          trigger_type: "manual",
          input_data: {
            user_id: "user456",
            api_key: "sk-***",
          },
        },
      },
      {
        id: 1006,
        workflow_id: workflowId,
        status: "completed",
        started_at: new Date(now.getTime() - 60 * 60 * 1000).toISOString(), // 1시간 전
        completed_at: new Date(now.getTime() - 59 * 60 * 1000).toISOString(), // 59분 전
        result: {
          success: true,
          message: "이메일 발송이 완료되었습니다.",
          data: {
            emails_sent: 150,
            failed_emails: 2,
            delivery_time: "1.8초",
          },
        },
        execution_data: {
          trigger_type: "webhook",
          input_data: {
            webhook_id: "wh_email_campaign",
            campaign_id: "camp_20241201",
          },
        },
      },
      {
        id: 1007,
        workflow_id: workflowId,
        status: "cancelled",
        started_at: new Date(now.getTime() - 20 * 60 * 1000).toISOString(), // 20분 전
        completed_at: new Date(now.getTime() - 19 * 60 * 1000).toISOString(), // 19분 전
        error_message: "사용자에 의해 취소됨",
        execution_data: {
          trigger_type: "manual",
          input_data: {
            user_id: "user789",
            cancel_reason: "user_request",
          },
        },
      },
      {
        id: 1008,
        workflow_id: workflowId,
        status: "pending",
        started_at: new Date(now.getTime() - 1 * 60 * 1000).toISOString(), // 1분 전
        execution_data: {
          trigger_type: "schedule",
          input_data: {
            schedule_id: "hourly_sync",
            next_run: new Date(now.getTime() + 59 * 60 * 1000).toISOString(),
          },
        },
      },
    ];

    return mockLogs.sort(
      (a, b) =>
        new Date(b.started_at).getTime() - new Date(a.started_at).getTime()
    );
  };

  const loadLogs = async () => {
    try {
      setLoading(true);
      setError(null);

      // 실제 API 호출 대신 모킹된 데이터 사용
      // const response = await executionApi.getWorkflowExecutions(workflowId);
      // setLogs(response.data || []);

      // 모킹된 데이터 사용
      const mockLogs = generateMockLogs();
      setLogs(mockLogs);

      // 실제 API 호출 시뮬레이션을 위한 지연
      await new Promise((resolve) => setTimeout(resolve, 500));
    } catch (err) {
      console.error("Failed to load execution logs:", err);
      setError("실행 로그를 불러오는데 실패했습니다.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (open) {
      loadLogs();
    }
  }, [open, workflowId]);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "completed":
        return <SuccessIcon color="success" />;
      case "failed":
        return <ErrorIcon color="error" />;
      case "running":
        return <CircularProgress size={16} />;
      case "pending":
        return <PendingIcon color="warning" />;
      case "cancelled":
        return <CancelledIcon color="disabled" />;
      default:
        return <PendingIcon />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed":
        return "success";
      case "failed":
        return "error";
      case "running":
        return "info";
      case "pending":
        return "warning";
      case "cancelled":
        return "default";
      default:
        return "default";
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case "completed":
        return "완료";
      case "failed":
        return "실패";
      case "running":
        return "실행중";
      case "pending":
        return "대기중";
      case "cancelled":
        return "취소됨";
      default:
        return status;
    }
  };

  const formatDateTime = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString("ko-KR", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  };

  const getDuration = (startedAt: string, completedAt?: string) => {
    const start = new Date(startedAt);
    const end = completedAt ? new Date(completedAt) : new Date();
    const duration = end.getTime() - start.getTime();

    if (duration < 1000) {
      return `${duration}ms`;
    } else if (duration < 60000) {
      return `${Math.round(duration / 1000)}초`;
    } else {
      const minutes = Math.floor(duration / 60000);
      const seconds = Math.round((duration % 60000) / 1000);
      return `${minutes}분 ${seconds}초`;
    }
  };

  const filteredLogs = logs.filter((log) => {
    const matchesSearch =
      log.id.toString().includes(searchTerm) ||
      log.status.includes(searchTerm) ||
      (log.error_message && log.error_message.includes(searchTerm)) ||
      (log.result && JSON.stringify(log.result).includes(searchTerm));

    if (selectedTab === 0) return matchesSearch; // All
    if (selectedTab === 1) return matchesSearch && log.status === "completed";
    if (selectedTab === 2) return matchesSearch && log.status === "failed";
    if (selectedTab === 3)
      return (
        matchesSearch && (log.status === "running" || log.status === "pending")
      );

    return matchesSearch;
  });

  const renderLogDetails = (log: ExecutionLog) => (
    <Box sx={{ mt: 2 }}>
      <Typography variant="h6" gutterBottom>
        실행 상세 정보 (ID: {log.id})
      </Typography>

      <Box
        sx={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 2, mb: 2 }}
      >
        <Paper sx={{ p: 2 }}>
          <Typography variant="subtitle2" color="text.secondary" gutterBottom>
            시작 시간
          </Typography>
          <Typography variant="body2">
            {formatDateTime(log.started_at)}
          </Typography>
        </Paper>

        <Paper sx={{ p: 2 }}>
          <Typography variant="subtitle2" color="text.secondary" gutterBottom>
            완료 시간
          </Typography>
          <Typography variant="body2">
            {log.completed_at ? formatDateTime(log.completed_at) : "진행중"}
          </Typography>
        </Paper>

        <Paper sx={{ p: 2 }}>
          <Typography variant="subtitle2" color="text.secondary" gutterBottom>
            실행 시간
          </Typography>
          <Typography variant="body2">
            {getDuration(log.started_at, log.completed_at)}
          </Typography>
        </Paper>

        <Paper sx={{ p: 2 }}>
          <Typography variant="subtitle2" color="text.secondary" gutterBottom>
            상태
          </Typography>
          <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
            {getStatusIcon(log.status)}
            <Typography variant="body2">{getStatusText(log.status)}</Typography>
          </Box>
        </Paper>
      </Box>

      {log.error_message && (
        <Paper
          sx={{
            p: 2,
            mb: 2,
            bgcolor: "error.light",
            color: "error.contrastText",
          }}
        >
          <Typography variant="subtitle2" gutterBottom>
            오류 메시지
          </Typography>
          <Typography
            variant="body2"
            sx={{ fontFamily: "monospace", whiteSpace: "pre-wrap" }}
          >
            {log.error_message}
          </Typography>
        </Paper>
      )}

      {log.result && (
        <Paper sx={{ p: 2, mb: 2 }}>
          <Typography variant="subtitle2" gutterBottom>
            실행 결과
          </Typography>
          <Typography
            variant="body2"
            sx={{
              fontFamily: "monospace",
              whiteSpace: "pre-wrap",
              bgcolor: "grey.100",
              p: 1,
              borderRadius: 1,
              overflow: "auto",
              maxHeight: 200,
            }}
          >
            {JSON.stringify(log.result, null, 2)}
          </Typography>
        </Paper>
      )}

      {log.execution_data && (
        <Paper sx={{ p: 2 }}>
          <Typography variant="subtitle2" gutterBottom>
            실행 데이터
          </Typography>
          <Typography
            variant="body2"
            sx={{
              fontFamily: "monospace",
              whiteSpace: "pre-wrap",
              bgcolor: "grey.100",
              p: 1,
              borderRadius: 1,
              overflow: "auto",
              maxHeight: 200,
            }}
          >
            {JSON.stringify(log.execution_data, null, 2)}
          </Typography>
        </Paper>
      )}
    </Box>
  );

  return (
    <>
      <Dialog
        open={open}
        onClose={onClose}
        maxWidth="lg"
        fullWidth
        PaperProps={{
          sx: { height: "90vh" },
        }}
      >
        <DialogTitle sx={{ display: "flex", alignItems: "center", gap: 1 }}>
          <HistoryIcon color="primary" />
          <Typography variant="h6">실행 로그</Typography>
          <Chip
            label={workflowName}
            size="small"
            color="primary"
            variant="outlined"
          />
          <Box sx={{ flexGrow: 1 }} />
          <IconButton onClick={loadLogs} size="small" disabled={loading}>
            <RefreshIcon />
          </IconButton>
          <IconButton onClick={onClose} size="small">
            <CloseIcon />
          </IconButton>
        </DialogTitle>

        <DialogContent sx={{ p: 0, display: "flex", flexDirection: "column" }}>
          <Box sx={{ p: 2, borderBottom: 1, borderColor: "divider" }}>
            <Box sx={{ display: "flex", gap: 2, alignItems: "center", mb: 2 }}>
              <TextField
                size="small"
                placeholder="로그 검색..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon />
                    </InputAdornment>
                  ),
                }}
                sx={{ flexGrow: 1 }}
              />
            </Box>

            <Tabs
              value={selectedTab}
              onChange={(_, newValue) => setSelectedTab(newValue)}
              sx={{ borderBottom: 1, borderColor: "divider" }}
            >
              <Tab label={`전체 (${logs.length})`} />
              <Tab
                label={`성공 (${
                  logs.filter((l) => l.status === "completed").length
                })`}
              />
              <Tab
                label={`실패 (${
                  logs.filter((l) => l.status === "failed").length
                })`}
              />
              <Tab
                label={`진행중 (${
                  logs.filter(
                    (l) => l.status === "running" || l.status === "pending"
                  ).length
                })`}
              />
            </Tabs>
          </Box>

          <Box sx={{ flex: 1, overflow: "auto", p: 2 }}>
            {loading ? (
              <Box sx={{ display: "flex", justifyContent: "center", p: 4 }}>
                <CircularProgress />
              </Box>
            ) : error ? (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            ) : filteredLogs.length === 0 ? (
              <Alert severity="info">
                {searchTerm ? "검색 결과가 없습니다." : "실행 로그가 없습니다."}
              </Alert>
            ) : (
              <TableContainer component={Paper} variant="outlined">
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>ID</TableCell>
                      <TableCell>상태</TableCell>
                      <TableCell>시작 시간</TableCell>
                      <TableCell>완료 시간</TableCell>
                      <TableCell>실행 시간</TableCell>
                      <TableCell>오류</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {filteredLogs.map((log) => (
                      <TableRow
                        key={log.id}
                        hover
                        onClick={() => setSelectedLog(log)}
                        sx={{ cursor: "pointer" }}
                      >
                        <TableCell>
                          <Typography variant="body2" fontWeight="bold">
                            #{log.id}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Box
                            sx={{
                              display: "flex",
                              alignItems: "center",
                              gap: 1,
                            }}
                          >
                            {getStatusIcon(log.status)}
                            <Chip
                              label={getStatusText(log.status)}
                              size="small"
                              color={getStatusColor(log.status)}
                              variant="outlined"
                            />
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">
                            {formatDateTime(log.started_at)}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">
                            {log.completed_at
                              ? formatDateTime(log.completed_at)
                              : "-"}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">
                            {getDuration(log.started_at, log.completed_at)}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          {log.error_message ? (
                            <Typography
                              variant="body2"
                              color="error"
                              sx={{
                                maxWidth: 200,
                                overflow: "hidden",
                                textOverflow: "ellipsis",
                                whiteSpace: "nowrap",
                              }}
                              title={log.error_message}
                            >
                              {log.error_message}
                            </Typography>
                          ) : (
                            "-"
                          )}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            )}
          </Box>
        </DialogContent>

        <DialogActions sx={{ p: 2, borderTop: 1, borderColor: "divider" }}>
          <Button
            onClick={loadLogs}
            startIcon={<RefreshIcon />}
            disabled={loading}
          >
            새로고침
          </Button>
          <Button onClick={onClose} variant="contained">
            닫기
          </Button>
        </DialogActions>
      </Dialog>

      {selectedLog && (
        <Dialog
          open={Boolean(selectedLog)}
          onClose={() => setSelectedLog(null)}
          maxWidth="md"
          fullWidth
        >
          <DialogTitle sx={{ display: "flex", alignItems: "center", gap: 1 }}>
            <HistoryIcon color="primary" />
            <Typography variant="h6">
              로그 상세 (ID: {selectedLog.id})
            </Typography>
            <Box sx={{ flexGrow: 1 }} />
            <Chip
              label={getStatusText(selectedLog.status)}
              size="small"
              color={getStatusColor(selectedLog.status)}
              variant="outlined"
            />
            <IconButton onClick={() => setSelectedLog(null)} size="small">
              <CloseIcon />
            </IconButton>
          </DialogTitle>
          <DialogContent dividers>
            {renderLogDetails(selectedLog)}
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setSelectedLog(null)} variant="contained">
              닫기
            </Button>
          </DialogActions>
        </Dialog>
      )}
    </>
  );
};

export default LogModal;

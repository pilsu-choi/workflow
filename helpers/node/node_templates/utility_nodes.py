import json
import time
from typing import Any, Dict

import requests  # type: ignore

from helpers.node.node_base import BaseNode, NodeInputOutput, NodeInputOutputType
from setting.logger import get_logger

logger = get_logger(__name__)


class DelayNode(BaseNode):
    """지연 노드"""

    def __init__(self, node_id: str, properties: Dict[str, Any]):
        super().__init__(node_id, properties)
        self.inputs = [
            NodeInputOutput(
                name="delay_seconds",
                type=NodeInputOutputType.NUMBER,
                description="지연 시간(초)",
                value=1,
            )
        ]
        self.outputs = [
            NodeInputOutput(
                name="output",
                type=NodeInputOutputType.TEXT,
                description="지연 후 출력",
            )
        ]

    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        delay_seconds = inputs.get("delay_seconds", 1)
        time.sleep(delay_seconds)
        return {"output": f"지연 {delay_seconds}초 완료"}

    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        delay_seconds = inputs.get("delay_seconds", 1)
        return isinstance(delay_seconds, (int, float)) and delay_seconds >= 0


class WebhookNode(BaseNode):
    """웹훅 노드"""

    def __init__(self, node_id: str, properties: Dict[str, Any]):
        super().__init__(node_id, properties)
        self.inputs = [
            NodeInputOutput(
                name="url", type=NodeInputOutputType.TEXT, description="웹훅 URL"
            ),
            NodeInputOutput(
                name="method",
                type=NodeInputOutputType.TEXT,
                description="HTTP 메서드",
                value="POST",
            ),
            NodeInputOutput(
                name="headers",
                type=NodeInputOutputType.JSON,
                description="HTTP 헤더",
                required=False,
            ),
            NodeInputOutput(
                name="data",
                type=NodeInputOutputType.JSON,
                description="전송할 데이터",
                required=False,
            ),
        ]
        self.outputs = [
            NodeInputOutput(
                name="response",
                type=NodeInputOutputType.JSON,
                description="웹훅 응답",
            ),
            NodeInputOutput(
                name="status_code",
                type=NodeInputOutputType.NUMBER,
                description="HTTP 상태 코드",
            ),
        ]

    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        url = inputs.get("url")
        method = inputs.get("method", "POST").upper()
        headers = inputs.get("headers", {})
        data = inputs.get("data", {})

        if not url:
            raise ValueError("웹훅 URL이 필요합니다")

        try:
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == "PUT":
                response = requests.put(url, json=data, headers=headers, timeout=30)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=30)
            else:
                raise ValueError(f"지원하지 않는 HTTP 메서드: {method}")

            response.raise_for_status()

            try:
                response_data = response.json()
            except Exception as e:
                logger.error(f"웹훅 응답 파싱 실패: {e}", exc_info=True)
                response_data = response.text

            return {"response": response_data, "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            raise Exception(f"웹훅 호출 실패: {str(e)}")

    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        return "url" in inputs and inputs["url"]


# class MergeNode(BaseNode):
#     """데이터 병합 노드"""

#     def __init__(self, node_id: str, properties: Dict[str, Any]):
#         super().__init__(node_id, properties)
#         self.inputs = [
#             NodeInputOutput(
#                 name="input1",
#                 type=NodeInputOutputType.JSON,
#                 description="첫 번째 입력",
#                 required=False,
#             ),
#             NodeInputOutput(
#                 name="input2",
#                 type=NodeInputOutputType.JSON,
#                 description="두 번째 입력",
#                 required=False,
#             ),
#             NodeInputOutput(
#                 name="input3",
#                 type=NodeInputOutputType.JSON,
#                 description="세 번째 입력",
#                 required=False,
#             ),
#             NodeInputOutput(
#                 name="merge_strategy",
#                 type=NodeInputOutputType.TEXT,
#                 description="병합 전략",
#                 value="merge",
#             ),
#         ]
#         self.outputs = [
#             NodeInputOutput(
#                 name="merged_data",
#                 type=NodeInputOutputType.JSON,
#                 description="병합된 데이터",
#             )
#         ]

#     def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
#         merge_strategy = inputs.get("merge_strategy", "merge")

#         # 모든 입력 수집
#         all_inputs = []
#         for key, value in inputs.items():
#             if key.startswith("input") and value is not None:
#                 all_inputs.append(value)

#         if merge_strategy == "merge":
#             # 딕셔너리 병합
#             merged = {}
#             for input_data in all_inputs:
#                 if isinstance(input_data, dict):
#                     merged.update(input_data)
#                 else:
#                     merged[f"input_{len(merged)}"] = input_data
#         elif merge_strategy == "array":
#             # 배열로 병합
#             merged = all_inputs
#         elif merge_strategy == "concat":
#             # 문자열 연결
#             merged = " ".join(str(input_data) for input_data in all_inputs)
#         else:
#             merged = all_inputs

#         return {"merged_data": merged}

#     def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
#         return True  # 모든 입력이 선택사항


class SplitNode(BaseNode):
    """데이터 분할 노드"""

    def __init__(self, node_id: str, properties: Dict[str, Any]):
        super().__init__(node_id, properties)
        self.inputs = [
            NodeInputOutput(
                name="data",
                type=NodeInputOutputType.TEXT,
                description="분할할 데이터",
            ),
            NodeInputOutput(
                name="separator",
                type=NodeInputOutputType.TEXT,
                description="구분자",
                value=",",
            ),
            NodeInputOutput(
                name="max_splits",
                type=NodeInputOutputType.NUMBER,
                description="최대 분할 수",
                required=False,
            ),
        ]
        self.outputs = [
            NodeInputOutput(
                name="split_data",
                type=NodeInputOutputType.ARRAY,
                description="분할된 데이터 배열",
            )
        ]

    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        data = inputs.get("data", "")
        separator = inputs.get("separator", ",")
        max_splits = inputs.get("max_splits")

        if max_splits:
            split_data = data.split(separator, max_splits)
        else:
            split_data = data.split(separator)

        return {"split_data": split_data}

    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        return "data" in inputs and inputs["data"]


class TextOutputNode(BaseNode):
    """텍스트 출력 노드"""

    def __init__(self, node_id: str, properties: Dict[str, Any]):
        super().__init__(node_id, properties)
        self.inputs = [
            NodeInputOutput(
                name="text",
                type=NodeInputOutputType.TEXT,
                description="출력할 텍스트",
            )
        ]
        self.outputs = [
            NodeInputOutput(
                name="output",
                type=NodeInputOutputType.TEXT,
                description="출력된 텍스트",
            )
        ]

    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        text = inputs.get("text", "")
        # 실제 구현에서는 파일 저장, 로깅, API 응답 등으로 출력
        print("Text Output: ", text)
        return {"output": text}

    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        return "text" in inputs


class JSONOutputNode(BaseNode):
    """JSON 출력 노드"""

    def __init__(self, node_id: str, properties: Dict[str, Any]):
        super().__init__(node_id, properties)
        self.inputs = [
            NodeInputOutput(
                name="data",
                type=NodeInputOutputType.JSON,
                description="출력할 JSON 데이터",
            )
        ]
        self.outputs = [
            NodeInputOutput(
                name="output",
                type=NodeInputOutputType.JSON,
                description="출력된 JSON 데이터",
            )
        ]

    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        data = inputs.get("data", {})
        # 실제 구현에서는 파일 저장, 로깅, API 응답 등으로 출력
        print(f"JSON Output: {json.dumps(data, ensure_ascii=False, indent=2)}")
        return {"output": data}

    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        return "data" in inputs

from typing import Any, Dict

from helpers.node.node_base import BaseNode, NodeInputOutput, NodeInputOutputType
from setting.logger import get_logger

logger = get_logger(__name__)


class ConditionNode(BaseNode):
    """조건문 노드"""

    def __init__(self, node_id: str, properties: Dict[str, Any]):
        super().__init__(node_id, properties)
        self.inputs = [
            NodeInputOutput(
                name="condition",
                type=NodeInputOutputType.TEXT,
                description="조건식",
                required=False,  # properties에서 가져올 수 있으므로 optional
            ),
            NodeInputOutput(
                name="value",
                type=NodeInputOutputType.TEXT,
                description="비교할 값",
            ),
        ]
        self.outputs = [
            NodeInputOutput(
                name="true",
                type=NodeInputOutputType.BOOLEAN,
                description="조건이 참일 때",
            ),
            NodeInputOutput(
                name="false",
                type=NodeInputOutputType.BOOLEAN,
                description="조건이 거짓일 때",
            ),
        ]

    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        self.params = inputs

        # condition은 inputs나 properties에서 가져오기
        condition = inputs.get("condition") or self.properties.get("condition", "")
        value = inputs.get("value", "")

        # 간단한 조건 평가 (실제로는 더 복잡한 파싱 필요)
        try:
            if not condition:
                # condition이 비어있으면 항상 True 반환
                logger.warning("조건식이 비어있습니다. True를 반환합니다.")
                return {"true": True, "false": False}

            # condition의 "value"를 실제 값으로 치환
            # 예: "value == 'admin'" -> "user123 == 'admin'" (value가 "user123"인 경우)
            # 또는 'value == 'admin'' -> 'admin == 'admin'' (value가 "admin"인 경우)
            evaluated_condition = condition.replace("value", repr(value))
            result = eval(evaluated_condition)

            logger.info(f"조건 평가: {condition}, 값: {value}, 결과: {result}")
            return {"true": result, "false": not result}
        except Exception as e:
            logger.error(f"조건문 실행 실패: {e}", exc_info=True)
            return {"true": False, "false": True}

    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """
        현재는 부모 클래스의 default method 이용하여 inputs 검증 진행. 필요시 override.
        """
        return super().validate_inputs(inputs)

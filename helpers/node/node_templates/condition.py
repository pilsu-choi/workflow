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
        # operator는 properties에서, value는 inputs에서 가져오기
        operator = self.properties.get("config", {}).get(
            "operator", ""
        )  # equal, not_equal, greater_than, less_than, greater_equal, less_equal
        compare_value = self.properties.get("config", {}).get("compare_value", "")

        # inputs에서 실제 비교할 값 가져오기
        input_value = inputs.get("value", "")

        # 간단한 조건 평가
        try:
            if not operator:
                # operator가 비어있으면 항상 True 반환
                logger.warning("조건식이 비어있습니다. True를 반환합니다.")
                return {"true": True, "false": False}

            # operator에 따라 비교 수행
            result = False
            if operator == "equal" or operator == "==":
                result = input_value == compare_value
            elif operator == "not_equal" or operator == "!=":
                result = input_value != compare_value
            elif operator == "greater_than" or operator == ">":
                result = float(input_value) > float(compare_value)
            elif operator == "less_than" or operator == "<":
                result = float(input_value) < float(compare_value)
            elif operator == "greater_equal" or operator == ">=":
                result = float(input_value) >= float(compare_value)
            elif operator == "less_equal" or operator == "<=":
                result = float(input_value) <= float(compare_value)
            else:
                logger.warning(f"알 수 없는 operator: {operator}, False를 반환합니다.")
                result = False

            logger.info(
                f"조건 평가: {input_value} {operator} {compare_value}, 결과: {result}"
            )
            return {"true": result, "false": not result}
        except (ValueError, TypeError) as e:
            logger.error(f"조건문 실행 실패 (비교 불가능한 값): {e}", exc_info=True)
            return {"true": False, "false": True}
        except Exception as e:
            logger.error(f"조건문 실행 실패: {e}", exc_info=True)
            return {"true": False, "false": True}

    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """
        현재는 부모 클래스의 default method 이용하여 inputs 검증 진행. 필요시 override.
        """
        return super().validate_inputs(inputs)

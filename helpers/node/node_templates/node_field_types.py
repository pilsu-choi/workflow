"""
노드 필드 스키마 타입 정의 모듈 (Level 1 - 하위)

역할:
- 프론트엔드 UI 렌더링을 위한 필드 정의 타입 제공
- 노드 프로퍼티 설정 폼의 메타데이터 구조 정의
- "어떤 설정 필드를 어떻게 보여줄지" 정의

특징:
- 순수 타입 정의만 포함 (Pydantic BaseModel)
- 노드 구현체에 대한 의존성 없음
- 프론트엔드-백엔드 인터페이스 계약 역할

사용처:
- 각 노드 클래스의 get_properties_schema() 반환 타입
- API 응답으로 프론트엔드에 전달
- 프론트엔드에서 동적 폼 생성에 사용

의존성 계층:
  node_type.py
       ↓
  node_field_types.py (현재 파일)
       ↓
  node 구현체들 (llm.py, condition.py 등)
       ↓
  node_template_types.py
"""

from typing import List, Union

from pydantic import BaseModel, ConfigDict, Field


class FieldOption(BaseModel):
    """
    필드 옵션 정의 (select, radio 등에 사용)

    예시:
        FieldOption(value="openai", label="OpenAI")
        → 프론트엔드에서 드롭다운 옵션으로 표시
    """

    value: str = Field(description="옵션 값")
    label: str = Field(description="옵션 표시 라벨")


class NodeField(BaseModel):
    """
    개별 노드 설정 필드 정의

    프론트엔드에서 이 정보를 기반으로 입력 필드를 동적 생성

    필드 타입 예시:
        - "select": 드롭다운 선택
        - "textarea": 여러 줄 텍스트 입력
        - "text": 한 줄 텍스트 입력
        - "password": 비밀번호 입력
        - "number": 숫자 입력
        - "keyvalue": Key-Value 쌍 입력
        - "model_select": 모델 선택 (provider에 따라 동적 변경)

    조건부 표시:
        - show_if: 다른 필드 값에 따라 표시/숨김
        - depends_on: 다른 필드에 의존적인 옵션
    """

    name: str = Field(description="필드 이름")
    type: str = Field(
        description="필드 타입 (select, model_select, password, textarea, text, keyvalue, number)"
    )
    required: bool = Field(default=False, description="필수 입력 여부")
    default: Union[str, int, float, bool, None] = Field(
        default=None, description="기본값"
    )
    options: List[Union[str, FieldOption]] = Field(
        default_factory=list, description="선택 옵션 목록 (select 타입에 사용)"
    )
    depends_on: str | None = Field(
        default=None, description="의존하는 다른 필드 이름. 필드는 항상 표시."
    )
    placeholder: str | None = Field(
        default=None, description="입력 필드 플레이스홀더 텍스트"
    )
    # rows: int | None = Field(default=None, description="textarea 필드의 행 수")
    show_if: str | None = Field(
        default=None,
        description="조건부 표시 조건 (예: 'operation_type == extract_value')",
    )
    helper_text: str | None = Field(default=None, description="필드 설명 도움말 텍스트")
    # min: int | None = Field(default=None, description="number 타입의 최소값")
    # max: int | None = Field(default=None, description="number 타입의 최대값")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "provider",
                "type": "select",
                "required": True,
                "default": "openai",
                "options": ["openai", "anthropic", "google"],
            }
        }
    )


class NodeFieldsDefinition(BaseModel):
    """
    특정 노드 타입의 전체 필드 정의

    노드 클래스의 get_properties_schema() 메서드가 반환하는 타입

    예시:
        NodeFieldsDefinition(
            fields=[
                NodeField(name="provider", type="select", ...),
                NodeField(name="api_key", type="password", ...)
            ]
        )

    필드가 없는 노드의 경우:
        NodeFieldsDefinition(
            fields=[],
            info="No additional configuration required."
        )
    """

    fields: List[NodeField] = Field(description="노드 필드 목록")
    info: str | None = Field(
        default=None, description="추가 정보 (필드가 없는 노드의 경우)"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "fields": [
                    {
                        "name": "provider",
                        "type": "select",
                        "required": True,
                        "default": "openai",
                        "options": ["openai", "anthropic", "google"],
                    }
                ]
            }
        }
    )

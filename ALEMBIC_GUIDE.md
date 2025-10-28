# Alembic 사용 가이드

이 프로젝트에서 Alembic을 사용하여 데이터베이스 마이그레이션을 관리합니다.

## 설정 완료된 내용

1. **alembic.ini**: 데이터베이스 URL 설정 (PostgreSQL)
2. **alembic/env.py**: SQLModel 모델들 자동 import 설정
3. **초기 마이그레이션**: 기존 테이블 구조 반영

## 주요 명령어

### 마이그레이션 생성
```bash
# 자동으로 모델 변경사항 감지하여 마이그레이션 생성
uv run alembic revision --autogenerate -m "마이그레이션 설명"

# 수동으로 빈 마이그레이션 파일 생성
uv run alembic revision -m "마이그레이션 설명"
```

### 마이그레이션 실행
```bash
# 최신 마이그레이션까지 업그레이드
uv run alembic upgrade head

# 특정 마이그레이션까지 업그레이드
uv run alembic upgrade <revision_id>

# 한 단계씩 업그레이드
uv run alembic upgrade +1
```

### 마이그레이션 되돌리기
```bash
# 이전 마이그레이션으로 되돌리기
uv run alembic downgrade -1

# 특정 마이그레이션으로 되돌리기
uv run alembic downgrade <revision_id>

# 모든 마이그레이션 되돌리기
uv run alembic downgrade base
```

### 상태 확인
```bash
# 현재 마이그레이션 상태 확인
uv run alembic current

# 마이그레이션 히스토리 확인
uv run alembic history

# 사용 가능한 마이그레이션 목록
uv run alembic heads
```

## 모델 변경 시 워크플로우

1. **모델 수정**: `database/graph/` 폴더의 모델 파일들 수정
2. **마이그레이션 생성**: `uv run alembic revision --autogenerate -m "변경사항 설명"`
3. **마이그레이션 검토**: 생성된 마이그레이션 파일 확인 및 필요시 수정
4. **마이그레이션 실행**: `uv run alembic upgrade head`

## 주의사항

- 마이그레이션 실행 전에 항상 백업을 생성하세요
- 프로덕션 환경에서는 마이그레이션을 신중하게 검토하세요
- `--autogenerate`로 생성된 마이그레이션은 항상 검토 후 실행하세요

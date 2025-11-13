# 데이터베이스 마이그레이션 가이드

데이터베이스 스키마 변경을 쉽게 관리할 수 있는 스크립트들을 제공합니다.

## 📋 사용 가능한 스크립트

### 1. `db_migrate.sh` - 마이그레이션 관리 도구

일반적인 마이그레이션 작업을 위한 메인 스크립트입니다.

```bash
# 도움말 보기
./scripts/db_migrate.sh help

# 새 마이그레이션 생성 (자동 감지)
./scripts/db_migrate.sh create "add user email field"

# 모든 마이그레이션 적용
./scripts/db_migrate.sh upgrade

# 마이그레이션 1단계 되돌리기
./scripts/db_migrate.sh downgrade

# 마이그레이션 2단계 되돌리기
./scripts/db_migrate.sh downgrade 2

# 현재 마이그레이션 버전 확인
./scripts/db_migrate.sh current

# 마이그레이션 히스토리 보기
./scripts/db_migrate.sh history

# 전체 상태 보기
./scripts/db_migrate.sh status
```

### 2. `db_sync.sh` - 빠른 동기화 도구

모델 변경 후 빠르게 마이그레이션을 생성하고 적용할 수 있습니다.

```bash
# 기본 메시지로 동기화
./scripts/db_sync.sh

# 커스텀 메시지로 동기화
./scripts/db_sync.sh "add new columns to edges table"
```

이 스크립트는:
1. 현재 데이터베이스 버전을 표시
2. 자동으로 마이그레이션 생성
3. 적용 여부를 확인 (y/N)
4. 승인 시 즉시 적용

### 3. `db_reset.sh` - 데이터베이스 리셋

**⚠️ 주의: 모든 데이터가 삭제됩니다!**

```bash
# 데이터베이스를 초기 상태로 리셋
./scripts/db_reset.sh
```

이 스크립트는:
1. 모든 마이그레이션을 되돌림 (base로)
2. 처음부터 다시 마이그레이션 적용
3. 테스트/개발 환경에서만 사용 권장

## 🔄 일반적인 워크플로우

### 시나리오 1: 모델 필드 추가

1. **모델 수정**
   ```python
   # database/graph/edge.py
   class Edge(SQLModel, table=True):
       # ... 기존 필드들
       new_field: str = Field(default="")  # 새 필드 추가
   ```

2. **마이그레이션 생성 및 적용**
   ```bash
   ./scripts/db_sync.sh "add new_field to edges"
   # 또는
   ./scripts/db_migrate.sh create "add new_field to edges"
   ./scripts/db_migrate.sh upgrade
   ```

### 시나리오 2: 실수한 마이그레이션 되돌리기

```bash
# 1단계 되돌리기
./scripts/db_migrate.sh downgrade

# 문제 수정 후 다시 적용
./scripts/db_migrate.sh upgrade
```

### 시나리오 3: 현재 상태 확인

```bash
# 간단히 현재 버전만 확인
./scripts/db_migrate.sh current

# 전체 상태 확인
./scripts/db_migrate.sh status

# 상세 히스토리 확인
./scripts/db_migrate.sh history
```

## 📝 알아두면 좋은 팁

### 자동 생성된 마이그레이션 검토하기

`--autogenerate`로 생성된 마이그레이션은 항상 검토하세요:

```bash
# 마이그레이션 생성 후
cd alembic/versions
ls -lt | head -5  # 최신 파일 확인
# 에디터로 파일 열어서 내용 확인
```

### 마이그레이션 파일 위치

```
backend/alembic/versions/
├── b34c8fa0b414_initial_migration.py
├── 63fe39cad050_test_migration.py
├── 0db0b9cfb4f5_add_source_and_target_properties_to_.py
└── 52e9be1c1c00_remove_properties_column_from_edges_.py
```

### 프로덕션 환경 주의사항

1. **백업 필수**: 마이그레이션 전 반드시 데이터베이스 백업
2. **테스트**: 개발 환경에서 먼저 테스트
3. **다운타임**: 큰 변경사항은 다운타임 고려
4. **롤백 계획**: 문제 발생 시 롤백 계획 준비

## 🛠️ 트러블슈팅

### 문제: "No such table" 에러

```bash
# 데이터베이스 초기화
./scripts/db_reset.sh
```

### 문제: 마이그레이션 충돌

```bash
# 현재 상태 확인
./scripts/db_migrate.sh current

# 필요 시 되돌리기
./scripts/db_migrate.sh downgrade

# 또는 완전히 리셋
./scripts/db_reset.sh
```

### 문제: 자동 감지가 변경사항을 찾지 못함

`alembic/env.py`에 모델이 import 되어 있는지 확인:

```python
# Import all models to ensure they are registered with SQLModel
from database.graph.edge import Edge
from database.graph.graph import Graph
from database.graph.vertex import Vertex
```

## 🔗 추가 리소스

- [Alembic 공식 문서](https://alembic.sqlalchemy.org/)
- [SQLModel 문서](https://sqlmodel.tiangolo.com/)
- 프로젝트 내 `ALEMBIC_GUIDE.md` 참고


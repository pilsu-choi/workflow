# 데이터베이스 마이그레이션 스크립트

## 🚀 빠른 시작

### 가장 자주 사용하는 명령어

```bash
# 1. 모델 변경 후 자동 동기화 (추천!)
./scripts/db_sync.sh "설명"

# 2. 마이그레이션만 생성
./scripts/db_migrate.sh create "설명"

# 3. 마이그레이션 적용
./scripts/db_migrate.sh upgrade

# 4. 현재 상태 확인
./scripts/db_migrate.sh status
```

## 📚 스크립트 설명

### `db_sync.sh` - 빠른 동기화 (가장 많이 사용)
모델을 변경한 후 데이터베이스를 빠르게 동기화합니다.

```bash
./scripts/db_sync.sh "add email field to user"
```

### `db_migrate.sh` - 세밀한 제어
마이그레이션을 단계별로 제어할 수 있습니다.

```bash
# 생성
./scripts/db_migrate.sh create "migration message"

# 적용
./scripts/db_migrate.sh upgrade

# 되돌리기
./scripts/db_migrate.sh downgrade

# 상태 확인
./scripts/db_migrate.sh status
./scripts/db_migrate.sh current
./scripts/db_migrate.sh history
```

### `db_reset.sh` - 완전 초기화
⚠️ **위험**: 모든 데이터가 삭제됩니다!

```bash
./scripts/db_reset.sh
```

## 📖 더 자세한 내용

전체 가이드는 `DB_MIGRATION_GUIDE.md`를 참조하세요.


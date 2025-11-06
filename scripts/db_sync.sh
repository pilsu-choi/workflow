#!/bin/bash

# Quick Database Sync Script
# Automatically creates and applies migrations

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Change to backend directory
cd "$(dirname "$0")/.."

# Activate virtual environment
source .venv/bin/activate

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Get migration message from argument or use default
MESSAGE="${1:-auto sync models}"

echo ""
print_info "=== Database Sync Tool ==="
echo ""

# Show current status
print_info "Current database version:"
uv run alembic current
echo ""

# Create migration
print_info "Creating migration: $MESSAGE"
uv run alembic revision --autogenerate -m "$MESSAGE"
echo ""

# Ask for confirmation
print_info "Migration file created. Review it in alembic/versions/"
echo ""
read -p "Do you want to apply this migration now? (y/N) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "Applying migration..."
    uv run alembic upgrade head
    echo ""
    print_success "Database synced successfully!"
    echo ""
    print_info "New database version:"
    uv run alembic current
else
    print_info "Migration created but not applied"
    print_info "You can apply it later with: ./scripts/db_migrate.sh upgrade"
fi

echo ""


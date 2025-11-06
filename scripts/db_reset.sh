#!/bin/bash

# Database Reset Script
# WARNING: This will drop and recreate all tables!

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

print_warning() {
    echo -e "${RED}⚠ WARNING: $1${NC}"
}

echo ""
print_warning "This will RESET the database to the initial state!"
print_warning "All data will be LOST!"
echo ""
read -p "Are you sure you want to continue? (yes/NO) " -r
echo ""

if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    print_info "Database reset cancelled"
    exit 0
fi

# Downgrade to base (remove all migrations)
print_info "Rolling back all migrations..."
uv run alembic downgrade base
print_success "All migrations rolled back"
echo ""

# Upgrade to head (apply all migrations)
print_info "Applying all migrations from scratch..."
uv run alembic upgrade head
print_success "All migrations applied"
echo ""

print_success "Database reset completed!"
echo ""
print_info "Current database version:"
uv run alembic current
echo ""


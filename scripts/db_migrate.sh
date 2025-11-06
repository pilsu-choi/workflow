#!/bin/bash

# Database Migration Script
# Usage: ./scripts/db_migrate.sh [command] [options]

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

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Function to show usage
show_usage() {
    cat << EOF
Database Migration Script

Usage: ./scripts/db_migrate.sh [command] [options]

Commands:
    create <message>    Create a new migration with autogenerate
    upgrade             Apply all pending migrations (upgrade to head)
    downgrade [steps]   Rollback migrations (default: 1 step)
    current             Show current migration version
    history             Show migration history
    status              Show current status and pending migrations

Examples:
    ./scripts/db_migrate.sh create "add user table"
    ./scripts/db_migrate.sh upgrade
    ./scripts/db_migrate.sh downgrade
    ./scripts/db_migrate.sh downgrade 2
    ./scripts/db_migrate.sh current
    ./scripts/db_migrate.sh history
    ./scripts/db_migrate.sh status

EOF
}

# Main command handling
case "${1:-}" in
    create)
        if [ -z "$2" ]; then
            print_error "Migration message is required"
            echo "Usage: ./scripts/db_migrate.sh create \"migration message\""
            exit 1
        fi
        print_info "Creating new migration: $2"
        uv run alembic revision --autogenerate -m "$2"
        print_success "Migration created successfully"
        print_info "Please review the generated migration file before applying it"
        ;;
    
    upgrade)
        print_info "Applying all pending migrations..."
        uv run alembic upgrade head
        print_success "All migrations applied successfully"
        ;;
    
    downgrade)
        STEPS="${2:-1}"
        print_info "Rolling back $STEPS migration(s)..."
        uv run alembic downgrade -${STEPS}
        print_success "Rollback completed successfully"
        ;;
    
    current)
        print_info "Current migration version:"
        uv run alembic current
        ;;
    
    history)
        print_info "Migration history:"
        uv run alembic history --verbose
        ;;
    
    status)
        print_info "Current migration status:"
        echo ""
        echo "Current version:"
        uv run alembic current
        echo ""
        echo "Migration history:"
        uv run alembic history
        ;;
    
    help|--help|-h)
        show_usage
        ;;
    
    *)
        print_error "Unknown command: ${1:-}"
        echo ""
        show_usage
        exit 1
        ;;
esac


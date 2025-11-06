"""remove properties column from edges table

Revision ID: 52e9be1c1c00
Revises: 0db0b9cfb4f5
Create Date: 2025-10-28 15:17:09.655584

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op  # type: ignore

# revision identifiers, used by Alembic.
revision: str = "52e9be1c1c00"
down_revision: Union[str, Sequence[str], None] = "0db0b9cfb4f5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Remove properties column from edges table
    op.drop_column("edges", "properties")


def downgrade() -> None:
    """Downgrade schema."""
    # Add properties column back to edges table
    op.add_column(
        "edges",
        sa.Column(
            "properties",
            postgresql.JSON(astext_type=sa.Text()),
            autoincrement=False,
            nullable=False,
            server_default="{}",
        ),
    )

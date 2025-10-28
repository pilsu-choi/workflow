"""add_source_and_target_properties_to_edges

Revision ID: 0db0b9cfb4f5
Revises: 63fe39cad050
Create Date: 2025-10-27 15:32:06.468822

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op  # type: ignore

# revision identifiers, used by Alembic.
revision: str = "0db0b9cfb4f5"
down_revision: Union[str, Sequence[str], None] = "63fe39cad050"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add source_properties and target_properties columns to edges table
    op.add_column(
        "edges",
        sa.Column("source_properties", sa.JSON, nullable=True, server_default="{}"),
    )
    op.add_column(
        "edges",
        sa.Column("target_properties", sa.JSON, nullable=True, server_default="{}"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove source_properties and target_properties columns from edges table
    op.drop_column("edges", "source_properties")
    op.drop_column("edges", "target_properties")

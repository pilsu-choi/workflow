from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime
from sqlmodel import Field, SQLModel


class Edge(SQLModel, table=True):  # type: ignore
    __tablename__ = "edges"  # type: ignore
    id: int = Field(
        default=None, primary_key=True, sa_column_kwargs={"autoincrement": True}
    )
    graph_id: int = Field(foreign_key="graphs.id")
    source_id: int = Field(foreign_key="vertices.id")
    target_id: int = Field(foreign_key="vertices.id")
    type: str = Field(default=None)
    properties: dict = Field(default_factory=dict, sa_type=JSON)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
    )

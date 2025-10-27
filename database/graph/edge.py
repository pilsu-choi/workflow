from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import JSON, DateTime
from sqlmodel import Field, SQLModel

if TYPE_CHECKING:
    from helpers.node.node_base import NodeInputOutput


class Edge(SQLModel, table=True):  # type: ignore
    __tablename__ = "edges"  # type: ignore
    id: int = Field(
        default=None, primary_key=True, sa_column_kwargs={"autoincrement": True}
    )
    graph_id: int = Field(foreign_key="graphs.id")
    source_id: int = Field(foreign_key="vertices.id")
    target_id: int = Field(foreign_key="vertices.id")
    type: str = Field(default=None)
    source_properties: "NodeInputOutput" = Field(
        default_factory=dict,
        sa_type=JSON,
        description="Source Node의 output 포트",
    )
    target_properties: "NodeInputOutput" = Field(
        default_factory=dict,
        sa_type=JSON,
        description="Target Node의 input 포트",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
    )

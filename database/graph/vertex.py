from __future__ import annotations
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel
from sqlalchemy import JSON, DateTime


class Vertex(SQLModel, table=True):
    __tablename__ = "vertices"
    id: int = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    graph_id: int = Field(foreign_key="graphs.id")
    type: str = Field(default=None)
    properties: dict = Field(default_factory=dict, sa_type=JSON)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_type=DateTime(timezone=True))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_type=DateTime(timezone=True))

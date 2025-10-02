from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .edge import Edge


class Vertex(SQLModel):
    __tablename__ = "vertices"
    id: int = Field(default=None, primary_key=True)
    type: str = Field(default=None)
    properties: dict = Field(default_factory=dict)
    created_at: datetime = Field(default=None)
    updated_at: datetime = Field(default=None)

    outgoing_edges: list["Edge"] = Relationship(
        back_populates="source_vertex",
        sa_relationship_kwargs={"foreign_keys": "[Edge.source_id]"},
    )
    incoming_edges: list["Edge"] = Relationship(
        back_populates="target_vertex",
        sa_relationship_kwargs={"foreign_keys": "[Edge.target_id]"},
    )

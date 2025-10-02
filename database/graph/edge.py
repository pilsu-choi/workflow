from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .vertex import Vertex


class Edge(SQLModel):
    __tablename__ = "edges"
    id: int = Field(default=None, primary_key=True)
    source_id: int = Field(foreign_key="vertices.id")
    target_id: int = Field(foreign_key="vertices.id")
    type: str = Field(default=None)
    properties: dict = Field(default_factory=dict)
    created_at: datetime = Field(default=None)
    updated_at: datetime = Field(default=None)

    source_vertex: "Vertex" = Relationship(
        back_populates="outgoing_edges",
        sa_relationship_kwargs={"foreign_keys": "[Edge.source_id]"},
    )
    target_vertex: "Vertex" = Relationship(
        back_populates="incoming_edges",
        sa_relationship_kwargs={"foreign_keys": "[Edge.target_id]"},
    )

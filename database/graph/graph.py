from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.graph.edge import Edge
    from database.graph.vertex import Vertex


class Graph(SQLModel):
    __tablename__ = "graphs"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    description: str = Field(default=None)
    created_at: datetime = Field(default=None)
    updated_at: datetime = Field(default=None)
    vertices: list["Vertex"] = Relationship(back_populates="graph")
    edges: list["Edge"] = Relationship(back_populates="graph")

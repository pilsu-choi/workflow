from datetime import datetime, timezone
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import JSON, DateTime


class Graph(SQLModel, table=True):
    __tablename__ = "graphs"
    id: int = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    name: str = Field(default=None)
    description: str = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_type=DateTime(timezone=True))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_type=DateTime(timezone=True))
    properties: dict = Field(default_factory=dict, sa_type=JSON)

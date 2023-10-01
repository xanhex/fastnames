"""Pydantic models (schemas)."""
from pydantic import BaseModel, ConfigDict


class InitialNickname(BaseModel):
    """Initial schema for nickname."""

    name: str
    model_config = ConfigDict(from_attributes=True)


class Nickname(InitialNickname):
    """Schema for nickname after actual model creation."""

    id: int

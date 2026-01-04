"""Pydantic models for ExileNexus message contracts."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class EventType(str, Enum):
    """Event type enumeration for message classification."""

    AREA_ENTERED = "area_entered"
    AREA_LEFT = "area_left"
    ITEM_DROP = "item_drop"
    TRADE_RECEIVED = "trade_received"
    TRADE_ACCEPTED = "trade_accepted"
    CHAT_MESSAGE = "chat_message"
    DEATH = "death"
    LEVEL_UP = "level_up"
    CUSTOM = "custom"


class MessageHeader(BaseModel):
    """Message header containing metadata."""

    id: UUID = Field(default_factory=uuid4, description="Unique message identifier")
    source: str = Field(..., description="Source service identifier")
    event_type: EventType = Field(..., description="Type of event")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="ISO8601 timestamp"
    )
    priority: int = Field(default=0, ge=0, le=10, description="Message priority (0-10)")

    @field_validator("timestamp", mode="before")
    @classmethod
    def parse_timestamp(cls, v: Any) -> datetime:
        """Ensure timestamp is a datetime object."""
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        return v


class PoeMessage(BaseModel):
    """Complete message contract for Pub/Sub communication."""

    header: MessageHeader = Field(..., description="Message header with metadata")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Message payload data")

    def to_json(self) -> str:
        """Serialize message to JSON string."""
        return self.model_dump_json()

    @classmethod
    def from_json(cls, json_str: str) -> "PoeMessage":
        """Deserialize message from JSON string."""
        return cls.model_validate_json(json_str)

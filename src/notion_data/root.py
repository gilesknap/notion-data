"""
A base class for all Notion data classes.

Uses pydantic model and defines the common attributes for all Notion data
classes.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


def _format_datetime(date: datetime) -> str:
    return date.isoformat()


class Root(BaseModel):
    """A Base class for setting consistent Pydantic model configuration"""

    model_config = ConfigDict(
        extra="forbid", use_enum_values=True, json_encoders={datetime: _format_datetime}
    )


class PropertyRoot(Root):
    """A Base class for setting Page Properties which have dynamic keys"""

    model_config = ConfigDict(
        extra="allow", use_enum_values=True, json_encoders={datetime: _format_datetime}
    )

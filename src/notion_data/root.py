"""
A base class for all Notion data classes.

Uses pydantic model and defines the common attributes for all Notion data
classes.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


def format_datetime(date: datetime) -> str:
    if date is None:
        return None
    return date.isoformat()


CONFIG = ConfigDict(
    extra="forbid",
    use_enum_values=True,
    ser_json_timedelta="iso8601",
)


class Root(BaseModel):
    """A Base class for setting consistent Pydantic model configuration"""

    model_config = CONFIG

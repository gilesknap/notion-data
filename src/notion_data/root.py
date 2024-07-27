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


class Root(BaseModel):
    """A Base class for setting consistent Pydantic model configuration"""

    model_config = ConfigDict(
        extra="forbid",
        use_enum_values=True,
        ser_json_timedelta="iso8601",
        populate_by_name=True,
    )


def unset_none(model: BaseModel):
    """
    Strangely setting a field to None when None is its default causes the field
    to be registered in model_fields_set set. This in turn cause it to serialize
    with nil for each of those fields. This breaks the Notion API and here
    we 'un-set' any None fields to fix that..
    """
    remove = []
    for field in model.model_fields_set:
        if getattr(model, field) is None:
            remove.append(field)
    for field in remove:
        model.model_fields_set.remove(field)

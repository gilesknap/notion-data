"""
A base class for all Notion data classes.

Uses pydantic model and defines the common attributes for all Notion data
classes.
"""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, create_model
from pydantic.fields import Field


def format_datetime(date: datetime) -> str:
    if date is None:
        return None
    return date.isoformat()


class Root(BaseModel):
    """
    A Base class for setting consistent Pydantic model configuration
    and behavior.
    """

    model_config = ConfigDict(
        extra="forbid",
        use_enum_values=True,
        ser_json_timedelta="iso8601",
        populate_by_name=True,
    )
    # TODO put a global serializer here to handle all datetime fields


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


def dict_model_instance(name: str, dict_def: dict) -> Root:
    """
    Because database child pages have dynamic property names, we need to create
    a model at runtime for them
    """
    # replace spaces as they make illegal variable names - but really we need more
    # robust handling of this as other illegal characters are possible.
    aliased_dict = {key.replace(" ", "_"): value for key, value in dict_def.items()}
    fields = {
        key: Annotated[
            type(value),
            Field(
                description=key,
                alias=key.replace("_", " "),
            ),
        ]
        for key, value in aliased_dict.items()
    }

    model = create_model(name, **fields, __base__=Root)  # type: ignore
    instance = model(**dict_def)
    return instance

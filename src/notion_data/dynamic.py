from typing import Annotated

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo


def dict_model_instance(name: str, dict_def: dict) -> BaseModel:
    """
    Because database child pages have dynamic properties, we need to create
    a model at runtime for them
    """
    fields = {}
    for field_name, value in dict_def.items():
        fields[field_name] = Annotated[type(value), FieldInfo(description=field_name)]
    model = create_model(name, **fields)  # type: ignore
    return model(**dict_def)

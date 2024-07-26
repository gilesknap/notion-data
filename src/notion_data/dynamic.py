from typing import Annotated

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo

from .root import CONFIG


def dict_model_instance(name: str, dict_def: dict) -> BaseModel:
    """
    Because database child pages have dynamic property names, we need to create
    a model at runtime for them
    """
    # replace spaces as they make illegal field names - but really we need more
    # robust handling of this
    new_dict = {key.replace(" ", "_"): val for key, val in dict_def.items()}
    fields = {
        key.replace(" ", "_"): Annotated[
            type(value), FieldInfo(description=key, alias=key.replace("_", " "))
        ]
        for key, value in new_dict.items()
    }

    model = create_model(name, **fields, model_config=CONFIG)  # type: ignore
    return model(**new_dict)

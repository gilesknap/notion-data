from typing import Annotated

from pydantic import create_model
from pydantic.fields import Field

from .root import Root


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

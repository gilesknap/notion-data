"""
Helper functions for preparting data for API requests.
"""

from pydantic import BaseModel


def encode_object(obj: BaseModel) -> dict:
    """
    Encode a Python object into a format that the Notion API can understand.
    """

    def remove_read_only_fields(obj):
        # remove fields that cannot be set
        for field in ["created_time", "created_by", "Created_time", "Created_by"]:
            if hasattr(obj, field):
                delattr(obj, field)

    remove_read_only_fields(obj)
    if hasattr(obj, "properties"):
        remove_read_only_fields(obj.properties)

    json = obj.model_dump(by_alias=True, exclude_unset=True)
    return json

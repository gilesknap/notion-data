"""
Classes for identifying data in Notion.
"""

from typing import Literal

from pydantic import Field

from .regex import UUIDv4
from .root import Root


class NotionUser(Root):
    """A Notion user object"""

    object: Literal["user"] = "user"
    id: str = Field(description="The ID of the user", pattern=UUIDv4)

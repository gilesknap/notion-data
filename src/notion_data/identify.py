"""
Classes for identifying data in Notion.
"""

from typing import Literal

from .regex import ID
from .root import Root


class NotionUser(Root):
    """A Notion user object"""

    object: Literal["user"] = "user"
    id: str = ID

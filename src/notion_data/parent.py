"""
Represents a parent object in Notion.

https://developers.notion.com/reference/parent-object
"""

from typing import Annotated, Literal, Union

from pydantic import Field

from .regex import UUIDv4
from .root import Root


class DatabaseParent(Root):
    """A database parent object in Notion"""

    type: Literal["database_id"]
    database_id: str = Field(description="The ID of the database", pattern=UUIDv4)


class PageParent(Root):
    """A page parent object in Notion"""

    type: Literal["page_id"]
    page_id: str = Field(description="The ID of the page", pattern=UUIDv4)


class WorkspaceParent(Root):
    """A workspace parent object in Notion"""

    type: Literal["workspace"]
    workspace: bool = True


class BlockParent(Root):
    """A block parent object in Notion"""

    type: Literal["block_id"]
    id: str = Field(description="The ID of the block", pattern=UUIDv4)
    block: bool = True


Parent = Annotated[  # type: ignore
    DatabaseParent | PageParent | WorkspaceParent | BlockParent,
    Field(discriminator="type", description="union of arg types"),
]
""" Parent is union of all parent types, discriminated by `type` literal """

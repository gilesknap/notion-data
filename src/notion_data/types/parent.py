"""
Represents a parent object in Notion.

https://developers.notion.com/reference/parent-object
"""

from typing import Annotated, Literal, TypeAlias

from pydantic import Field

from .model import Root
from .regex import ID


class DatabaseParent(Root):
    """A database parent object in Notion"""

    type: Literal["database_id"] = "database_id"
    database_id: str = ID


class PageParent(Root):
    """A page parent object in Notion"""

    type: Literal["page_id"] = "page_id"
    page_id: str = ID


class WorkspaceParent(Root):
    """A workspace parent object in Notion"""

    type: Literal["workspace"] = "workspace"
    workspace: bool = True


class BlockParent(Root):
    """A block parent object in Notion"""

    type: Literal["block_id"] = "block_id"
    id: str = ID
    block: bool = True


_ParentUnion: TypeAlias = Annotated[  # type: ignore
    DatabaseParent | PageParent | WorkspaceParent | BlockParent,
    Field(discriminator="type", description="union of arg types"),
]
""" Parent is union of all parent types, discriminated by `type` literal """

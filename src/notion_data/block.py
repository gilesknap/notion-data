"""
Represent the block data structure in the Notion API.

https://developers.notion.com/reference/block
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Literal

from pydantic import Field, RootModel

from .identify import NotionUser
from .parent import Parent
from .regex import UUIDv4
from .rich_text import RichText
from .root import Root


class Block(RootModel):
    root: BlockUnion


class BlockEnum(Enum):
    BOOKMARK = "bookmark"
    BREADCRUMB = "breadcrumb"
    BULLETED_LIST_ITEM = "bulleted_list_item"
    CALLOUT = "callout"
    CHILD_DATABASE = "child_database"
    CHILD_PAGE = "child_page"
    COLUMN = "column"
    COLUMN_LIST = "column_list"
    DIVIDER = "divider"
    EMBED = "embed"
    EQUATION = "equation"
    FILE = "file"
    HEADING_1 = "heading_1"
    HEADING_2 = "heading_2"
    HEADING_3 = "heading_3"
    IMAGE = "image"
    LINK_PREVIEW = "link_preview"
    LINK_TO_PAGE = "link_to_page"
    NUMBERED_LIST_ITEM = "numbered_list_item"
    PARAGRAPH = "paragraph"
    PDF = "pdf"
    QUOTE = "quote"
    SYNCED_BLOCK = "synced_block"
    TABLE = "table"
    TABLE_OF_CONTENTS = "table_of_contents"
    TABLE_ROW = "table_row"
    TEMPLATE = "template"  # deprecated - w
    TO_DO = "to_do"
    TOGGLE = "toggle"
    UNSUPPORTED = "unsupported"
    VIDEO = "video"


class BlockCommon(Root):
    """A block in Notion"""

    object: Literal["block"]
    id: str = Field(description="The ID of the block", pattern=UUIDv4)
    parent: Parent
    created_time: datetime | None = None
    last_edited_time: datetime | None = None
    created_by: NotionUser | None = None
    last_edited_by: NotionUser | None = None
    has_children: bool = False
    archived: bool = False
    in_trash: bool = False


class _HeadingData(Root):
    rich_text: RichText
    color: str = "default"
    is_toggleable: bool = False


class Heading1(BlockCommon):
    type: Literal["heading_1"]
    heading_1: _HeadingData


class Heading2(BlockCommon):
    type: Literal["heading_2"]
    heading_2: _HeadingData


class Heading3(BlockCommon):
    type: Literal["heading_3"]
    heading_3: _HeadingData


class Paragraph(BlockCommon):
    type: Literal["paragraph"]
    paragraph: RichText
    color: str = "default"
    children: list[BlockUnion] | None = None


class Todo(BlockCommon):
    class TodoData(Root):
        rich_text: RichText
        checked: bool = False
        color: str = "default"
        children: list[BlockUnion]

    type: Literal["to_do"]
    to_do: TodoData


""" Block is union of all block types, discriminated by type literal """
# TODO iterate over the subclasses of BlockCommon instead of hardcoding them
BlockUnion = Annotated[
    Heading2 | Paragraph | Todo,
    Field(discriminator="type", description="union of arg types"),
]

"""
Represent the block data structure in the Notion API.

https://developers.notion.com/reference/block
"""

# TODO see here for some good tricks on how to do partial models for patching
# etc. This would avoid all the | None stuff
# https://github.com/pydantic/pydantic/issues/6381

# TODO: important: we need to consolodate the use of TypeAdapter, RootModel,
# at present I seem to have ended up with a mix of approaches to dealing with
# Unions, list and dict[str, Union] types.

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, TypeAlias, Union

from pydantic import (
    Field,
    RootModel,
    TypeAdapter,
    field_serializer,
)

from .types.enums import Color, Language
from .types.file import FileUnion
from .types.model import Root, format_datetime
from .types.parent import _ParentUnion
from .types.regex import ID
from .types.rich_text import RichText, Url
from .types.simple import HeadingData, Icon, NotionUser


class _BlockCommon(Root):
    """A block in Notion"""

    object: Literal["block"] | None = None
    id: str | None = ID
    parent: _ParentUnion | None = None
    created_time: datetime | None = None
    last_edited_time: datetime | None = None

    created_by: NotionUser | None = None
    last_edited_by: NotionUser | None = None
    has_children: bool = False
    archived: bool = False
    in_trash: bool = False
    request_id: str | None = ID

    @field_serializer("last_edited_time", "created_time")
    def validate_time(self, time: datetime, _info):
        return format_datetime(time)


class Bookmark(_BlockCommon):
    class _BookmarkData(Root):
        url: str
        caption: list[RichText]

    type: Literal["bookmark"]
    bookmark: _BookmarkData


class BreadCrumb(_BlockCommon):
    type: Literal["breadcrumb"]
    breadcrumb: dict = {}


class BulletedListItem(_BlockCommon):
    class _BulletedData(Root):
        rich_text: list[RichText]
        color: Color = Color.DEFAULT
        children: list[BlockUnion] | None = None

    type: Literal["bulleted_list_item"]
    bulleted_list_item: _BulletedData


class Callout(_BlockCommon):
    class _CalloutData(Root):
        rich_text: list[RichText]
        icon: Icon | None = None
        color: Color = Color.DEFAULT

    type: Literal["callout"]
    callout: _CalloutData


class ChildDatabase(_BlockCommon):
    class _ChildDatabaseData(Root):
        title: str

    type: Literal["child_database"]
    child_database: _ChildDatabaseData


class ChildPage(_BlockCommon):
    class _ChildPageData(Root):
        title: str

    type: Literal["child_page"]
    child_page: _ChildPageData


class Code(_BlockCommon):
    class _CodeData(Root):
        caption: list[RichText]
        rich_text: list[RichText]
        language: Language

    type: Literal["code"]
    code: _CodeData


class ColumnList(_BlockCommon):
    type: Literal["column_list"]
    column_list: dict = {}


class Column(_BlockCommon):
    type: Literal["column"]
    column: dict = {}


class Heading1(_BlockCommon):
    type: Literal["heading_1"]
    heading_1: HeadingData


class Divider(_BlockCommon):
    type: Literal["divider"]
    divider: dict = {}


class Embed(_BlockCommon):
    type: Literal["embed"]
    embed: Url


class Equation(_BlockCommon):
    class _EquationData(Root):
        expression: str

    type: Literal["equation"]
    equation: _EquationData


class FileBlock(_BlockCommon):
    type: Literal["file"]
    file: FileUnion


class Heading2(_BlockCommon):
    type: Literal["heading_2"]
    heading_2: HeadingData


class Heading3(_BlockCommon):
    type: Literal["heading_3"]
    heading_3: HeadingData


class Image(_BlockCommon):
    class _ImageData(Root):
        file: FileUnion

    type: Literal["image"]
    image: _ImageData


class LinkPreview(_BlockCommon):
    """
    Cannot be created by the API, only returned in the context of a page.
    """

    type: Literal["link_preview"]
    link_to: Url


class NumberedListItem(_BlockCommon):
    class _NumberedListItemData(Root):
        rich_text: list[RichText]
        color: Color = Color.DEFAULT
        children: list[BlockUnion] | None = None

    type: Literal["numbered_list_item"]
    numbered_list_item: _NumberedListItemData


class Paragraph(_BlockCommon):
    class _ParagraphData(Root):
        rich_text: list[RichText]
        color: Color = Color.DEFAULT
        children: list[BlockUnion] | None = None

    type: Literal["paragraph"] = "paragraph"
    paragraph: _ParagraphData


class Quote(_BlockCommon):
    class _QuoteData(Root):
        rich_text: list[RichText]
        color: Color = Color.DEFAULT
        children: list[BlockUnion] | None = None

    type: Literal["quote"]
    quote: _QuoteData


class SyncedBlock(_BlockCommon):
    class _SyncedBlockData(Root):
        class _SyncedFrom(Root):
            block_id: str = ID

        synced_from: _SyncedFrom | None
        children: list[BlockUnion] | None = None

    type: Literal["synced_block"]
    synced_block: _SyncedBlockData


class Table(_BlockCommon):
    class _TableData(Root):
        table_width: int
        has_column_header: bool
        has_row_header: bool

    type: Literal["table"]
    table: _TableData


class TableRow(_BlockCommon):
    class _TableRowData(Root):
        cells: list[list[RichText]]

    type: Literal["table_row"]
    table_row: _TableRowData


class Todo(_BlockCommon):
    class TodoData(Root):
        rich_text: list[RichText]
        checked: bool = False
        color: Color = Color.DEFAULT
        children: list[BlockUnion] | None = None

    type: Literal["to_do"]
    to_do: TodoData


class Toggle(_BlockCommon):
    class _ToggleData(Root):
        rich_text: list[RichText]
        color: Color = Color.DEFAULT
        children: list[BlockUnion] | None = None

    type: Literal["toggle"]
    toggle: _ToggleData


class Video(_BlockCommon):
    class _VideoData(Root):
        file: FileUnion

    type: Literal["video"]
    video: _VideoData


""" Block is union of all block types, discriminated by type literal """
BlockUnion: TypeAlias = Annotated[  # type: ignore
    Union[tuple(_BlockCommon.__subclasses__())],  # type: ignore
    Field(discriminator="type", description="union of block types"),
]


Block = TypeAdapter(BlockUnion)


class Blocks(Root):
    """A list of blocks in Notion returned by api call blocks.children.list"""

    object: Literal["list"] = "list"
    type: Literal["block"] = "block"
    results: list[BlockUnion]
    next_cursor: str | None = None
    request_id: str = ID
    block: BlockUnion | dict = {}
    has_more: bool = False


class BlocksList(RootModel):
    """A list of blocks to pass to api call blocks.children.append"""

    root: list[BlockUnion]

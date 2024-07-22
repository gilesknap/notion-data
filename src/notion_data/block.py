"""
Represent the block data structure in the Notion API.

https://developers.notion.com/reference/block
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, TypeAlias, Union

from pydantic import Field, RootModel, model_validator

from .enums import Color, Language
from .file import FileObject
from .identify import NotionUser
from .parent import Parent
from .regex import UUIDv4
from .rich_text import RichText
from .root import Root


class Block(RootModel):
    root: _BlockUnion


class _BlockCommon(Root):
    """A block in Notion"""

    # child block objects do not require type
    object: Literal["block"] | None = None
    id: str | None = Field(
        default=None, description="The ID of the block", pattern=UUIDv4
    )
    # child block objects do not require parent
    parent: Parent | None = None
    created_time: datetime | None = None
    last_edited_time: datetime | None = None
    created_by: NotionUser | None = None
    last_edited_by: NotionUser | None = None
    has_children: bool = False
    archived: bool = False
    in_trash: bool = False
    request_id: str | None = Field(
        default=None, description="The ID of the block", pattern=UUIDv4
    )

    @model_validator(mode="before")
    # for child blocks, type is not required so insert it
    # so that the discriminator is present
    def insert_type(cls, values):
        if "type" not in values:
            # type is the first and only key in the dict
            values["type"] = list(values)[0]
        return values


class Bookmark(_BlockCommon):
    class _BookmarkData(Root):
        url: str
        caption: RichText

    type: Literal["bookmark"]
    bookmark: _BookmarkData


class BreadCrumb(_BlockCommon):
    type: Literal["breadcrumb"]
    breadcrumb: dict = {}


class BulletedListItem(_BlockCommon):
    class _BulletedData(Root):
        rich_text: RichText
        color: Color = Color.DEFAULT
        children: list[_ChildBlockUnion] | None = None

    type: Literal["bulleted_list_item"]
    bulleted_list_item: RichText


class Callout(_BlockCommon):
    class _CalloutData(Root):
        rich_text: RichText
        icon: str | None = None
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
        caption: RichText
        rich_text: RichText
        language: Language

    type: Literal["code"]
    code: _CodeData


class ColumnList(_BlockCommon):
    type: Literal["column_list"]
    column_list: dict = {}


class Column(_BlockCommon):
    type: Literal["column"]
    column: dict = {}


class _HeadingData(Root):
    rich_text: RichText
    color: Color = Color.DEFAULT
    is_toggleable: bool = False


class Heading1(_BlockCommon):
    type: Literal["heading_1"]
    heading_1: _HeadingData


class Divider(_BlockCommon):
    type: Literal["divider"]
    divider: dict = {}


class Embed(_BlockCommon):
    class _EmbedData(Root):
        url: str

    type: Literal["embed"]
    embed: _EmbedData


class Equation(_BlockCommon):
    class _EquationData(Root):
        expression: str

    type: Literal["equation"]
    equation: _EquationData


class File(_BlockCommon):
    type: Literal["file"]
    file: FileObject


class Heading2(_BlockCommon):
    type: Literal["heading_2"]
    heading_2: _HeadingData


class Heading3(_BlockCommon):
    type: Literal["heading_3"]
    heading_3: _HeadingData


class Image(_BlockCommon):
    class _ImageData(Root):
        file: FileObject

    type: Literal["image"]
    image: _ImageData


class LinkPreview(_BlockCommon):
    """
    Cannot be created by the API, only returned in the context of a page.
    """

    class _LinkPreviewData(Root):
        url: str

    type: Literal["link_preview"]
    link_to: _LinkPreviewData


class NumberedListItem(_BlockCommon):
    class _NumberedListItemData(Root):
        rich_text: RichText
        color: Color = Color.DEFAULT
        children: list[_ChildBlockUnion] | None = None

    type: Literal["numbered_list_item"]
    numbered_list_item: _NumberedListItemData


class Paragraph(_BlockCommon):
    class _ParagraphData(Root):
        rich_text: RichText
        color: Color = Color.DEFAULT
        children: list[_ChildBlockUnion] | None = None

    type: Literal["paragraph"]
    paragraph: _ParagraphData


class Quote(_BlockCommon):
    class _QuoteData(Root):
        rich_text: RichText
        color: Color = Color.DEFAULT
        children: list[_ChildBlockUnion] | None = None

    type: Literal["quote"]
    quote: _QuoteData


class SyncedBlock(_BlockCommon):
    class _SyncedBlockData(Root):
        class _SyncedFrom(Root):
            block_id: str = Field(description="The ID of the block", pattern=UUIDv4)

        synced_from: _SyncedFrom | None
        children: list[_ChildBlockUnion] | None = None

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
        cells: list[RichText]

    type: Literal["table_row"]
    table_row: _TableRowData


class Todo(_BlockCommon):
    class TodoData(Root):
        rich_text: RichText
        checked: bool = False
        color: Color = Color.DEFAULT
        children: list[_ChildBlockUnion] | None = None

    type: Literal["to_do"]
    to_do: TodoData


class Toggle(_BlockCommon):
    class _ToggleData(Root):
        rich_text: RichText
        color: Color = Color.DEFAULT
        children: list[_ChildBlockUnion] | None = None

    type: Literal["toggle"]
    toggle: _ToggleData


class Video(_BlockCommon):
    class _VideoData(Root):
        file: FileObject

    type: Literal["video"]
    video: _VideoData


""" Block is union of all block types, discriminated by type literal """
_BlockUnion: TypeAlias = Annotated[  # type: ignore
    Union[tuple(_BlockCommon.__subclasses__())],  # type: ignore
    Field(discriminator="type", description="union of block types"),
]

""" ChildBlocks do not have type so can't use it as a discriminator.
    In the model validator for these we insert the type so that
    Pytdantic can resolve the subclass of the Union - just not as easilty as
    with the discriminator.

    (unfortunately discriminators are applied before the model validator
    so we can't use type here even though the validator is adding it)
"""
_ChildBlockUnion: TypeAlias = Annotated[  # type: ignore
    Union[tuple(_BlockCommon.__subclasses__())],  # type: ignore
    Field(description="union of block types"),
]

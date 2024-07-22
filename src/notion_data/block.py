"""
Represent the block data structure in the Notion API.

https://developers.notion.com/reference/block
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, Union

from pydantic import Field, RootModel

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

    object: Literal["block"]
    id: str | None = Field(
        default=None, description="The ID of the block", pattern=UUIDv4
    )
    parent: Parent
    created_time: datetime | None = None
    last_edited_time: datetime | None = None
    created_by: NotionUser | None = None
    last_edited_by: NotionUser | None = None
    has_children: bool = False
    archived: bool = False
    in_trash: bool = False


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
        children: list[_BlockUnion]

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


class Paragraph(_BlockCommon):
    type: Literal["paragraph"]
    paragraph: RichText
    color: Color = Color.DEFAULT
    children: list[_BlockUnion] | None = None


class Todo(_BlockCommon):
    class TodoData(Root):
        rich_text: RichText
        checked: bool = False
        color: Color = Color.DEFAULT
        children: list[_BlockUnion]

    type: Literal["to_do"]
    to_do: TodoData


""" Block is union of all block types, discriminated by type literal """
_BlockUnion = Annotated[
    Union[tuple(_BlockCommon.__subclasses__())],
    Field(discriminator="type", description="union of arg types"),
]

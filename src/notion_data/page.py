"""
Represent the page data structure in the Notion API.

https://developers.notion.com/reference/page
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


class _PageCommon(Root):
    """A page in Notion"""

    object: Literal["page"] | None = None
    id: str | None = Field(
        default=None, description="The ID of the block", pattern=UUIDv4
    )
    created_time: datetime | None = None
    last_edited_time: datetime | None = None
    created_by: NotionUser | None = None
    last_edited_by: NotionUser | None = None
    cover: FileObject | None = None
    icon: FileObject | None = None
    has_children: bool = False
    parent: Parent | None = None
    archived: bool = False
    in_trash: bool = False
    request_id: str | None = Field(
        default=None, description="The ID of the block", pattern=UUIDv4
    )
    properties: dict[PageProperty]
    url: str | None = None
    public_url: str | None = None


class PageProperty(Root):
    # id and type are returned in get's but not required for post / patch
    id: str | None = None


class DueDate(PageProperty):
    class _DueDateData(Root):
        due_date: datetime

    type: Literal["due_date"] = "due_date"
    DueDate: _DueDateData


class State(PageProperty):
    class _StateData(Root):
        select: Annotated[dict[str, str], Field(alias="select")]

    type: Literal["state"] = "state"
    State: _StateData


class Title(PageProperty):
    class _TitleData(Root):
        title: RichText

    type: Literal["title"] = "title"
    Title: _TitleData

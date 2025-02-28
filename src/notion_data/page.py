"""
Represent the page data structure in the Notion API.

https://developers.notion.com/reference/page
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, Sequence, TypeAlias, Union

from pydantic import Field, field_serializer, field_validator

from .dynamic import dict_model_instance
from .enums import Color
from .file import FileUnion
from .identify import NotionUser
from .parent import _ParentUnion
from .regex import ID
from .rich_text import RichText
from .root import Root, format_datetime


class Icon(Root):
    # TODO this needs to be a union of emoji and other things
    type: Literal["emoji"] = "emoji"
    emoji: str


class PageProperty(Root):
    # id and type are returned in get's but not required for post / patch
    id: str | None = None


class Checkbox(PageProperty):
    type: Literal["checkbox"] = "checkbox"
    checkbox: bool


class User(Root):
    class _Person(Root):
        email: str

    object: Literal["user"] = "user"
    id: str = ID
    name: str | None = None
    avatar_url: str | None = None
    type: str | None = None
    bot: dict | None = None
    person: _Person | None = None


class CreatedBy(PageProperty):
    type: Literal["created_by"] = "created_by"
    created_by: User


class CreatedTime(PageProperty):
    type: Literal["created_time"] = "created_time"
    created_time: datetime

    @field_serializer("created_time")
    def validate_time(self, time: datetime, _info):
        return format_datetime(time)


class Date(PageProperty):
    class _DateData(Root):
        start: datetime
        end: datetime | None = None
        time_zone: str | None = None

        @field_serializer("start", "end")
        def validate_time(self, time: datetime, _info):
            return format_datetime(time)

    type: Literal["date"] = "date"
    date: _DateData


class Email(PageProperty):
    type: Literal["email"] = "email"
    email: str


class Files(PageProperty):
    type: Literal["files"] = "files"
    files: list[FileUnion]


class Formula(PageProperty):
    type: Literal["formula"] = "formula"
    formula: FormulaBool | FormulaDate | FormulaNumber | FormulaString


class FormulaBool(Root):
    type: Literal["bool"] = "bool"
    formula: bool


class FormulaDate(Root):
    type: Literal["date"] = "date"
    formula: datetime


class FormulaNumber(Root):
    type: Literal["number"] = "number"
    formula: float | int


class FormulaString(Root):
    type: Literal["string"] = "string"
    formula: str


class LastEditedBy(PageProperty):
    type: Literal["last_edited_by"] = "last_edited_by"
    last_edited_by: User


class LastEditedTime(PageProperty):
    type: Literal["last_edited_time"] = "last_edited_time"
    last_edited_time: datetime


class MultiSelect(PageProperty):
    class _MultiSelectData(Root):
        color: Color = Color.DEFAULT
        id: str = ID  # TODO the docs imply this may not be a UUID
        # https://developers.notion.com/reference/page-property-values#example-multi_select-page-property-value-as-returned-in-a-get-page-request
        name: str

    type: Literal["multi_select"] = "multi_select"
    multi_select: list[_MultiSelectData]


class Number(PageProperty):
    type: Literal["number"] = "number"
    number: float | int


class People(PageProperty):
    type: Literal["people"] = "people"
    people: list[User]


class Relation(PageProperty):
    class _RelationData(Root):
        id: str = ID

    type: Literal["relation"] = "relation"
    has_more: bool | None = None
    relation: list[_RelationData]


class Status(PageProperty):
    class _StatusData(Root):
        id: str | None = ID
        name: str
        color: Color = Color.DEFAULT

    type: Literal["status"] = "status"
    status: _StatusData


class TitleClass(PageProperty):
    type: Literal["title"] = "title"
    title: Sequence[RichText]


PropertyUnion: TypeAlias = Annotated[  # type: ignore
    # TODO need to include list[RichText] but that is a list and therefore not
    # a Pydantic model - how to do this?
    Union[tuple(PageProperty.__subclasses__())],  # type: ignore
    Field(description="union of block types"),
]


class Page(Root):
    """A page in Notion"""

    object: Literal["page"] = "page"
    id: str = ID
    created_time: datetime | None = None
    last_edited_time: datetime | None = None
    created_by: NotionUser | None = None
    last_edited_by: NotionUser | None = None
    cover: FileUnion | None = None
    icon: Icon | None = None
    has_children: bool = False
    parent: _ParentUnion
    archived: bool = False
    in_trash: bool = False
    request_id: str | None = ID
    url: str | None = None
    public_url: str | None = None
    # Properties' keys are the column names from parent database
    # Therefore dynamic - model is created by validate_properties below
    # TODO: model this as title: TitleClass | dynamic properties
    properties: dict[str, PropertyUnion]

    @field_serializer("last_edited_time", "created_time")
    def validate_time(self, time: datetime, _info):
        return format_datetime(time)

    @field_validator("properties", mode="after")
    def validate_properties(cls, properties, _info):
        return dict_model_instance("properties", properties)

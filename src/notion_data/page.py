"""
Represent the page data structure in the Notion API.

https://developers.notion.com/reference/page
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, TypeAlias, Union

from pydantic import Field, RootModel

from .enums import Color
from .file import FileObject
from .identify import NotionUser
from .parent import Parent
from .regex import UUIDv4
from .rich_text import RichText
from .root import Root

ID: Field = Field(default=None, description="Identifier", pattern=UUIDv4)  # type: ignore


class Icon(Root):
    # TODO this needs to be a union of emoji and other things
    type: Literal["emoji"]
    emoji: str


class PageProperty(Root):
    # id and type are returned in get's but not required for post / patch
    id: str | None = None
    # name is shown in the docs sometimes but is just a copy of the property key
    name: str | None = None

    # @model_validator(mode="before")
    # # ensure the discriminator is present
    # def insert_type(cls, values):
    #     if "type" not in values:
    #         # type is the first and only key in the dict
    #         values["type"] = list(values)[0]
    #     return values


class Checkbox(PageProperty):
    type: Literal["checkbox"]
    checkbox: bool


class User(Root):
    class _Person(Root):
        email: str

    object: Literal["user"]
    id: str = ID
    name: str | None = None
    avatar_url: str | None = None
    type: str | None = None
    bot: dict | None = None
    person: _Person | None = None


class CreatedBy(PageProperty):
    type: Literal["created_by"]
    created_by: User


class CreatedTime(PageProperty):
    type: Literal["created_time"]
    created_time: datetime


class Date(PageProperty):
    class _DateData(Root):
        start: datetime
        end: datetime | None = None
        time_zone: str | None = None

    type: Literal["date"]
    date: _DateData


class Email(PageProperty):
    type: Literal["email"]
    email: str


class Files(PageProperty):
    type: Literal["files"]
    files: list[FileObject]


class Formula(PageProperty):
    type: Literal["formula"]
    formula: FormulaBool | FormulaDate | FormulaNumber | FormulaString


class FormulaBool(Root):
    type: Literal["bool"]
    formula: bool


class FormulaDate(Root):
    type: Literal["date"]
    formula: datetime


class FormulaNumber(Root):
    type: Literal["number"]
    formula: float | int


class FormulaString(Root):
    type: Literal["string"]
    formula: str


class LastEditedBy(PageProperty):
    type: Literal["last_edited_by"]
    last_edited_by: User


class LastEditedTime(PageProperty):
    type: Literal["last_edited_time"]
    last_edited_time: datetime


class MultiSelect(PageProperty):
    class _MultiSelectData(Root):
        color: Color = Color.DEFAULT
        id: str = ID  # TODO the docs imply this may not be a UUID
        # https://developers.notion.com/reference/page-property-values#example-multi_select-page-property-value-as-returned-in-a-get-page-request
        name: str

    type: Literal["multi_select"]
    multi_select: list[_MultiSelectData]


class Number(PageProperty):
    type: Literal["number"]
    number: float | int


class People(PageProperty):
    type: Literal["people"]
    people: list[User]


class Relation(PageProperty):
    class _RelationData(Root):
        id: str = ID

    type: Literal["relation"]
    has_more: bool | None = None
    relation: list[_RelationData]


class Status(PageProperty):
    class _StatusData(Root):
        id: str | None = ID
        name: str
        color: Color = Color.DEFAULT

    type: Literal["status"]
    status: _StatusData


class Title(PageProperty):
    type: Literal["title"]
    title: RichText


_PropertyUnion: TypeAlias = Annotated[  # type: ignore
    # TODO need to include RichText but that is a list and therefore not
    # a Pydantic model - how to do this?
    Union[tuple(PageProperty.__subclasses__())],  # type: ignore
    Field(description="union of block types"),
]

PageProperties: TypeAlias = Annotated[
    dict[str, _PropertyUnion], Field(description="dynamic page properties")
]


class _PageCommon(Root):
    """A page in Notion"""

    object: Literal["page"]
    id: str | None = ID
    created_time: datetime | None = None
    last_edited_time: datetime | None = None
    created_by: NotionUser | None = None
    last_edited_by: NotionUser | None = None
    cover: FileObject | None = None
    icon: Icon | None = None
    has_children: bool = False
    parent: Parent | None = None
    archived: bool = False
    in_trash: bool = False
    request_id: str | None = ID
    properties: PageProperties
    url: str | None = None
    public_url: str | None = None

    # @model_validator(mode="after")
    # # because the property keys are dynamic, we need to convert them to a
    # # model at validation time
    # def make_properties(self) -> Self:
    #     self.properties = dict_model_instance("PageProperties", self.properties)
    #     return self


class Page(RootModel):
    root: _PageCommon

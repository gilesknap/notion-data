"""
Some simple types used by pages and/or blocks
"""

from datetime import datetime
from typing import Literal

from .enums import Color
from .model import Root
from .regex import ID
from .rich_text import RichText


class Icon(Root):
    # TODO this needs to be a union of emoji and other things
    type: Literal["emoji"] = "emoji"
    emoji: str


class HeadingData(Root):
    rich_text: list[RichText]
    color: Color = Color.DEFAULT
    is_toggleable: bool = False


class NotionUser(Root):
    """A Notion user object"""

    object: Literal["user"] = "user"
    id: str = ID


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

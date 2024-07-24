"""
Represent the rich text data structure in the Notion API.

https://developers.notion.com/reference/rich-text
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field

from .root import Root

# TODO href should be typed ??


class Url(Root):
    type: Literal["url"] | None = None
    url: str


class BaseRichText(Root):
    """A base class for all rich text objects"""

    annotations: Annotations | None = None
    plain_text: str | None = None
    href: str | None = None


class TextObject(BaseRichText):
    class TextObjectData(Root):
        content: str
        link: Url | None = None

    type: Literal["text"]
    text: TextObjectData


class Mention(BaseRichText):
    type: Literal["mention"]
    mention: list  # TODO


class Equation(BaseRichText):
    type: Literal["equation"]
    equation: dict  # TODO


class Annotations(Root):
    bold: bool = False
    italic: bool = False
    strikethrough: bool = False
    underline: bool = False
    code: bool = False
    color: str = "default"


RichTextUnion = Annotated[
    TextObject | Mention | Equation,
    Field(discriminator="type", description="union of rich text types"),
]

RichText = list[RichTextUnion]

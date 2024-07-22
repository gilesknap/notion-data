"""
Represent the rich text data structure in the Notion API.

https://developers.notion.com/reference/rich-text
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field

from .root import Root

# TODO href and color should be typed as ?? / enum


class BaseRichText(Root):
    """A base class for all rich text objects"""

    annotations: Annotations
    plain_text: str
    href: str | None


class TextObject(BaseRichText):
    class TextObjectData(Root):
        content: str
        link: str | None

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

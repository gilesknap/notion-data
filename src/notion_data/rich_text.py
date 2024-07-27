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


class _BaseRichText(Root):
    """A base class for all rich text objects"""

    annotations: Annotations | None = None
    plain_text: str | None = None
    href: str | None = None


class TextObject(_BaseRichText):
    def __init__(self, text, **data) -> None:
        if isinstance(text, str):
            data["text"] = self._TextObjectData(content=text, link=data.get("link"))
        else:
            data["text"] = text
        super().__init__(**data)

    class _TextObjectData(Root):
        content: str = ""
        link: Url | None = None

    type: Literal["text"] = "text"
    text: _TextObjectData


class Mention(_BaseRichText):
    type: Literal["mention"] = "mention"
    mention: list  # TODO


class Equation(_BaseRichText):
    type: Literal["equation"] = "equation"
    equation: dict  # TODO


class Annotations(Root):
    bold: bool = False
    italic: bool = False
    strikethrough: bool = False
    underline: bool = False
    code: bool = False
    color: str = "default"


RichText = Annotated[
    TextObject | Mention | Equation,
    Field(discriminator="type", description="union of rich text types"),
]

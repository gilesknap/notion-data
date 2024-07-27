"""
Represents a file object in Notion.

https://developers.notion.com/reference/file-object
"""

from datetime import datetime
from typing import Annotated, Literal, TypeAlias, Union

from pydantic import Field

from .rich_text import RichText
from .root import Root


class _FileCommon(Root):
    caption: list[RichText] | None = None
    name: str | None = None


class FileUrl(_FileCommon):
    """A file object in Notion"""

    class _FileData(Root):
        url: str
        expiry_time: datetime

    type: Literal["file"] = "file"
    file: _FileData


class FileExternal(_FileCommon):
    """An external file object in Notion"""

    class _FileExternalData(Root):
        url: str

    type: Literal["external"] = "external"
    external: _FileExternalData


class PDF(_FileCommon):
    """A PDF file object in Notion"""

    type: Literal["pdf"] = "pdf"
    pdf: FileExternal


_FileUnion: TypeAlias = Annotated[  # type: ignore
    Union[tuple(_FileCommon.__subclasses__())],  # type: ignore
    Field(discriminator="type", description="union of arg types"),
]

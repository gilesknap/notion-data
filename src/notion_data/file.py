"""
Represents a file object in Notion.

https://developers.notion.com/reference/file-object
"""

from datetime import datetime
from typing import Annotated, Literal, Union

from pydantic import Field

from .rich_text import RichText
from .root import Root


class _FileCommon(Root):
    caption: RichText | None = None
    name: str | None = None


class FileUrl(_FileCommon):
    """A file object in Notion"""

    class _FileData(Root):
        url: str
        expiry_time: datetime

    type: Literal["file"]
    file: _FileData


class FileExternal(_FileCommon):
    """An external file object in Notion"""

    class _FileExternalData(Root):
        url: str

    type: Literal["external"]
    external: _FileExternalData


class PDF(_FileCommon):
    """A PDF file object in Notion"""

    type: Literal["pdf"]
    pdf: FileExternal


FileObject = Annotated[
    Union[tuple(_FileCommon.__subclasses__())],
    Field(discriminator="type", description="union of arg types"),
]

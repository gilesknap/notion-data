"""
Functions to help with creation of more complex properties types
"""

from datetime import datetime

from ..file import FileExternal, FileUnion, FileUrl
from ..page import PropertyUnion, TitleClass
from ..rich_text import RichText, RichTextList, TextObject, Url
from ..root import unset_none


def add_properties(
    properties: dict[str, PropertyUnion] | None = None, **kargs
) -> dict[str, PropertyUnion]:
    """
    Add a list of kwargs to a dictionary of properties. Optianally, pass in a
    dictionary of properties to update.

    returns: dict of properties
    """
    if properties is None:
        properties = {}
    # TODO: could validate property types here for early error detection
    properties.update(kargs)
    return properties


def rich_text(text: str, link: str | None = None) -> RichTextList:
    """
    Create a rich text object for a page property.
    """
    url = Url(url=link) if link else None
    data = TextObject._TextObjectData(content=text, link=url)
    return RichTextList([TextObject(text=data)])


def title(text: str, link: str | None = None) -> TitleClass:
    """
    Create a textual title object for a page property.
    """
    rich = rich_text(text, link)
    return TitleClass(title=rich)


def file(
    url: str,
    name: str | None = None,
    caption: list[RichText] | None = None,
    expiry_time: datetime | None = None,
) -> FileUnion:
    """
    Create a file object for a page property.
    """
    if expiry_time is None:
        ext_data = FileExternal._FileExternalData(url=url)
        ext_file = FileExternal(external=ext_data, name=name, caption=caption)
        unset_none(ext_file)
        return ext_file
    else:
        data = FileUrl._FileData(url=url, expiry_time=expiry_time)
        return FileUrl(file=data, name=name, caption=caption)

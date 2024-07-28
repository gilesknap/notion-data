"""
Functions to help with creation of more complex properties types
"""

from datetime import datetime

from ..page import PropertyUnion, TitleClass
from ..types.file import FileExternal, FileUnion, FileUrl
from ..types.model import unset_none
from ..types.rich_text import RichText, RichTextList, TextObject, Url


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


def rich_text_list(text: str, link: str | None = None) -> RichTextList:
    """
    Create a rich text property (list of TextObject).
    """
    url = Url(url=link) if link else None
    data = TextObject._TextObjectData(content=text, link=url)
    return RichTextList([TextObject(text=data)])


def get_text_object(rich_text: RichTextList, n=0) -> TextObject:
    """
    Get the rich text object from a rich text property.
    """
    return rich_text[n]


def set_rich_text(rich_text: RichTextList, item: RichText, n=0) -> None:
    """
    Update the rich text object in a rich text property.
    """
    rich_text[n].text = item


def title(text: str, link: str | None = None) -> TitleClass:
    """
    Create a title property.
    """
    title = TitleClass(title=rich_text_list(text, link))
    return title


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

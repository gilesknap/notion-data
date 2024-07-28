"""
Helper functions to simplify the creation of the more complex block types.
"""

from ..block import BlockUnion, Paragraph
from ..types.enums import Color
from ..types.model import unset_none
from ..types.rich_text import RichTextList


def paragraph(
    rich_text: RichTextList,
    color: Color = Color.DEFAULT,
    children: list[BlockUnion] | None = None,
) -> Paragraph:
    """
    Create a paragraph object for a page property.
    """
    data = Paragraph._ParagraphData(rich_text=rich_text, color=color, children=children)
    unset_none(data)
    return Paragraph(paragraph=data)

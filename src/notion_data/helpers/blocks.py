"""
Helper functions to simplify the creation of the more complex block types.
"""

from ..block import BlockUnion, Paragraph
from ..enums import Color
from ..rich_text import RichTextList
from ..root import unset_none


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

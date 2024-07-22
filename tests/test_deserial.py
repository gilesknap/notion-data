"""
Testing that we can deserialise notion objects from the documentation into
our own objects.
"""

import json

from notion_data.block import Block
from notion_data.root import Root


class Page(Root):
    block: Block


def test_paragraph(data_folder):
    p = data_folder / "paragraph.json"
    with p.open() as f:
        data = json.load(f)

    page = Page(**data)
    assert page.block.object == "block"

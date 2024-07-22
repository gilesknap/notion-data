"""
Testing that we can deserialise notion objects from the documentation into
our own objects.
"""

import json

from notion_data.block import Block
from notion_data.root import Root


class Page(Root):
    block: Block


def test_block(data_folder):
    """
    example: https://developers.notion.com/reference/block
    """
    p = data_folder / "block.json"
    with p.open() as f:
        data = json.load(f)

    block = Block(**data)
    assert block.root.object == "block"
    assert block.root.heading_2.rich_text[0].plain_text == "Lacinato kale"

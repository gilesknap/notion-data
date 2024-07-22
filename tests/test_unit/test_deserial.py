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


def test_bookmark(data_folder):
    """
    example: https://developers.notion.com/reference/block
    """
    p = data_folder / "bookmark.json"
    with p.open() as f:
        data = json.load(f)

    block = Block(**data)
    assert block.root.object == "block"
    assert block.root.bookmark.url == "https://companywebsite.com"


def test_breadcrumb(data_folder):
    """
    example: https://developers.notion.com/reference/block
    """
    p = data_folder / "breadcrumb.json"
    with p.open() as f:
        data = json.load(f)

    block = Block(**data)
    assert block.root.object == "block"
    assert block.root.breadcrumb == {}


def test_code(data_folder):
    """
    example: https://developers.notion.com/reference/block
    """
    p = data_folder / "code.json"
    with p.open() as f:
        data = json.load(f)

    block = Block(**data)
    assert block.root.object == "block"
    assert block.root.code.language == "javascript"
    assert block.root.code.rich_text[0].text.content == "const a = 3"


def test_file(data_folder):
    """
    example: https://developers.notion.com/reference/block
    """
    p = data_folder / "file.json"
    with p.open() as f:
        data = json.load(f)

    block = Block(**data)
    assert block.root.object == "block"
    assert block.root.file.external.url == "https://companywebsite.com/files/doc.txt"


def test_synced_from(data_folder):
    """
    example: https://developers.notion.com/reference/block
    """
    p = data_folder / "synced_from.json"
    with p.open() as f:
        data = json.load(f)

    block = Block(**data)
    assert block.root.object == "block"
    assert (
        block.root.synced_block.synced_from.block_id
        == "29833787-2cf9-4fdf-8782-e53db20768a5"
    )


def test_synced_to(data_folder):
    """
    example: https://developers.notion.com/reference/block
    """
    p = data_folder / "synced_to.json"
    with p.open() as f:
        data = json.load(f)

    block = Block(**data)
    assert block.root.object == "block"
    assert block.root.synced_block.synced_from is None
    assert (
        block.root.synced_block.children[0].callout.rich_text[0].text.content
        == "Callout in synced block"
    )

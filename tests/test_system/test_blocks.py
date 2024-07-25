import os

from notion_client import Client

from notion_data.block import Block

secret = os.getenv("NOTION_SECRET")
block_id = "d91a45aac9d54c6f832bf3b2b871c4da"
notion = Client(auth=secret)


def test_get_paragraph():
    block_json = notion.blocks.retrieve(block_id=block_id)

    block = Block.validate_python(block_json)

    assert block.paragraph.rich_text[0].text.content == "Interesting block with url "
    assert block.paragraph.rich_text[1].text.link.url == "http://www.google.com/"

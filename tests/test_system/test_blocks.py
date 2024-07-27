from notion_client import Client

from notion_data.block import Block


def test_get_paragraph(client: Client, ids):
    block_json = client.blocks.retrieve(block_id=ids.block_id)

    block = Block.validate_python(block_json)

    assert block.paragraph.rich_text[0].text.content == "Interesting block with url "
    assert block.paragraph.rich_text[1].text.link.url == "http://www.google.com/"

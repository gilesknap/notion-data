import os
from pprint import pprint

from notion_client import Client

from notion_data.block import Block
from notion_data.page import Page

secret = os.getenv("NOTION_SECRET")
database_page_id = "a53dc7f12ae7499d870f129299a3733b"
database_child_page_id = "eee59c60767348999403c4cd68279b46"
block_id = "d91a45aac9d54c6f832bf3b2b871c4da"

notion = Client(auth=secret)
page_json = notion.pages.retrieve(page_id=database_child_page_id)
pprint(page_json)
block_json = notion.blocks.retrieve(block_id=block_id)
pprint(block_json)

block = Block(block_json)
pprint(block.model_dump())
page = Page(page_json)
pprint(page.model_dump())

pprint(page.root.parent)

print()
pprint(page.root.properties["Created time"].model_dump())
# make a copy of the page
# notion.pages.create(
#     parent=page.root.parent.model_dump(),
#     properties=page.root.properties,
#     cover=page.root.cover,
# )

"""
Some tests to experiment with how to make use of our Notion Data Model.
"""

from datetime import datetime
from pprint import pprint

from notion_data.block import Blocks, BlocksList
from notion_data.helpers.blocks import paragraph
from notion_data.helpers.properties import add_properties, file, rich_text, title
from notion_data.page import Icon, Page
from notion_data.types.parent import PageParent
from notion_data.types.simple import NotionUser


def test_make_page(client, ids):
    # create a new page object
    page = Page(
        last_edited_time=datetime.now(),
        last_edited_by=NotionUser(id=ids.user_id),
        cover=file(url="https://www.notion.so/images/page-cover/webb2.jpg"),
        icon=Icon(emoji="🚀"),
        has_children=False,
        parent=(PageParent(page_id=ids.root_page_id)),
        properties=add_properties(title=title("Generated Test Page")),
    )

    # create the page on the notion server
    result = client.pages.create(
        **page.model_dump(exclude_unset=True, by_alias=True),
    )
    new_page = Page(**result)

    pprint(new_page.model_dump())
    # example of updating a fetched page
    new_page.icon.emoji = "🌟"
    client.pages.update(
        page_id=new_page.id, **new_page.model_dump(exclude_unset=True, by_alias=True)
    )

    # delete the page we just created
    client.pages.update(page_id=new_page.id, archived=True)


def test_make_page_blocks(client, ids):
    p1 = paragraph(rich_text=rich_text("This is a rich text object"))
    p2 = paragraph(rich_text=rich_text("This is another rich text object"))
    p3 = paragraph(rich_text=rich_text("This is a third rich text object"))

    blocks = BlocksList([p1, p2, p3])

    page = Page(
        last_edited_time=datetime.now(),
        last_edited_by=NotionUser(id=ids.user_id),
        cover=file(url="https://www.notion.so/images/page-cover/webb2.jpg"),
        icon=Icon(emoji="🚀"),
        parent=(PageParent(page_id=ids.root_page_id)),
        properties=add_properties(title=title("Generated Test Page with Blocks")),
    )

    # create the initial page
    result = client.pages.create(
        **page.model_dump(exclude_unset=True, by_alias=True),
    )
    new_page = Page.model_validate(result)

    # add the child blocks to the page
    result = client.blocks.children.append(
        children=blocks.model_dump(exclude_unset=True, by_alias=True),
        block_id=new_page.id,
    )

    # fetch the child blocks from the page
    result = client.blocks.children.list(block_id=new_page.id)
    blocks = Blocks(**result)

    # delete the page we just created
    client.pages.update(page_id=new_page.id, archived=True)


def test_get_page_blocks(client, ids):
    # get the blocks of a page
    new_page_result = client.blocks.children.list(block_id=ids.plain_page_id)
    pprint(new_page_result)
    blocks = Blocks.model_validate(new_page_result)
    pprint(blocks.model_dump())

    new_page = Page(
        cover=file(url="https://www.notion.so/images/page-cover/webb2.jpg"),
        icon=Icon(emoji="🚀"),
        parent=(PageParent(page_id=ids.root_page_id)),
        properties=add_properties(
            title=title("Generated Test Page copied from TESTING STD Page")
        ),
    )

    # create the initial page
    new_page_result = client.pages.create(
        **new_page.model_dump(exclude_unset=True, by_alias=True),
    )
    new_page_result = Page(**new_page_result)

    # fetch the child blocks of the page we are copying
    blocks_result = client.blocks.children.list(block_id=ids.plain_page_id)
    blocks = Blocks.model_validate(blocks_result)
    new_blocks = BlocksList(blocks.results)

    # add the children to the page
    _new_blocks_result = client.blocks.children.append(
        children=new_blocks.model_dump(exclude_unset=True, by_alias=True),
        block_id=new_page_result.id,
    )

    # delete the page we just created
    client.pages.update(page_id=new_page_result.id, archived=True)

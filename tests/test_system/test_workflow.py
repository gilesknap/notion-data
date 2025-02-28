"""
Some tests to experiment with how to make use of our Notion Data Model.
"""

from datetime import datetime
from pprint import pprint

from notion_data.block import Blocks, BlocksList
from notion_data.helpers import add_properties, file, paragraph, rich_text, title
from notion_data.identify import NotionUser
from notion_data.page import Icon, Page
from notion_data.parent import PageParent


def test_make_page(client, ids):
    page = Page(
        last_edited_time=datetime.now(),
        last_edited_by=NotionUser(id=ids.user_id),
        cover=file(url="https://www.notion.so/images/page-cover/webb2.jpg"),
        icon=Icon(emoji="🚀"),
        has_children=False,
        parent=(PageParent(page_id=ids.plain_page_id)),
        properties=add_properties(title=title("Generated Test Page")),
    )

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
    client.pages.update(page_id=new_page.id, in_trash=True)


def test_make_page_children(client, ids):
    p1 = paragraph(rich_text=rich_text("This is a rich text object"))
    p2 = paragraph(rich_text=rich_text("This is another rich text object"))
    p3 = paragraph(rich_text=rich_text("This is a third rich text object"))

    blocks = BlocksList([p1, p2, p3])

    page = Page(
        last_edited_time=datetime.now(),
        last_edited_by=NotionUser(id=ids.user_id),
        cover=file(url="https://www.notion.so/images/page-cover/webb2.jpg"),
        icon=Icon(emoji="🚀"),
        parent=(PageParent(page_id=ids.plain_page_id)),
        properties=add_properties(title=title("Generated Test Page with Blocks")),
    )

    # create the initial page
    result = client.pages.create(
        **page.model_dump(exclude_unset=True, by_alias=True),
    )
    new_page = Page(**result)

    # add the children to the page
    result = client.blocks.children.append(
        children=blocks.model_dump(exclude_unset=True, by_alias=True),
        block_id=new_page.id,
    )

    # fetch the page to see if the children were added
    result = client.blocks.children.list(block_id=new_page.id)
    blocks = Blocks(**result)

    pass
    # delete the page we just created
    # client.pages.update(page_id=new_page.id, in_trash=True)

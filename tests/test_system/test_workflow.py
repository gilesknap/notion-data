"""
Some tests to experiment with how to make use of our Notion Data Model.
"""

from datetime import datetime
from pprint import pprint

import pytest

from notion_data.block import Children
from notion_data.helpers import add_properties, file, rich_text, title
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


@pytest.mark.skip(reason="Children validate_python not yet working")
def test_make_page_children(client, ids):
    r1 = rich_text("This is a rich text object")
    r2 = rich_text("This is another rich text object")
    r3 = rich_text("This is a third rich text object")
    all = [r1, r2, r3]
    children = Children.validate_python(all)

    page = Page(
        last_edited_time=datetime.now(),
        last_edited_by=NotionUser(id=ids.user_id),
        cover=file(url="https://www.notion.so/images/page-cover/webb2.jpg"),
        icon=Icon(emoji="🚀"),
        parent=(PageParent(page_id=ids.plain_page_id)),
        properties=add_properties(title=title("Generated Test Page with Children")),
    )

    result = client.pages.create(
        **page.model_dump(exclude_unset=True, by_alias=True),
    )
    new_page = Page(**result)

    result = client.blocks.children.append(children=children, block_id=new_page.id)

    # delete the page we just created
    # client.pages.update(page_id=new_page.id, in_trash=True)

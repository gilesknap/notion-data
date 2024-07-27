"""
Some tests to experiment with how to make use of our Notion Data Model.
"""

from datetime import datetime
from pprint import pprint

from notion_data.helpers import add_properties, file, title
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

    assert page.icon.emoji == "🚀"
    assert not page.has_children

    pprint(page)
    pprint(page.model_dump(exclude_unset=True))
    pprint(page.cover)
    pprint(page.cover.model_dump(exclude_unset=True))

    result = client.pages.create(
        **page.model_dump(exclude_unset=True, by_alias=True),
    )

    # delete the page we just created
    new_page = Page(**result)
    client.pages.update(page_id=new_page.id, in_trash=True)

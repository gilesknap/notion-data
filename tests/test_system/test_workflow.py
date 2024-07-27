"""
Some tests to experiment with how to make use of our Notion Data Model.
"""

from datetime import datetime

from notion_data.file import FileExternal
from notion_data.identify import NotionUser
from notion_data.page import Icon, Page, TitleClass
from notion_data.parent import PageParent
from notion_data.rich_text import TextObject


def test_make_page(client, ids):
    page = Page(
        last_edited_time=datetime.now(),
        last_edited_by=NotionUser(id=ids.user_id),
        cover=FileExternal(external={"url": "http://example.com"}),
        icon=Icon(type="emoji", emoji="🚀"),
        has_children=False,
        parent=(PageParent(page_id=ids.plain_page_id)),
        properties={"title": TitleClass(title=[TextObject("Generated Test Page")])},
    )

    assert page.icon.emoji == "🚀"
    assert not page.has_children

    result = client.pages.create(
        parent=page.parent.model_dump(exclude_unset=True),
        properties=page.properties.model_dump(exclude_unset=True),
    )

    # delete the page we just created
    new_page = Page(**result)
    # client.pages.update(page_id=new_page.id, in_trash=True)

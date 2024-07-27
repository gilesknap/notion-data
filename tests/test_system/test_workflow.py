"""
Some tests to experiment with how to make use of our Notion Data Model.
"""

from datetime import datetime

from notion_data.file import FileExternal
from notion_data.identify import NotionUser
from notion_data.page import Icon, Page, TitleClass
from notion_data.parent import PageParent
from notion_data.rich_text import RichText


def test_make_page(client, ids):
    page = Page(
        last_edited_time=datetime.now(),
        last_edited_by=NotionUser(id=ids.user_id),
        cover=FileExternal(external={"url": "http://example.com"}),
        icon=Icon(type="emoji", emoji="🚀"),
        has_children=False,
        parent=(PageParent(page_id=ids.plain_page_id)),
        properties={"Title": TitleClass(title=[{"text": "example"}])},
    )

    assert page.cover.name == "example"
    assert page.icon.emoji == "🚀"
    assert page.has_children

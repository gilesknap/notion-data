from pprint import pprint

from notion_client import Client

from notion_data.helpers.api import encode_object
from notion_data.page import Page


def test_db_page(client: Client, ids):
    page_json = client.pages.retrieve(page_id=ids.database_child_page_id)
    pprint(page_json)

    page = Page.model_validate(page_json)

    # last TODO - use a Title object here to avoid the type: ignore
    rich_text = page.properties.Name.title[0].text  # type: ignore
    rich_text.content = "DB Page COPY. MADE by test_db_page()"

    args = encode_object(page)
    # make a copy of the page with the same properties
    result = client.pages.create(**args)

    # delete the page we just created
    new_page = Page.model_validate(result)
    client.pages.update(page_id=new_page.id, archived=True)


def test_plain_page(client, ids):
    page_json = client.pages.retrieve(page_id=ids.plain_page_id)
    pprint(page_json)

    page = Page.model_validate(page_json)

    rich_text = page.properties.title.title[0].text
    rich_text.content = "DB Page COPY. MADE by test_plain_page()"

    # make a copy of the page
    result = client.pages.create(**encode_object(page))

    # delete the page we just created
    new_page = Page(**result)
    client.pages.update(page_id=new_page.id, archived=True)

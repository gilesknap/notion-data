from pprint import pprint

from notion_client import Client

from notion_data.helpers.api import encode
from notion_data.helpers.properties import get_text_object, title
from notion_data.page import Page


# TODO we are going to get type errors for properties - can I do anything about that?
def test_db_page(client: Client, ids):
    # get a DB page from the server
    page_json = client.pages.retrieve(page_id=ids.database_child_page_id)
    pprint(page_json)
    page = Page.model_validate(page_json)

    # update the name of the database page
    old_title = get_text_object(page.properties.Name.title)  # type: ignore
    new_title = title(f"DB Page COPY (was {old_title.text.content})")
    page.properties.Name = new_title  # type: ignore

    # make a copy of the page with the same properties
    result = client.pages.create(**encode(page))

    # delete the page we just created
    new_page = Page.model_validate(result)
    client.pages.update(page_id=new_page.id, archived=True)


def test_plain_page(client, ids):
    # get a standard page from the server
    page_json = client.pages.retrieve(page_id=ids.plain_page_id)
    pprint(page_json)
    page = Page.model_validate(page_json)

    # update the title of the page
    old_title = get_text_object(page.properties.title.title)
    new_title = title(f"Test Page COPY (was {old_title.text.content})")
    page.properties.title = new_title

    # save a copy of the page to the server
    result = client.pages.create(**encode(page))

    # delete the page we just created
    new_page = Page(**result)
    client.pages.update(page_id=new_page.id, archived=True)

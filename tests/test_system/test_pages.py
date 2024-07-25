import os
from pprint import pprint

from notion_client import Client

from notion_data.dynamic import dict_model_instance
from notion_data.page import Page

secret = os.getenv("NOTION_SECRET")
database_page_id = "a53dc7f12ae7499d870f129299a3733b"
database_child_page_id = "eee59c60767348999403c4cd68279b46"
plain_page_id = "da6398fd210540919fc0bd70e33f18c7"
notion = Client(auth=secret)


def test_db_page():
    page_json = notion.pages.retrieve(page_id=database_child_page_id)
    pprint(page_json)

    page = Page(**page_json)
    pprint(page.model_dump())

    pprint(page.properties)
    properties = dict_model_instance("props", page.properties).model_dump()
    print()
    pprint(properties)
    pprint(page.parent.model_dump())

    # make a copy of the page
    # notion.pages.create(
    #     parent=page.root.parent.model_dump(),
    #     properties=properties.model_dump(),
    # )


def test_plain_page():
    page_json = notion.pages.retrieve(page_id=plain_page_id)
    pprint(page_json)

    page = Page(**page_json)

    parent = page.parent.model_dump()
    rich_text = page.properties["title"].title[0].text
    rich_text.content += " COPY. MADE by test_plain_page()"

    properties = dict_model_instance("props", page.properties).model_dump()

    pprint(properties)
    pprint(parent)

    # make a copy of the page
    result = notion.pages.create(
        parent=parent,
        properties=properties,
    )
    # delete the page we just created
    new_page = Page(**result)
    notion.pages.update(page_id=new_page.id, archived=True)

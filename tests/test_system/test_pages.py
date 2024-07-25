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

    # TODO still really struggling with getting properties to work
    # they have dynamic keys and so no model in code.
    # I cna use dic_model_instance to create a model at runtime but then
    # the below fails deserialising datetime

    # make a copy of the page
    # notion.pages.create(
    #     parent=page.root.parent.model_dump(),
    #     properties=properties.model_dump(),
    # )


def test_plain_page():
    page_json = notion.pages.retrieve(page_id=plain_page_id)
    pprint(page_json)

    page = Page(**page_json)
    pprint(page.model_dump())

    properties = page.properties
    print()
    pprint(properties)
    pprint(page.parent.model_dump())

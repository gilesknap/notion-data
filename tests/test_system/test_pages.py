import os
from pprint import pprint

from notion_client import Client

from notion_data.dynamic import dict_model_instance
from notion_data.page import Page

secret = os.getenv("NOTION_SECRET")
database_page_id = "a53dc7f12ae7499d870f129299a3733b"
database_child_page_id = "eee59c60767348999403c4cd68279b46"
notion = Client(auth=secret)


def test_db_page():
    page_json = notion.pages.retrieve(page_id=database_child_page_id)
    pprint(page_json)

    page = Page(page_json)
    pprint(page.model_dump())

    properties = dict_model_instance("PageProperties", page.root.properties)
    print()
    pprint(properties.model_dump())
    pprint(page.root.parent.model_dump())

    # TODO still really struggling with getting properties to work
    # they have dynamic keys and so no model in code.
    # I cna use dic_model_instance to create a model at runtime but then
    # the below fails deserialising datetime

    # make a copy of the page
    # notion.pages.create(
    #     parent=page.root.parent.model_dump(),
    #     properties=properties.model_dump(),
    # )

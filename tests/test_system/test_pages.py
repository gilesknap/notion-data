from pprint import pprint

from notion_client import Client

from notion_data.page import Page


# TODO need to eliminate the need for type: ignores
def test_db_page(client: Client, ids):
    page_json = client.pages.retrieve(page_id=ids.database_child_page_id)  # type: ignore
    pprint(page_json)

    page = Page(**page_json)  # type: ignore
    properties = page.properties
    # not allowed to set these - TODO helper should remove them from the model
    # TODO helper should also avoid type: ignore
    del properties.Created_time  # type: ignore
    del properties.Created_by  # type: ignore

    rich_text = page.properties.Name.title[0].text  # type: ignore
    rich_text.content += " COPY. MADE by test_db_page()"

    # make a copy of the page with the same properties
    result = client.pages.create(
        parent=page.parent.model_dump(),
        properties=properties.model_dump(by_alias=True),  # type: ignore
    )

    # delete the page we just created
    new_page = Page(**result)  # type: ignore
    client.pages.update(page_id=new_page.id, in_trash=True)


def test_plain_page(client, ids):
    page_json = client.pages.retrieve(page_id=ids.plain_page_id)
    pprint(page_json)

    page = Page(**page_json)

    rich_text = page.properties.title.title[0].text
    rich_text.content += " COPY. MADE by test_plain_page()"

    # make a copy of the page
    result = client.pages.create(
        parent=page.parent.model_dump(),
        properties=page.properties.model_dump(by_alias=True),
    )
    # delete the page we just created
    new_page = Page(**result)
    client.pages.update(page_id=new_page.id, in_trash=True)

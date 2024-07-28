import os
from pathlib import Path

import pytest
from notion_client import Client

# Prevent pytest from catching exceptions when debugging in vscode so that break on
# exception works correctly (see: https://github.com/pytest-dev/pytest/issues/7409)
if os.getenv("PYTEST_RAISE", "0") == "1":

    @pytest.hookimpl(tryfirst=True)
    def pytest_exception_interact(call):
        raise call.excinfo.value

    @pytest.hookimpl(tryfirst=True)
    def pytest_internalerror(excinfo):
        raise excinfo.value


@pytest.fixture
def data_folder():
    return Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def client():
    return Client(auth=os.getenv("NOTION_SECRET"))


@pytest.fixture
def ids():
    class Ids:
        database_page_id = "a53dc7f12ae7499d870f129299a3733b"
        database_child_page_id = "eee59c60767348999403c4cd68279b46"
        plain_page_id = "da6398fd210540919fc0bd70e33f18c7"
        block_id = "d91a45aac9d54c6f832bf3b2b871c4da"
        user_id = "cbb991ef-0db4-4c20-a298-ce5aad994d09"
        root_page_id = "8e0d8f87b513486f8a3cea085ce5c308"

    return Ids()

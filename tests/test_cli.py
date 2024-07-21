import subprocess
import sys

from notion_data import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "notion_data", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__

import subprocess
import sys

from notiondata import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "notiondata", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__

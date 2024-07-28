"""
Some simple types shared by pages and blocks
"""

from typing import Literal

from .root import Root


class Icon(Root):
    # TODO this needs to be a union of emoji and other things
    type: Literal["emoji"] = "emoji"
    emoji: str

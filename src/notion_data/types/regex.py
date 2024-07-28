"""
Some regex patterns for fields in the Notion API.
"""

from pydantic import Field

UUIDv4 = r"([0-9a-z]{8}(-[0-9a-z]{4}){3}-[0-9a-z]{12})|([0-9a-z]{27})"

ID: Field = Field(default=None, description="Identifier", pattern=UUIDv4)  # type: ignore

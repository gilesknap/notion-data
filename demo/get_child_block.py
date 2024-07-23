from pathlib import Path
from pprint import pprint

from notion_client import Client
from ruamel.yaml import YAML

from notion_data.block import Block

config_file = Path(__file__).parent / ".config.yaml"
config_txt = config_file.read_text()
config = YAML().load(config_txt)

notion = Client(auth=config.get("secret"))

block_json = notion.blocks.retrieve(block_id=config.get("block_id"))
pprint(block_json)
block = Block(**block_json)

children_json = notion.blocks.children.list(block_id=config.get("block_id"))
child2 = Block(**children_json["results"][0])

text = child2.root.paragraph.rich_text[0].text.content
print(text)

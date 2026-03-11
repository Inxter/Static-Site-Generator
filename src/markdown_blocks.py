from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered_list"
    OL = "ordered_list"

# Function to split markdown text into blocks based on double newlines
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    temp_list = []
    for block in blocks:
        if block == "":
            continue
        temp_list.append(block.strip())
    return temp_list

# Function to determine the block type of a given markdown block
def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") for line in block.split("\n")):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in block.split("\n")):
        return BlockType.UL
    elif all(re.match(r"^\d+\. ", line) for line in block.split("\n")):
        return BlockType.OL
    else:
        return BlockType.PARAGRAPH



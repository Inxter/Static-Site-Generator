import unittest

from functions import *
from markdown_blocks import *


class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_block_multiple_newlines(self):
        md = """
# This is a\nmeme header



- A list
- With an item

Just some text


What does this looks like ?
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a\nmeme header",
                "- A list\n- With an item",
                "Just some text",
                "What does this looks like ?"
            ]
        )

    # Heading assertion test
    def test_block_to_block_type_heading(self):
        heading = "### This is a heading"

        result = block_to_block_type(heading)

        self.assertEqual(result, BlockType.HEADING)
    # Code block assertion test
    def test_block_to_block_type_code(self):
        code = "```\nThis is a code block```"

        result = block_to_block_type(code)

        self.assertEqual(result, BlockType.CODE)
    # Quote block assertion test
    def test_block_to_block_type_quote(self):
        quote = "> This is a quote"

        result = block_to_block_type(quote)

        self.assertEqual(result, BlockType.QUOTE)
    # Unordered list assertion block
    def test_block_to_block_type_ul(self):
        ul = "- This is a quote\n- And a second quote"

        result = block_to_block_type(ul)

        self.assertEqual(result, BlockType.UL)
    # Ordered list assertion block
    def test_block_to_block_type_ol(self):
        ol = "1. This is a quote\n2. A second quote\n3. Third quote?"

        result = block_to_block_type(ol)

        self.assertEqual(result, BlockType.OL)
    # Paragraph block assertion test
    def test_block_to_block_type_paragraph(self):
        paragraph = "This is a normal paragraph with no special markdown syntax."

        result = block_to_block_type(paragraph)

        self.assertEqual(result, BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
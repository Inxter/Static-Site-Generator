import unittest

from functions import *
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_node_split_basic_bold(self):     
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(result,[
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ])

    def test_node_split_basic_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ])

    def test_node_split_basic_code(self):
        node = TextNode("This is `code` text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT)
        ])

    def test_node_split_non_text_node(self):
        node = TextNode("This is bold text", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(result, [
            TextNode("This is bold text", TextType.BOLD)
        ])

    def test_node_split_missing_closing_delimiter(self):
        node = TextNode("This is **bold text", TextType.TEXT)
        
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_node_split_multiple_bold_delimiters(self):     
        node = TextNode("This **is** additional **bold** text and a **bonus**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(result,[
            TextNode("This ", TextType.TEXT),
            TextNode("is", TextType.BOLD),
            TextNode(" additional ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text and a ", TextType.TEXT),
            TextNode("bonus", TextType.BOLD)
        ])

    def test_node_split_bold_and_missing_delimiter(self):   
        node = TextNode("This is **bold** text**", TextType.TEXT)
        
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_node_split_different_delimiters(self):
        node = TextNode("This is **bold** and _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], ["**", "_"], TextType.BOLD)

        self.assertEqual(result,[
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ])

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images_multiple(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ], new_nodes)
    
    def test_split_images_back_to_back(self):
        node = TextNode(
            "![img1](https://img.com/1.png)![img2](https://img.com/2.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "https://img.com/1.png"),
                TextNode("img2", TextType.IMAGE, "https://img.com/2.png"),
            ],
            new_nodes,
        )
    
    def test_split_images_identical_images(self):
        node = TextNode(
            "![img1](https://img.com/1.png)![img1](https://img.com/1.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "https://img.com/1.png"),
                TextNode("img1", TextType.IMAGE, "https://img.com/1.png"),
            ],
            new_nodes,
        )

    def test_split_images_identical_urls(self):
        node = TextNode(
            "![img1](https://img.com/1.png)![img2](https://img.com/1.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "https://img.com/1.png"),
                TextNode("img2", TextType.IMAGE, "https://img.com/1.png"),
            ],
            new_nodes,
        )
    

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_split_links_multiple(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ], new_nodes)

    def test_split_links_back_to_back(self):
        node = TextNode(
            "[Google](https://www.google.com)[YouTube](https://www.youtube.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Google", TextType.LINK, "https://www.google.com"),
                TextNode("YouTube", TextType.LINK, "https://www.youtube.com"),
            ],
            new_nodes,
        )

    def test_split_links_identical_links(self):
        node = TextNode(
            "[To Google](https://www.google.com)[To Google](https://www.google.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("To Google", TextType.LINK, "https://www.google.com"),
                TextNode("To Google", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )
class TestCombinationFunctions(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **bold** text, and some _italic_. Can't forget `a code block` with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.example.com)"
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text, and some ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(". Can't forget ", TextType.TEXT),
            TextNode("a code block", TextType.CODE),
            TextNode(" with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.example.com"),
        ])

    def test_text_to_textnodes_no_markdown(self):
        text = "This is plain text with no markdown."
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("This is plain text with no markdown.", TextType.TEXT),
        ])

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

        
if __name__ == "__main__":
    unittest.main()

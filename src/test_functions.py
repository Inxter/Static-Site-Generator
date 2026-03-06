import unittest

from functions import *
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestFunctions(unittest.TestCase):
    def test_node_split_basic_bold(self):
        
        node = TextNode("This is **bold** text", TextType.TEXT)

        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result,[
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ])







if __name__ == "__main__":
    unittest.main()

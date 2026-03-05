import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    # Test parameters
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.LINK, url="https://example.com")
        node2 = TextNode("This is a text node", TextType.LINK, url="https://different.com")
        self.assertNotEqual(node, node2)

    # Test initialization
    def test_init(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        self.assertEqual(node.text, "This is a text node")
        self.assertEqual(node.text_type, TextType.PLAIN.value)
        self.assertIsNone(node.url)

    # Test representation
    def test_repr(self):
        node = TextNode("This is a text node", TextType.CODE, url="https://example.com")
        expected= f"TextNode(This is a text node, `Code Text`, https://example.com)"
        self.assertEqual(repr(node), expected)

if __name__ == "__main__":
    unittest.main()
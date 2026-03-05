import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    # Tests for HTMLNode class
    def test_htmlnode_tag(self):
        node = HTMLNode(tag="a", value="Not suspicious link", props={"href": "https://www.boot.dev"})
        self.assertEqual(node.tag, "a")

    def test_htmlnode_value(self):
        node = HTMLNode(tag="a", value="Not suspicious link", props={"href": "https://www.boot.dev"})
        self.assertEqual(node.value, "Not suspicious link")

    def test_htmlnode_props(self):
        node = HTMLNode(tag="a", value="Not suspicious link", props={"href": "https://www.boot.dev"})
        self.assertEqual(node.props, {"href": "https://www.boot.dev"})
    
    def test_htmlnode_multiple_props(self):
        node = HTMLNode(tag="a", value="Not suspicious link", props={"href": "https://www.boot.dev", "target": "_blank"})
        result = node.props_to_html()

        self.assertIn('href="https://www.boot.dev"', result)
        self.assertIn('target="_blank"', result)
    
    def test_htmlnode_missing_children(self):
        node = HTMLNode(tag="a", value="Not suspicious link", props={"href": "https://www.boot.dev"})
        self.assertIsNone(node.children)
        
    def test_htmlnode_repr(self):
        node = HTMLNode(tag="a", value="Not suspicious link", props={"href": "https://www.boot.dev"})
        expected = f'HTMLNode(a, Not suspicious link, None, "{{\'href\': \'https://www.boot.dev\'}}")'
        self.assertEqual(repr(node), expected)

    # Tests for LeafNode class
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leafnode_no_tag(self):
        node = LeafNode(value="Not suspicious link", props={"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), "Not suspicious link")


if __name__ == "__main__":
    unittest.main()
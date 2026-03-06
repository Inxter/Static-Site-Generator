import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_to_html_not_implemented_error(self):
        node = HTMLNode(tag="div")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    # Tests for LeafNode class

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leafnode_no_tag(self):
        node = LeafNode(value="Not suspicious link", props={"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), "Not suspicious link")

    def test_leafnode_requires_value(self):
        with self.assertRaises(ValueError):
            LeafNode(tag="p", props={"href": "https://www.boot.dev"})

    def test_leafnode_multiple_props(self):
        node = LeafNode("a", "Click me", props={"href": "https://www.boot.dev", "target": "_blank"})
        result = node.to_html()
        self.assertIn('href="https://www.boot.dev"', result)
        self.assertIn('target="_blank"', result)

    # Tests for ParentNode class

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parentnode_requires_tag(self):
        child = LeafNode("div", "Child")
        node = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parentnode_requires_children(self):
        node = ParentNode("div", None, props={"href": "https://www.boot.dev"})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parentnode_nested_children(self):
        child4 = LeafNode("i", "Child4")
        child3 = ParentNode("b", [child4])
        child2 = LeafNode("p", "Child2")
        child1 = ParentNode("span", [child3, child2])
        node = ParentNode("div", [child1])

        self.assertEqual(
            node.to_html(), "<div><span><b><i>Child4</i></b><p>Child2</p></span></div>"
        )

if __name__ == "__main__":
    unittest.main()
import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(),' href="https://www.google.com"')

    def test_eq_mul(self):
        node1 = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node1.props_to_html(),' href="https://www.google.com" target="_blank"')

    def test_eq_none(self):
        node2 = HTMLNode(props=None)
        self.assertEqual(node2.props_to_html(), "")

if __name__ == "__main__":
    unittest.main()

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node1 = LeafNode("a", "Hello, world!")
        self.assertEqual(node1.to_html(),"<a>Hello, world!</a>")
    
    def test_leaf_to_html_a_href(self):
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node2.to_html(),"<a href=\"https://www.google.com\">Click me!</a>")
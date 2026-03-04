import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(None, None, None, {"href": "https://www.google.com", "target": "_blank"})
        result = f' href="https://www.google.com" target="_blank"' 
        self.assertEqual(node.props_to_html(), result)

    def test_none(self):
        node = HTMLNode()
        result = ""
        self.assertEqual(node.props_to_html(), result)

    def test_init(self):
        node = HTMLNode("h1", "Hello")
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_none_Tag(self):
        node = LeafNode(None, "value")
        self.assertEqual(node.to_html(), "value")
        

if __name__ == "__main__":
    unittest.main()
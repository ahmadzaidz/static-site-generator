import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
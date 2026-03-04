import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("this is a text node", TextType.BOLD)
        node2 = TextNode("this is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_text(self):
        node = TextNode("this is a text node", TextType.PLAIN)
        node2 = TextNode("this is a different text node", TextType.PLAIN)
        self.assertNotEqual(node, node2)
    
    def test_one_url(self):
        node = TextNode("this is a text node", TextType.LINK, "www.google.com")
        node2 = TextNode("this is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)
    
    def test_eq_url(self):
        node = TextNode("this is a text node", TextType.LINK, "www.google.com")
        node2 = TextNode("this is a text node", TextType.LINK, "www.google.com")
        self.assertEqual(node, node2)
    
    def test_plain(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic")

    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")

    def test_link(self):
        node = TextNode("Click here", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_invalid_type_raises(self):
        node = TextNode("oops", None)
        with self.assertRaises(Exception):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
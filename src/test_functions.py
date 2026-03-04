import unittest
from functions import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.PLAIN),
            ],
            new_nodes,
        )
    
    def test_delim_bold(self):
        node = TextNode("This is text with two **bolded words**.", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with two ", TextType.PLAIN),
                TextNode("bolded words", TextType.BOLD),
                TextNode(".", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_delim_italics(self):
        node = TextNode("_Italics at the start_ and _at the end_", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("Italics at the start", TextType.ITALIC),
                TextNode(" and ", TextType.PLAIN),
                TextNode("at the end", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_chained(self):
            node = TextNode("_Italics at the start_ and **bold** after", TextType.PLAIN)
            italic_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
            final_nodes = split_nodes_delimiter(italic_nodes, "**", TextType.BOLD)
            self.assertListEqual(
                [
                    TextNode("Italics at the start", TextType.ITALIC),
                    TextNode(" and ", TextType.PLAIN),
                    TextNode("bold", TextType.BOLD),
                    TextNode(" after", TextType.PLAIN),
                ],
                final_nodes,
            )

    
    def test_delim_invalid(self):
        node = TextNode("I opened a `code but never closed it", TextType.PLAIN)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)
         
    
if __name__ == "__main__":
    unittest.main()
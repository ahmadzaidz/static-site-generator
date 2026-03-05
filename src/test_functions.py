import unittest
from functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_both(self):
        text = "[a link](www.google.com) at the start and at the end an ![image](image.png)"
        img_match = extract_markdown_images(text)
        link_match = extract_markdown_links(text)
        self.assertListEqual([("a link", "www.google.com")], link_match)
        self.assertListEqual([("image", "image.png")], img_match)

    def test_extract_markdown_none(self):
        text = "this text has no image or link"
        img_match = extract_markdown_images(text)
        link_match = extract_markdown_links(text)
        self.assertListEqual([], link_match)
        self.assertListEqual([], img_match)

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
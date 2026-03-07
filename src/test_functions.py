import unittest
from functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType

class TestTexttoTextNodes(unittest.TestCase):
    def test_all_types(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(text_to_textnodes(text), 
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )
    def test_empty(self):
        self.assertListEqual([], text_to_textnodes(""))

    def test_not_closed(self):
        text = "**Forgot to close the bold but put a ![image](image.png) anyway"
        with self.assertRaises(Exception):
            text_to_textnodes(text)

class TestSplitNodes(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://wikipedia.org) with text that follows",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.PLAIN),
                TextNode("another link", TextType.LINK, "https://wikipedia.org"),
                TextNode(" with text that follows", TextType.PLAIN),
            ],
            new_nodes,
        )


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
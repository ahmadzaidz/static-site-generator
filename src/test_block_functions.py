import unittest
from block_functions import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node

class TestBlocktoHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

class TestBlockTypes(unittest.TestCase):
    # Dash without a space should not be a list
    def test_ulist_no_space(self):
        block = "-item\n-item"
        self.assertEqual(block_to_block_type(block), BlockType.PARA)

    # Mixed: one line missing the dash
    def test_ulist_mixed(self):
        block = "- item\nitem"
        self.assertEqual(block_to_block_type(block), BlockType.PARA)

    # Numbering that doesn't start at 1
    def test_olist_wrong_start(self):
        block = "2. item\n3. item"
        self.assertEqual(block_to_block_type(block), BlockType.PARA)

    # Numbering that skips a number
    def test_olist_skipped_number(self):
        block = "1. item\n3. item"
        self.assertEqual(block_to_block_type(block), BlockType.PARA)

    # One line without > makes the whole block a paragraph
    def test_quote_mixed(self):
        block = "> quote\nnot a quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARA)

    # Max valid heading (6 hashes)
    def test_heading_max_level(self):
        block = "###### heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    # 7 hashes should NOT be a heading
    def test_heading_too_many_hashes(self):
        block = "####### not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARA)

    # Hash without a trailing space is not a heading
    def test_heading_no_space(self):
        block = "#notaheading"
        self.assertEqual(block_to_block_type(block), BlockType.PARA)

    # Single-line code block (no newline between backticks) should NOT be code
    def test_code_no_newline(self):
        block = "```code```"
        self.assertEqual(block_to_block_type(block), BlockType.PARA)

    def test_block_type_paragraph(self):
        block = "something that doesnt have anything at all" 
        self.assertEqual(block_to_block_type(block), BlockType.PARA

        )
    def test_block_type_heading(self):
        block = "#### this is a heading" 
        self.assertEqual(block_to_block_type(block), BlockType.HEADING

        )

    def test_block_type_code(self):
        block = """```
some code
```""" 
        self.assertEqual(block_to_block_type(block), BlockType.CODE

        )

    def test_block_type_quote(self):
        block = """> a multi
> lined
> quote""" 
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE

        )

    def test_block_type_unordered(self):
        block = """- an unordered
- list
- here""" 
        self.assertEqual(block_to_block_type(block), BlockType.BULLET

        )

    def test_block_type_ordered(self):
        block = """1. an ordered
2. list
3. here""" 
        self.assertEqual(block_to_block_type(block), BlockType.LIST

        )
class TestMarkdowntoBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        # there are extra spaces in one of the new lines
        md = """
This is **bolded** paragraph

    


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
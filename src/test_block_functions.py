import unittest
from block_functions import BlockType, markdown_to_blocks, block_to_block_type

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
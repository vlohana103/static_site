import unittest
from markdown_blocks import markdown_to_block, block_to_block_type, BlockType, extract_title
from textnode import TextNode, TextType

class TestMarkdownToHtml(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """

        blocks = markdown_to_block(md)
        self.assertEqual(
            blocks,
            [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
            ],
        )

    def test_excessive_spaces(self):
        md = """
# This is a title



This is a new paragraph with to many new lines below it




- This is a list item
    """

        blocks = markdown_to_block(md)
        self.assertEqual(
            blocks,
            [
                "# This is a title",
                "This is a new paragraph with to many new lines below it",
                "- This is a list item",
            ],
        )


class TestBlockType(unittest.TestCase):
    def test_heading(self):
        block = "### this is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code(self):
        block = "```\nthis is code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = "> this is a quote\n> second line of quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_ordered_list_success(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_fail(self):
        # This should fail because it skips a number (1 to 3)
        block = "1. first\n3. second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph(self):
        block = "This is just a normal paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_no_h1(self):
        with self.assertRaises(Exception):
            extract_title("No heading here")
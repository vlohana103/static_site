from textnode import TextNode, TextType
from enum import Enum
from htmlnode import ParentNode, LeafNode, text_node_to_html_node
from inline_markdown import text_to_textnodes

def markdown_to_block(markdown):
    result = []
    pieces = markdown.split("\n\n")
    for i in pieces:
        stripped = i.strip()
        if stripped != "":
            result.append(stripped)
    return result

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split("\n")

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith(("- ","* ")) for line in lines):
        return BlockType.UNORDERED_LIST

    if lines[0].startswith("1. "):
        is_ordered = True
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i+1}. "):
                is_ordered = False
                break
        if is_ordered:
            return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)

    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html(text_node)
        children.append(html_node)
    return children

def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        lines = block.split("\n")
        paragraph = " ".join(lines)
        return ParentNode("p", text_to_children(paragraph))
    
    if block_type == BlockType.HEADING:
        level = 0
        for char in block:
            if char == "#":
                level += 1
            else:
                break
        text = block[level + 1:]
        return ParentNode(f"h{level}", text_to_children(text))

    if block_type == BlockType.CODE:
        text = block[3:-3].strip("\n")
        code_node = ParentNode("code", [LeafNode(None, text)])
        return ParentNode("pre", [code_node])

    if block_type == BlockType.QUOTE:
        lines = block.split("\n")
        cleaned_lines = [line.lstrip(">").strip() for line in lines]
        text = " ".join(cleaned_lines)
        return ParentNode("blockquote", text_to_children(text))


    if block_type == BlockType.UNORDERED_LIST:
        lines = block.split("\n")
        li_nodes = []
        for line in lines:
            text = line[2:]
            li_nodes.append(ParentNode("li", text_to_children(text)))
        return ParentNode("ul", li_nodes)

    if block_type == BlockType.ORDERED_LIST:
        lines = block.split("\n")
        li_nodes = []
        for line in lines:
            text = line[line.find(" ") + 1:]
            li_nodes.append(ParentNode("li", text_to_children(text)))
        return ParentNode("ol", li_nodes)




def markdown_to_html_node(markdown):
    blocks = markdown_to_block(markdown)

    block_nodes = []
    for block in blocks:
        node = block_to_html_node(block)
        block_nodes.append(node)

    return ParentNode("div", block_nodes)
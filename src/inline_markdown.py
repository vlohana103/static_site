from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    results = []
    for i in old_nodes:
        if i.text_type != TextType.TEXT:
            results.append(i)
        else:
            split = i.text.split(delimiter)
            if len(split) % 2 == 0:
                raise Exception("invalid Markdown syntax")
            else:
                for j in range(0, len(split)):
                    if split[j] == "":
                        continue
                    if j % 2 == 0:
                        results.append(TextNode(split[j], TextType.TEXT))
                    else:
                        results.append(TextNode(split[j], text_type))
    return results


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        extracted = extract_markdown_images(node.text)
        if len(extracted) == 0:
            result.append(node)
            continue
        remaining = node.text
        for alt, url in extracted:
            sections = remaining.split(f"![{alt}]({url})", 1)
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.TEXT))
            result.append(TextNode(alt, TextType.IMAGE, url))
            remaining = sections[1]
        if remaining != "":
            result.append(TextNode(remaining, TextType.TEXT))
    return result

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        
        remaining_text = node.text
        for anchor, url in links:
            sections = remaining_text.split(f"[{anchor}]({url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            remaining_text = sections[1]
            
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            
    return new_nodes



def text_to_textnodes(text):
    # Start with a single node containing the raw text
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Chain the splitting functions
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

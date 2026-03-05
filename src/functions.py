from textnode import TextNode, TextType
import re

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    split_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.PLAIN:
            split_nodes.append(node)
            continue
        node_parts = []
        split_text = node.text.split(delimiter)
        
        if (len(split_text) % 2) == 0:
            raise Exception("invalid markdown")
        for i in range(0, len(split_text)):
            if split_text[i] == "":
                continue
            if (i % 2) == 0:
                node_parts.append(TextNode(split_text[i], TextType.PLAIN))
            else:
                node_parts.append(TextNode(split_text[i], text_type))
        
        
        split_nodes.extend(node_parts)
    return split_nodes
                
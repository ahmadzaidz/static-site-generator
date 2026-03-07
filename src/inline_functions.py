from textnode import TextNode, TextType
import re

def text_to_textnodes(text):
    original_node = TextNode(text, TextType.PLAIN)
    bolded = split_nodes_delimiter((split_nodes_link(split_nodes_image([original_node]))), "**", TextType.BOLD)
    coded = split_nodes_delimiter(bolded, "`", TextType.CODE)
    final = split_nodes_delimiter(coded, "_", TextType.ITALIC)
    return final

def split_nodes_image(old_nodes):
    split_nodes = []
    for node in old_nodes:
        if node.text == "":
            continue
        if node.text_type != TextType.PLAIN:
            split_nodes.append(node)
            continue

        original_text = node.text
        images = extract_markdown_images(original_text)

        if len(images) == 0:
            split_nodes.append(node)
            continue

        for image in images:
            image_alt = image[0]
            image_link = image[1]
            # Split once at the first occurrence of this specific image
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)
            
            if len(sections) != 2:
                raise ValueError("INvalid markdown, image section not closed")


            # Add the text before the image if it's not empty
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.PLAIN))
            
            # Add the image node itself
            split_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            
            # Continue searching the remaining text
            original_text = sections[1]
            
        # Add any remaining text after the last image
        if original_text != "":
            split_nodes.append(TextNode(original_text, TextType.PLAIN))
            
    return split_nodes


def split_nodes_link(old_nodes):
    split_nodes = []
    for node in old_nodes:
        if node.text == "":
            continue
        if node.text_type != TextType.PLAIN:
            split_nodes.append(node)
            continue

        original_text = node.text
        links = extract_markdown_links(original_text)

        if len(links) == 0:
            split_nodes.append(node)
            continue

        for link in links:
            link_text = link[0]
            link_url = link[1]
            # Split once at the first occurrence of this specific image
            sections = original_text.split(f"[{link_text}]({link_url})", 1)
            
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")


            # Add the text before the link if it's not empty
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.PLAIN))
            
            # Add the link node itself
            split_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            
            # Continue searching the remaining text
            original_text = sections[1]
            
        # Add any remaining text after the last image
        if original_text != "":
            split_nodes.append(TextNode(original_text, TextType.PLAIN))
            
    return split_nodes

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
                
from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_functions import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARA = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    BULLET = "unordered_list"
    LIST = "ordered_list"

def markdown_to_html_node(markdown):
    #Split the markdown into blocks (you already have a function for this)
    blocks = markdown_to_blocks(markdown)
    all_blocks = []
    for block in blocks:
        block_type = block_to_block_type(block)
        
        match (block_type):
            case BlockType.PARA:
                block = block.replace("\n", " ")
                node = ParentNode("p", text_to_children(block))
            case BlockType.HEADING:
                count = 0
                for char in block:
                    if char == "#":
                        count += 1
                    else:
                        break
                block = block.lstrip("#"*count).strip()
                node = ParentNode(f"h{count}", text_to_children(block))
            case BlockType.QUOTE:
                lines = block.splitlines()
                new_lines = []
                for line in lines:
                    new_lines.append(line.lstrip(">").strip())
                block = " ".join(new_lines)
                node = ParentNode("blockquote", text_to_children(block))
            case BlockType.BULLET:
                node = ParentNode("ul", children_list_nodes(block))
            case BlockType.LIST:
                node = ParentNode("ol", children_list_nodes(block))
            case BlockType.CODE:
                block = block[4:-3]  # removes opening ```\n and closing ```
                content = TextNode(block, TextType.PLAIN) 
                node = ParentNode("pre", [ParentNode("code", [text_node_to_html_node(content)])])
            case _:
                raise Exception("blocktype not valid")
        all_blocks.append(node)
    return ParentNode("div", all_blocks)
        

        

# Make all the block nodes children under a single parent HTML node (which should just be a div) and return it.
  

def text_to_children(text):
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        children.append(text_node_to_html_node(node))
    return children

def children_list_nodes(list_block):
    block_type = block_to_block_type(list_block)
    if block_type not in (BlockType.BULLET, BlockType.LIST):
        raise Exception("not a list")
    lines = list_block.splitlines()
    children = []
    for line in lines:
        if block_type == BlockType.BULLET:
            list_node = ParentNode("li", text_to_children(line[2:]))
            children.append(list_node)
        if block_type == BlockType.LIST:
            #index [1] grabs the string from the list returned by .split
            list_node = ParentNode("li", text_to_children(line.split(". ", 1)[1]))
            children.append(list_node)
    return children


def block_to_block_type(block):
    if block.startswith("# ") or block.startswith("## ") or block.startswith("### ") or block.startswith("#### ") or block.startswith("##### ") or block.startswith("###### "):
        return BlockType.HEADING
    elif block[:4] == """```
""" and block[-3:] == "```":
        return BlockType.CODE
    if block.startswith(">"):
        split = block.splitlines()
        is_quote = True
        for line in split:
            if not line.startswith(">"):
                is_quote = False
                break
        if is_quote is True:
            return BlockType.QUOTE
    if block.startswith("- "):
            split = block.splitlines()
            is_list = True
            for line in split:
                 if not line.startswith("- "):
                      is_list = False
                      break
            if is_list is True:
                 return BlockType.BULLET
    if block.startswith("1. "):
        split = block.splitlines()
        is_list = True
        for i in range(len(split)):
            if not split[i].startswith(f"{i+1}. "):
                is_list = False
                break
        if is_list is True:
            return BlockType.LIST
    
    return BlockType.PARA
    


def markdown_to_blocks(document):
    blocks = document.split("\n\n")
    result = []
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        result.append(block)
    return result

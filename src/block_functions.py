from enum import Enum

class BlockType(Enum):
    PARA = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    BULLET = "unordered_list"
    LIST = "ordered_list"

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

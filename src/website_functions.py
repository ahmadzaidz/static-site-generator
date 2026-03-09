import os, shutil
from block_functions import markdown_to_html_node
from htmlnode import HTMLNode

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    all_content = os.listdir(dir_path_content)
    
    for content in all_content:
        from_path = os.path.join(dir_path_content, content)
        to_path = os.path.join(dest_dir_path, content)
        if os.path.isfile(from_path) and from_path[-3:] == ".md":
            generate_page(from_path, template_path, f"{to_path[:-3]}.html")
        elif os.path.isdir(from_path):
            os.makedirs(to_path, exist_ok=True)
            generate_pages_recursive(from_path, template_path, to_path)


def generate_page(from_path, template_path, dest_path):
    print (f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        src = f.read()
    with open(template_path) as f:
        tem = f.read()
    content = markdown_to_html_node(src)
    content = content.to_html()
    title = extract_title(src)
    tem = tem.replace("{{ Title }}", title)
    tem = tem.replace("{{ Content }}", content)
    if os.path.dirname(dest_path) != "": 
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(tem)
    

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            title = line.lstrip("#").strip()
            return title
    raise Exception("No title found")


def prepare_and_copy(source_dir, dest_dir):
    source_dir_abs = os.path.abspath(source_dir)
    dest_dir_abs = os.path.abspath(dest_dir)
    if not os.path.exists(source_dir_abs):
        raise Exception(f'Error: Directory dont exist')
    if not os.path.isdir(source_dir_abs):
        raise Exception("Error: not directory")
    if os.path.exists(dest_dir_abs):
        shutil.rmtree(dest_dir_abs)
    os.mkdir(dest_dir_abs)
    return copy_source_to_dest(source_dir, dest_dir)

def copy_source_to_dest(source_dir, dest_dir):
    source_dir_abs = os.path.abspath(source_dir)
    dest_dir_abs = os.path.abspath(dest_dir)
    print(f"copying from {source_dir_abs} to {dest_dir_abs}")
    list_dir = os.listdir(source_dir_abs)
    for item in list_dir:
        dest_path = os.path.join(dest_dir_abs, item)
        src_path = os.path.join(source_dir_abs, item)
        print(f" * {src_path} -> {dest_path}", flush=True)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        if os.path.isdir(src_path):
            os.mkdir(dest_path)
            copy_source_to_dest(src_path, dest_path)



"""
os.path.abspath(): Get an absolute path from a relative path
os.path.join(): Join two paths together safely (handles slashes)
os.path.normpath(): Normalize a path (handles things like ..)
os.path.commonpath(): Get the common sub-path shared by multiple paths
os.listdir(): List the contents of a directory
os.path.isdir(): Check if a path points to an existing directory
os.path.isfile(): Check if a path points to an existing regular file
os.path.getsize(): Get the size of a file (in bytes)
.join(): Join a list of strings together with a given separator
"""
import os, shutil

def prepare_and_copy(source_dir, dest_dir):
    source_dir_abs = os.path.abspath(source_dir)
    dest_dir_abs = os.path.abspath(dest_dir)
    if not os.path.exists(source_dir_abs):
        raise Exception(f'Error: Directory dont exist')
    if not os.path.isdir(source_dir_abs):
        raise Exception("Error: not directory")
    shutil.rmtree(dest_dir_abs)
    os.mkdir(dest_dir_abs)
    copy_source_to_dest(source_dir, dest_dir)

def copy_source_to_dest(source_dir, dest_dir):
    source_dir_abs = os.path.abspath(source_dir)
    dest_dir_abs = os.path.abspath(dest_dir)
    list_dir = os.listdir(source_dir_abs)
    for item in list_dir:
        dest_path = os.path.join(dest_dir_abs, item)
        src_path = os.path.join(source_dir_abs, item)
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
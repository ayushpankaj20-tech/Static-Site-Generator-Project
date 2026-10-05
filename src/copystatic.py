import os
import shutil

def copy_files_recursively(src_dir, dest_dir):
    """
    Recursively copy files from src_dir to dest_dir.
    """

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for item in os.listdir(src_dir):
        s = os.path.join(src_dir, item)
        d = os.path.join(dest_dir, item)
        if os.path.isdir(s):
            copy_files_recursively(s, d)
        else:
            shutil.copy2(s, d)

def copy_static_files(src_dir, dest_dir):
    """
    Copy static files from src_dir to dest_dir.
    This function can be used to copy static assets like CSS, JS, images, etc.
    """

    if not os.path.exists(src_dir):
        raise ValueError(f"Source directory '{src_dir}' does not exist.")

    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    os.makedirs(dest_dir)
    

    copy_files_recursively(src_dir, dest_dir)
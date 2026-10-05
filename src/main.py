from textnode import TextType, TextNode
from copystatic import copy_static_files
from gencontent import generate_page, generate_pages_recursive
import sys

def main():

    basepath = #
    
    # Example usage of copy_static_files
    src_directory = f"{basepath}/static"
    dest_directory = f"{basepath}/public"
    
    try:
        copy_static_files(src_directory, dest_directory)
        print(f"Static files copied from '{src_directory}' to '{dest_directory}'.")
    except ValueError as e:
        print(e)
    
    # Example usage of generate_page
    generate_pages_recursive(f"{basepath}/content", f"{basepath}/template.html", f"{basepath}/public")

main()
  
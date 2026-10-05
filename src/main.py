from textnode import TextType, TextNode
from copystatic import copy_static_files
from gencontent import generate_page, generate_pages_recursive
import sys

def main():

    basepath = "/"
    if len(sys.argv) > 1:   
        basepath = sys.argv[1]

    # Example usage of copy_static_files
    src_directory = "./static"
    dest_directory = "./docs"
    
    try:
        copy_static_files(src_directory, dest_directory)
        print(f"Static files copied from '{src_directory}' to '{dest_directory}'.")
    except ValueError as e:
        print(e)
    
    # Example usage of generate_page
    generate_pages_recursive("content", "template.html", "docs", basepath)
main()
  
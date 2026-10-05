from utils import read_file
import os
from inline_markdown import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    page_content = read_file(from_path)
    template_content = read_file(template_path)
    title = extract_title(page_content)
    html_content = markdown_to_html_node(page_content)
    some_content = html_content.to_html()  # Assuming html_content is a ParentNode or similar object with a to_html method
    final_content = template_content.replace("href={basepath}", title).replace("src={basepath}", some_content)
    
    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)
    
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)
        if os.path.isdir(from_path):
            generate_pages_recursive(from_path, template_path, dest_path)
        elif entry.endswith('.md'):
            dest_path = os.path.splitext(dest_path)[0] + '.html'
            generate_page(from_path, template_path, dest_path)

    

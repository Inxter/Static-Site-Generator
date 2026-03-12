import os
from functions import markdown_to_html_node
from htmlnode import ParentNode

# Function to recursively delete items and directories
def recursive_deletion(path):
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            recursive_deletion(item_path)
        os.rmdir(path)

# Function to copy a directory from Static to Public, ensuring that the destination directory is clean before copying
def recursive_dir_copy(src, dest):
    workspace = "/home/inxter/workspace/inxter/Static-Site-Generator"
    src_path = os.path.join(workspace, src)
    dest_path = os.path.join(workspace, dest)

    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Source path '{src}' does not exist.")
    # Remove the destination directory if it already exists to ensure a clean copy
    if os.path.exists(dest_path):
        recursive_deletion(dest_path)   

    if os.path.isfile(src_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        with open(src_path, "rb") as f_src:
            data = f_src.read()
        with open(dest_path, "wb") as f_dest:
            f_dest.write(data)

    elif os.path.isdir(src_path):
        os.makedirs(dest_path, exist_ok=True)
        for item in os.listdir(src_path):
            item_src = os.path.join(src, item)
            item_dest = os.path.join(dest, item)

            recursive_dir_copy(item_src, item_dest)

def extract_title(markdown):
    html_node = markdown_to_html_node(markdown)
    for child in html_node.children:
        if isinstance(child, ParentNode) and child.tag == "h1":
            return child.children[0].value
    raise ValueError("No h1 heading found in the markdown to extract title from")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    node = markdown_to_html_node(markdown)
    html_content = node.to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content)

    with open(dest_path, "w") as f:
        f.write(template)

    # Generate HTML
    #test = markdown_to_html_node(markdown)
    #test_content = test.to_html()

    # Print the entire HTML (or just the blockquote)
    #print(test_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        item_content_path = os.path.join(dir_path_content, item)
        item_dest_path = os.path.join(dest_dir_path, item.replace(".md", ".html"))
        if os.path.isfile(item_content_path) and item_content_path.endswith(".md"):
            generate_page(item_content_path, template_path, item_dest_path)
        elif os.path.isdir(item_content_path):
            os.makedirs(item_dest_path, exist_ok=True)
            generate_pages_recursive(item_content_path, template_path, item_dest_path)
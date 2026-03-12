from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from functions import *
from website_functions import *
import os
import shutil
import sys


basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)
    
    dir_path_static = "./static"
    dir_path_public = "./docs"
    dir_path_content = "./content"
    template_path = "./template.html"

    # Copy static files to public directory
    recursive_dir_copy(dir_path_static, dir_path_public)
    # Generate page from markdown and template
    generate_pages_recursive(basepath, dir_path_content, template_path, dir_path_public)



if __name__ == "__main__":
    main()

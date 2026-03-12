from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from functions import *
from website_functions import *
import os
import shutil


def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)

    dir_path_static = "./static"
    dir_path_public = "./public"
    dir_path_content = "./content"
    template_path = "./template.html"

    # Copy static files to public directory
    recursive_dir_copy(dir_path_static, dir_path_public)
    # Generate page from markdown and template
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)



if __name__ == "__main__":
    main()

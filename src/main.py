from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from functions import *

print("Hello world!")

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)
        

main()
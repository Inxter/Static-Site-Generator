from textnode import TextNode
from textnode import TextType

print("Hello world!")

def main():
    node = TextNode("This is some anchor text", TextType.link_text, "https://www.boot.dev")
    print(node)

main()
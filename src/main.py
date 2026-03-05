from textnode import TextNode
from textnode import TextType

print("Hello world!")

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)

main()
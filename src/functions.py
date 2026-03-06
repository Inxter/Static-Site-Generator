from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

# This file contains functions that are used in the main.py file.


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, props={"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Unsupported text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    accepted_delimiters = {
        "**": TextType.BOLD,
        "_": TextType.ITALIC,
        "`": TextType.CODE,
    }
    # Normalize delimiters to a list in case there are multiple
    if isinstance(delimiter, str):
        delimiter = [delimiter]

    # List of processed nodes to be returned by the function
    new_nodes = []

    # Process old nodes
    for node in old_nodes:
        # Filter out non-TEXT type nodes immediately
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # List of nodes to be extended into the new nodes
        current_nodes = [node]

        for d in delimiter:
            # Placeholder for processed nodes
            temp_nodes = []
            for curr in current_nodes:
            # Filter and append nodes that are not of type TEXT or don't have the delimiter in them in case they are already processed      
                if curr.text_type != TextType.TEXT or d not in curr.text:
                    temp_nodes.append(curr)
                    continue

                # Split current node into a list of strings
                parts = curr.text.split(d)

                # Unmatched delimiter
                if len(parts) % 2 == 0:
                    raise ValueError(f"Error: Unmatched delimiter '{d}' in '{curr.text}'")
                for index, part in enumerate(parts):
                    # Skip empty nodes
                    if not part:
                        continue
                    # Odd index means the part is between delimiters
                    if index % 2 == 1:
                        temp_nodes.append(TextNode(part, accepted_delimiters[d]))
                    else:
                        temp_nodes.append(TextNode(part, TextType.TEXT))
            # Update current nodes to processed nodes from the loop
            current_nodes = temp_nodes
        # Add the list of processed nodes to be returned
        new_nodes.extend(current_nodes)
    return new_nodes
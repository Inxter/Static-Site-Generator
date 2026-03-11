from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type
import re

# This file contains functions

# Function to convert a TextNode to an HTMLNode based on its type
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

# Function to split a list of TextNodes based on a delimiter and assign the appropriate text type to the split parts
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


# Helper functions to extract markdown images and links from text using regular expressions
def extract_markdown_images(text):
    result = []
    matches = re.findall(r"!\[([^\]]+)\]\(([^\)]+)\)", text)
    
    result.extend(matches)
    return result

def extract_markdown_links(text):
    result = []
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    result.extend(matches)
    return result

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        temp_string = node.text
        if not images:
            new_nodes.append(node)
            continue      
        for img_part in images:
            alt, url = img_part
            parts = temp_string.split(f"![{alt}]({url})", 1)          
            if len(parts) != 2:
                raise ValueError(f"Error: Invalid markdown syntax, image syntax incorrect")
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            temp_string = parts[1]
        if temp_string != "":
            new_nodes.append(TextNode(temp_string, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        temp_string = node.text
        if not links:
            new_nodes.append(node)
            continue      
        for link_part in links:
            alt, url = link_part
            parts = temp_string.split(f"[{alt}]({url})", 1)          
            if len(parts) != 2:
                raise ValueError(f"Error: Invalid markdown syntax, link syntax incorrect")
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, url))
            temp_string = parts[1]
        if temp_string != "":
            new_nodes.append(TextNode(temp_string, TextType.TEXT))
    return new_nodes

# Combination function to convert text to text nodes and split them based on markdown syntax for images and links
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

# Function to find the appropriate HTML tag for a given markdown block type
def block_to_html_tag(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return "p"
    if block_type == BlockType.HEADING:
        for i in range(1, 7):
            if block.startswith("#" * i + " "):
                return f"h{i}"
    if block_type == BlockType.CODE:
        return "pre"
    if block_type == BlockType.QUOTE:
        return "blockquote"
    if block_type == BlockType.UL:
        return "ul"
    if block_type == BlockType.OL:
        return "ol"

# Extract text from block
def extract_text_from_block(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.HEADING:
        return block.lstrip("#").strip()
    if block_type == BlockType.CODE:
        if block.startswith("```\n") and block.endswith("```"):
            return block[4:-3]
        else:
            return block
    if block_type == BlockType.QUOTE:
        lines = block.split("\n")
        return [line.lstrip(">").strip() for line in lines if line.startswith(">")]
    if block_type == BlockType.UL:
        lines = []
        for line in block.split("\n"):
            if line.startswith("- "):
                lines.append(line.lstrip("- ").strip())
        return lines
    if block_type == BlockType.OL:
        lines = []
        for line in block.split("\n"):
            match = re.match(r"^\d+\. ", line)
            if match:
                lines.append(line[match.end():].strip())
        return lines
    if block_type == BlockType.PARAGRAPH:
        return " ".join(line.strip() for line in block.split("\n"))
    return block.strip()

# Helper function to convert a list of TextNodes into a list of children HTMLNodes
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

# Helper function to convert Markdown blocks into Parent and Child nodes
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    html_tag = block_to_html_tag(block)
    # text is a list for UL and OL
    text = extract_text_from_block(block)
    if block_type in [BlockType.PARAGRAPH, BlockType.HEADING]:
        children = text_to_children(text)
        parent_node = ParentNode(html_tag, children)
        return parent_node
    if block_type == BlockType.QUOTE:
        children_nodes = [ParentNode("p", text_to_children(line)) for line in text]
        return ParentNode(html_tag, children_nodes)
    if block_type == BlockType.CODE:
        # For code blocks, we want to preserve the newlines and spacing, so we use a LeafNode with a pre tag
        child_node = LeafNode("code", text)
        parent_node = ParentNode(html_tag, [child_node])
        return parent_node
    if block_type in [BlockType.UL, BlockType.OL]:
        list_items = []
        for item in text:
            children = text_to_children(item)
            list_items.append(ParentNode("li", children))
        return ParentNode(html_tag, list_items)
    

# Function to convert a full markdown document into a tree of HTMLNodes
def markdown_to_html_node(markdown):
    # Markdown into blocks
    markdown_blocks = markdown_to_blocks(markdown)
    # Blocks into HTMLNodes
    nodes = []
    for block in markdown_blocks:
        nodes.append(block_to_html_node(block))

    return ParentNode("div", nodes)

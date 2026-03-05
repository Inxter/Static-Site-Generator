from enum import Enum

class TextType(Enum):
    PLAIN = "Plain Text"
    BOLD = "**Bold Text**"
    ITALIC = "_Italic Text_"
    CODE = "`Code Text`"
    LINK = "[anchor text](URL)"
    IMAGE = "![alt text](image URL)"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type.value
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (self.text == other.text 
            and self.text_type == other.text_type 
            and self.url == other.url)
            
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"



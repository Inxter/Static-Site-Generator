class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method must be implemented by subclasses/childclasses")

    def props_to_html(self):
        if self.props is not None:
            return f" {' '.join(f'{key}=\"{value}\"' for key, value in self.props.items())}"
        return ""
        
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, "{self.props}")'

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        
    def test_leafnode_requires_value(self):
        with self.assertRaises(ValueError):
            LeafNode(tag="p")
        
    def to_html(self):    
        if self.tag is None:
            return f"{self.value}"
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, "{self.props}")'
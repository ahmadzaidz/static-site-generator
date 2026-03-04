class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        result = ""
        for prop in self.props:
            result += f' {prop}="{self.props[prop]}"'     
        return result
    def __repr__(self):

        return f"HTMLNode tag:{self.tag}, value:{self.value}, children:{self.children}, props:{self.props_to_html()}"
"""
An HTMLNode without a tag will just render as raw text
An HTMLNode without a value will be assumed to have children
An HTMLNode without children will be assumed to have a value
An HTMLNode without props simply won't have any attributes
"""

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
        
    
    def to_html(self):
        if self.value is None:
            raise ValueError
        if not self.tag:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode tag:{self.tag}, value:{self.value}, props:{self.props_to_html()}"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError
        if self.children == {}:
            raise ValueError("no children")
        html = ""
        for node in self.children:
            html += node.to_html()
        return f"<{self.tag}>{html}</{self.tag}>"   


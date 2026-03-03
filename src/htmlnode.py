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

        return f"HTMLNode tag:{self.tag}, value:{self.value}, children:{self.children}, props:{self.props.html()}"
"""
An HTMLNode without a tag will just render as raw text
An HTMLNode without a value will be assumed to have children
An HTMLNode without children will be assumed to have a value
An HTMLNode without props simply won't have any attributes
"""
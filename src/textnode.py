import unittest
from enum import Enum
from htmlnode import LeafNode, ParentNode

class TextType(Enum):
    TEXT = "text"
    LINK = "link"
    IMAGE = "image"
    BOLD = "bold"
    ITALIC = "italic" 
    CODE = "code"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, other):
        if isinstance(other, TextNode):
            return self.text == other.text and self.text_type == other.text_type and self.url == other.url
        return False
    def __repr__(self):
        return f"TextNode(text={self.text}, text_type={self.text_type}, url={self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value=None, props={"src": text_node.url, "alt": text_node.text})
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    else:
        raise ValueError(f"Unsupported text type: {text_node.text_type}")

class TestTextNodeToHTMLNode(unittest.TestCase):
    
    def test_text(self):
        text_node = TextNode("Hello, World!", TextType.TEXT)
        html_node = TextNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Hello, World!")
        self.assertEqual(html_node.props, None)

    def test_link(self):
        text_node = TextNode("Click here", TextType.LINK, url="https://example.com")
        html_node = TextNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        text_node = TextNode("Example image", TextType.IMAGE, url="https://example.com/image.png")
        html_node = TextNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "https://example.com/image.png", "alt": "Example image"})

    def test_bold(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = TextNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.props, None)

    def test_italic(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = TextNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.props, None)

    def test_code(self):
        text_node = TextNode("Code text", TextType.CODE)
        html_node = TextNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code text")
        self.assertEqual(html_node.props, None)

    def test_image(self):
        text_node = TextNode("Example image", TextType.IMAGE, url="https://example.com/image.png")
        html_node = TextNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "https://example.com/image.png", "alt": "Example image"})
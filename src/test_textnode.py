import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(text=This is a text node, text_type=TextType.BOLD, url=None)")
    def test_inequality(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_url(self):
        node = TextNode("This is a link", TextType.LINK, url="https://example.com")
        node2 = TextNode("This is a link", TextType.LINK, url="https://example.com")
        self.assertEqual(node, node2)
    def test_url_inequality(self):
        node = TextNode("This is a link", TextType.LINK, url="https://example.com")
        node2 = TextNode("This is a link", TextType.LINK, url="https://different.com")
        self.assertNotEqual(node, node2)
    def test_repr_with_url(self):
        node = TextNode("This is a link", TextType.LINK, url="https://example.com")
        self.assertEqual(repr(node), "TextNode(text=This is a link, text_type=TextType.LINK, url=https://example.com)")
    def test_repr_with_none_url(self):
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        self.assertEqual(repr(node), "TextNode(text=This is a text node, text_type=TextType.BOLD, url=None)")   


if __name__ == "__main__":
    unittest.main()

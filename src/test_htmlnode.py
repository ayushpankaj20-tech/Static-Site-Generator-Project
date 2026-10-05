import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(props= None)
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_repr(self):
        node = HTMLNode(props={})
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_props_to_html_with_props(self):
        node = HTMLNode(props={"class": "my-class"})
        result = node.props_to_html()
        self.assertEqual(result, ' class="my-class"')

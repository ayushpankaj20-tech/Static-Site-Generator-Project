from enum import Enum
import re
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode, LeafNode

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError("The text node does not contain the specified delimiter.")
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

def split_nodes_delimiter_with_url(old_nodes: list[TextNode], delimiter: str, text_type: TextType, url: str) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError("The text node does not contain the specified delimiter.")
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type, url=url))
    return new_nodes

def extract_markdown_images(text):
    import re
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

    matches = re.findall(pattern, text)
    images = []
    for alt_text, url in matches:
        images.append(TextNode(alt_text, TextType.IMAGE, url=url))
    return images

def extract_markdown_links(text):
    import re
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    links = []
    for link_text, url in matches:
        links.append(TextNode(link_text, TextType.LINK, url=url))
    return links

def test_extract_markdown_images(self):
    text = "Here is an image: ![alt text](https://example.com/image.png)"
    images = extract_markdown_images(text)
    self.assertEqual(len(images), 1)
    self.assertEqual(images[0].text, "alt text")
    self.assertEqual(images[0].text_type, TextType.IMAGE)
    self.assertEqual(images[0].url, "https://example.com/image.png")

def test_extract_markdown_links(self):
    text = "Here is a link: [link text](https://example.com)"
    links = extract_markdown_links(text)
    self.assertEqual(len(links), 1)
    self.assertEqual(links[0].text, "link text")
    self.assertEqual(links[0].text_type, TextType.LINK)
    self.assertEqual(links[0].url, "https://example.com")

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        remaining = node.text
        for image in images:
            delimiter = f"![{image.text}]({image.url})"
            before, after = remaining.split(delimiter, 1)
            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(image)
            remaining = after
        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        remaining = node.text
        for link in links:
            delimiter = f"[{link.text}]({link.url})"
            before, after = remaining.split(delimiter, 1)
            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(link)
            remaining = after
        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes

def test_split_images(self):
    text_node = TextNode("Here is an image: ![alt text](https://example.com/image.png)", TextType.TEXT)
    new_nodes = split_nodes_image([text_node])
    self.assertEqual(len(new_nodes), 2)
    self.assertEqual(new_nodes[0].text, "Here is an image: ")
    self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
    self.assertEqual(new_nodes[1].text, "alt text")
    self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
    self.assertEqual(new_nodes[1].url, "https://example.com/image.png")

def test_split_links(self):
    text_node = TextNode("Here is a link: [link text](https://example.com)", TextType.TEXT)
    new_nodes = split_nodes_link([text_node])
    self.assertEqual(len(new_nodes), 2)
    self.assertEqual(new_nodes[0].text, "Here is a link: ")
    self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
    self.assertEqual(new_nodes[1].text, "link text")
    self.assertEqual(new_nodes[1].text_type, TextType.LINK)
    self.assertEqual(new_nodes[1].url, "https://example.com")

def test_split_images_and_links(self):
    text_node = TextNode("Here is an image: ![alt text](https://example.com/image.png) and a link: [link text](https://example.com)", TextType.TEXT)
    new_nodes = split_nodes_image([text_node])
    new_nodes = split_nodes_link(new_nodes)
    self.assertEqual(len(new_nodes), 4)
    self.assertEqual(new_nodes[0].text, "Here is an image: ")
    self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
    self.assertEqual(new_nodes[1].text, "alt text")
    self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
    self.assertEqual(new_nodes[1].url, "https://example.com/image.png")
    self.assertEqual(new_nodes[2].text, " and a link: ")
    self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    self.assertEqual(new_nodes[3].text, "link text")
    self.assertEqual(new_nodes[3].text_type, TextType.LINK)
    self.assertEqual(new_nodes[3].url, "https://example.com")

def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    return new_nodes

def test_text_to_textnodes(self):
    text = "This is **bold** text, this is _italic_ text, and this is `code`."
    new_nodes = text_to_textnodes(text)
    self.assertEqual(len(new_nodes), 7)
    self.assertEqual(new_nodes[0].text, "This is ")
    self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
    self.assertEqual(new_nodes[1].text, "bold")
    self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
    self.assertEqual(new_nodes[2].text, " text, this is ")
    self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    self.assertEqual(new_nodes[3].text, "italic")
    self.assertEqual(new_nodes[3].text_type, TextType.ITALIC)
    self.assertEqual(new_nodes[4].text, " text, and this is ")
    self.assertEqual(new_nodes[4].text_type, TextType.TEXT)
    self.assertEqual(new_nodes[5].text, "code")
    self.assertEqual(new_nodes[5].text_type, TextType.CODE)
    self.assertEqual(new_nodes[6].text, ".")
    self.assertEqual(new_nodes[6].text_type, TextType.TEXT)

def test_text_to_textnodes_with_images_and_links(self):
    text = "This is an image: ![alt text](https://example.com/image.png) and a link: [link text](https://example.com)"
    new_nodes = text_to_textnodes(text)
    self.assertEqual(len(new_nodes), 4)
    self.assertEqual(new_nodes[0].text, "This is an image: ")
    self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
    self.assertEqual(new_nodes[1].text, "alt text")
    self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
    self.assertEqual(new_nodes[1].url, "https://example.com/image.png")
    self.assertEqual(new_nodes[2].text, " and a link: ")
    self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    self.assertEqual(new_nodes[3].text, "link text")
    self.assertEqual(new_nodes[3].text_type, TextType.LINK)
    self.assertEqual(new_nodes[3].url, "https://example.com")

def test_text_to_textnodes_with_all_features(self):
    text = "This is **bold** text, this is _italic_ text, this is `code`, this is an image: ![alt text](https://example.com/image.png) and this is a link: [link text](https://example.com)"
    new_nodes = text_to_textnodes(text)
    self.assertEqual(len(new_nodes), 11)
    self.assertEqual(new_nodes[0].text, "This is ")
    self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
    self.assertEqual(new_nodes[1].text, "bold")
    self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
    self.assertEqual(new_nodes[2].text, " text, this is ")
    self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    self.assertEqual(new_nodes[3].text, "italic")
    self.assertEqual(new_nodes[3].text_type, TextType.ITALIC)
    self.assertEqual(new_nodes[4].text, " text, this is ")
    self.assertEqual(new_nodes[4].text_type, TextType.TEXT)
    self.assertEqual(new_nodes[5].text, "code")
    self.assertEqual(new_nodes[5].text_type, TextType.CODE)
    self.assertEqual(new_nodes[6].text, ", this is an image: ")
    self.assertEqual(new_nodes[6].text_type, TextType.TEXT)
    self.assertEqual(new_nodes[7].text, "alt text")
    self.assertEqual(new_nodes[7].text_type, TextType.IMAGE)
    self.assertEqual(new_nodes[7].url, "https://example.com/image.png")
    self.assertEqual(new_nodes[8].text, " and this is a link: ")
    self.assertEqual(new_nodes[8].text_type, TextType.TEXT)
    self.assertEqual(new_nodes[9].text, "link text")
    self.assertEqual(new_nodes[9].text_type, TextType.LINK)
    self.assertEqual(new_nodes[9].url, "https://example.com")

def markdown_to_blocks(markdown):
    lines = markdown.splitlines()
    blocks = []
    current_block_lines = []
    for line in lines:
        if line.strip() == "":
            if current_block_lines:
                blocks.append("\n".join(current_block_lines))
                current_block_lines = []
        else:
            current_block_lines.append(line)
    if current_block_lines:
        blocks.append("\n".join(current_block_lines))
    return blocks

def test_markdown_to_blocks(self):
    markdown = """This is a paragraph.
"""
    blocks = markdown_to_blocks(markdown)
    self.assertEqual(len(blocks), 1)
    self.assertEqual(blocks[0], "This is a paragraph.")

def test_markdown_to_blocks_with_multiple_paragraphs(self):
    markdown = """This is the first paragraph.
"""
    blocks = markdown_to_blocks(markdown)
    self.assertEqual(len(blocks), 2)
    self.assertEqual(blocks[0], "This is the first paragraph.")

def test_markdown_to_blocks_with_empty_lines(self):
    markdown = """This is the first paragraph.
"""
    blocks = markdown_to_blocks(markdown)
    self.assertEqual(len(blocks), 3)
    self.assertEqual(blocks[0], "This is the first paragraph.")

class BlockType(Enum):
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
    H6 = "h6"
    BLOCKQUOTE = "blockquote"
    UL = "ul"
    OL = "ol"
    P = "p"
    CODE = "code"

def block_to_block_type(block):
    if block.startswith("```"):
        return BlockType.CODE
    elif block.startswith("# "):
        return BlockType.H1
    elif block.startswith("## "):
        return BlockType.H2 
    elif block.startswith("### "):
        return BlockType.H3
    elif block.startswith("#### "):
        return BlockType.H4
    elif block.startswith("##### "):
        return BlockType.H5
    elif block.startswith("###### "):
        return BlockType.H6
    elif block.startswith(">"):
        return BlockType.BLOCKQUOTE
    elif re.match(r"^(\*|\-|\+) ", block):
        return BlockType.UL
    elif re.match(r"^\d+\. ", block):
        return BlockType.OL
    else:
        return BlockType.P

def test_block_to_block_type(self):
    self.assertEqual(block_to_block_type("# Heading 1"), BlockType.H1)
    self.assertEqual(block_to_block_type("## Heading 2"), BlockType.H2)
    self.assertEqual(block_to_block_type("### Heading 3"), BlockType.H3)
    self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.H4)
    self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.H5)
    self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.H6)
    self.assertEqual(block_to_block_type("> This is a blockquote."), BlockType.BLOCKQUOTE)
    self.assertEqual(block_to_block_type("* This is an unordered list item."), BlockType.UL)
    self.assertEqual(block_to_block_type("- This is an unordered list item."), BlockType.UL)
    self.assertEqual(block_to_block_type("+ This is an unordered list item."), BlockType.UL)
    self.assertEqual(block_to_block_type("1. This is an ordered list item."), BlockType.OL)
    self.assertEqual(block_to_block_type("This is a paragraph."), BlockType.P)

def test_block_to_block_type_with_empty_block(self):
    self.assertEqual(block_to_block_type(""), BlockType.P)

def test_block_to_block_type_with_whitespace_block(self):
    self.assertEqual(block_to_block_type("   "), BlockType.P)

def test_block_to_block_type_with_non_markdown_block(self):
    self.assertEqual(block_to_block_type("This is a non-markdown block."), BlockType.P)

HEADINGS = {
    BlockType.H1, BlockType.H2, BlockType.H3,
    BlockType.H4, BlockType.H5, BlockType.H6,
}

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        tag = block_type.value
        if block_type in HEADINGS:
            level = int(tag[1])
            text = block[level + 1:]
        elif block_type == BlockType.BLOCKQUOTE:
            text = block.split(">")
            result = "".join([t.strip() for t in text if t.strip()])
            text = result
        elif block_type == BlockType.UL:
            li_nodes = []
            for line in block.split("\n"):
                item_text = line[2:]
                leaves = [text_node_to_html_node(tn) for tn in text_to_textnodes(item_text)]
                li_nodes.append(ParentNode("li", leaves))
            html_nodes.append(ParentNode("ul", li_nodes))
            continue
        elif block_type == BlockType.OL:
            li_nodes = []
            for line in block.split("\n"):
                item_text = line[3:]
                leaves = [text_node_to_html_node(tn) for tn in text_to_textnodes(item_text)]
                li_nodes.append(ParentNode("li", leaves))
            html_nodes.append(ParentNode("ol", li_nodes))
            continue
        elif block_type == BlockType.CODE:
            text = block.strip("`").lstrip("\n")
            code_leaf = LeafNode("code", text)
            html_nodes.append(ParentNode("pre", [code_leaf]))
            continue
        else:
            tag = "p"
            text = block
        leaves = [text_node_to_html_node(tn) for tn in text_to_textnodes(text)]
        html_nodes.append(ParentNode(tag, leaves))
    return ParentNode("div", html_nodes)

def test_paragraph_to_html_node(self):
    markdown = "This is a paragraph."
    html_nodes = markdown_to_html_node(markdown)
    self.assertEqual(len(html_nodes), 1)
    self.assertEqual(html_nodes[0][0], BlockType.P)
    self.assertEqual(len(html_nodes[0][1]), 1)
    self.assertEqual(html_nodes[0][1][0].text, "This is a paragraph.")
    self.assertEqual(html_nodes[0][1][0].text_type, TextType.TEXT)

def test_heading_to_html_node(self):
    markdown = "# This is a heading."
    html_nodes = markdown_to_html_node(markdown)
    self.assertEqual(len(html_nodes), 1)
    self.assertEqual(html_nodes[0][0], BlockType.H1)
    self.assertEqual(len(html_nodes[0][1]), 1)
    self.assertEqual(html_nodes[0][1][0].text, "This is a heading.")
    self.assertEqual(html_nodes[0][1][0].text_type, TextType.TEXT)

def test_blockquote_to_html_node(self):
    markdown = "> This is a blockquote."
    html_nodes = markdown_to_html_node(markdown)
    self.assertEqual(len(html_nodes), 1)
    self.assertEqual(html_nodes[0][0], BlockType.BLOCKQUOTE)
    self.assertEqual(len(html_nodes[0][1]), 1)
    self.assertEqual(html_nodes[0][1][0].text, "This is a blockquote.")
    self.assertEqual(html_nodes[0][1][0].text_type, TextType.TEXT)

def test_unordered_list_to_html_node(self):
    markdown = "* This is an unordered list item."
    html_nodes = markdown_to_html_node(markdown)
    self.assertEqual(len(html_nodes), 1)
    self.assertEqual(html_nodes[0][0], BlockType.UL)
    self.assertEqual(len(html_nodes[0][1]), 1)
    self.assertEqual(html_nodes[0][1][0].text, "This is an unordered list item.")
    self.assertEqual(html_nodes[0][1][0].text_type, TextType.TEXT)

def test_ordered_list_to_html_node(self):
    markdown = "1. This is an ordered list item."
    html_nodes = markdown_to_html_node(markdown)
    self.assertEqual(len(html_nodes), 1)
    self.assertEqual(html_nodes[0][0], BlockType.OL)
    self.assertEqual(len(html_nodes[0][1]), 1)
    self.assertEqual(html_nodes[0][1][0].text, "This is an ordered list item.")
    self.assertEqual(html_nodes[0][1][0].text_type, TextType.TEXT)

def extract_title(markdown):
    if not markdown:
        raise ValueError("The markdown string is empty.")
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.H1:
            return block[2:].strip()
    raise ValueError("No title found in the markdown string.")

def test_extract_title(self):
    markdown = "# This is a title\n\nThis is a paragraph."
    title = extract_title(markdown)
    self.assertEqual(title, "This is a title")

def test_extract_title_h2_only(self):
    markdown = "## Not a title\n\nSome paragraph."
    with self.assertRaises(ValueError):
        extract_title(markdown)

def test_extract_title_with_no_title(self):
    markdown = "This is a paragraph.\n\nThis is another paragraph."
    with self.assertRaises(ValueError):
        extract_title(markdown)

def test_extract_title_with_empty_markdown(self):
    markdown = ""
    with self.assertRaises(ValueError):
        extract_title(markdown)

def test_extract_title_with_whitespace_markdown(self):
    markdown = "   "
    with self.assertRaises(ValueError):
        extract_title(markdown)



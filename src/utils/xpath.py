import bs4.element

XPATH = "/"
COMMENT = "comment()"
NAVIGABLE_STRING = "text()"


def get_node_xpath(node: bs4.element.Tag | bs4.element.Comment) -> str:
    elements = [_node_to_xpath(node)]
    for parent in node.parents:
        if parent.name != "[document]":
            elements.append(_node_to_xpath(parent))
    return f"{XPATH}{XPATH.join(reversed(elements))}"


def _node_to_xpath(node: bs4.element.Tag | bs4.element.Comment) -> str:
    node_strings = {
        bs4.element.Tag: getattr(node, "name"),
        bs4.element.Comment: COMMENT,
        bs4.element.NavigableString: NAVIGABLE_STRING,
    }
    same_type_siblings = list(
        node.parent.find_all(
            lambda element:
            getattr(node, "name", True) == getattr(element, "name", False),
            recursive=False
        )
    )
    if len(same_type_siblings) > 1:
        index = same_type_siblings.index(node) + 1
        return f"{node_strings[type(node)]}[{index}]"
    return node_strings[type(node)]

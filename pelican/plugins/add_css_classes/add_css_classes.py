from typing import Dict, Iterable, Union

from bs4 import BeautifulSoup
from pelican import contents, signals
from pelican.contents import Content

ADD_CSS_CLASSES_KEY = "ADD_CSS_CLASSES"


ClassAttributeReplacements = Iterable[
    Dict[
        str,
        Union[Iterable[str], Dict[str, Union[Iterable[str], Dict[str, Iterable[str]]]]],
    ]
]


def add_css_classes_for_selector(
    content: BeautifulSoup, selector: str, classes: Iterable[str]
):
    for item in content.select(selector):
        attribute_set = item.attrs.get("class", []) + list(classes)
        item.attrs["class"] = list(attribute_set)


def add_css_classes(content: str, replacements: ClassAttributeReplacements) -> str:
    """Adds css classes to elements found in the content for the
    given selectors in the replacements

    Args:
        content: The content containing elements that needs classes to be added
        replacements: An iterable of classes to be added to the `class` attribute
            of the found html element

    Returns: content with the added class attributes
    """
    if not isinstance(replacements, list):
        raise ValueError(f"{ADD_CSS_CLASSES_KEY} must be a list")

    soup: BeautifulSoup = BeautifulSoup(content, "html.parser")

    for replacement in replacements:
        add_css_classes_for_selector(
            soup, replacement["element_name"], replacement["classes"]
        )

    return soup.decode()


def pelican_add_css_classes(content: Content):
    if isinstance(content, contents.Static):
        return

    replacements: ClassAttributeReplacements = content.settings.get(ADD_CSS_CLASSES_KEY)

    if replacements:
        content._content = add_css_classes(content._content, replacements)


def register():
    signals.content_object_init.connect(pelican_add_css_classes)

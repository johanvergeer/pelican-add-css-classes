from typing import Iterable, NamedTuple

from bs4 import BeautifulSoup
from pelican import contents, signals
from pelican.contents import Content

ADD_CSS_CLASSES_KEY = "ADD_CSS_CLASSES"


class ClassAttributeReplacement(NamedTuple):
    """Contains a selector to find an element
    and classes that should be added to the `class`
    attribute of the element

    Attributes:
        selector: The selector for the html element the css classes should be added to.
        classes: A list of css class names to add to the `class` attribute
            of the html element found by the selector
    """

    selector: str
    classes: Iterable[str]


def add_css_classes_for_selector(
    content: BeautifulSoup, selector: str, classes: Iterable[str]
):
    for item in content.select(selector):
        attribute_set = item.attrs.get("class", []) + list(classes)
        item.attrs["class"] = list(attribute_set)


def add_css_classes(
    content: str, replacements: Iterable[ClassAttributeReplacement]
) -> str:
    """Adds css classes to elements found in the content for the
    given selectors in the replacements

    Args:
        content: The content containing elements that needs classes to be added
        replacements: An iterable of classes to be added to the `class` attribute
            of the found html element

    Returns: content with the added class attributes
    """
    soup: BeautifulSoup = BeautifulSoup(content, "html.parser")

    for selector, classes in replacements:
        add_css_classes_for_selector(soup, selector, classes)

    return soup.decode()


def pelican_add_css_classes(content: Content):
    if isinstance(content, contents.Static):
        return

    replacements = content.settings.get(ADD_CSS_CLASSES_KEY)

    if replacements:
        content._content = add_css_classes(content._content, replacements)


def register():
    signals.content_object_init.connect(pelican_add_css_classes)

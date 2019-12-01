from typing import Dict, Iterable, Optional

from bs4 import BeautifulSoup
from pelican import contents, signals
from pelican.contents import Content

ADD_CSS_CLASSES_KEY = "ADD_CSS_CLASSES"
ADD_CSS_CLASSES_TO_PAGE_KEY = "ADD_CSS_CLASSES_TO_PAGE"
ADD_CSS_CLASSES_TO_ARTICLE_KEY = "ADD_CSS_CLASSES_TO_ARTICLE"
PELICAN_PAGE = "pelican_page"
PELICAN_ARTICLE = "pelican_article"

ClassAttributeReplacements = Dict[str, Iterable[str]]


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
    if not isinstance(replacements, dict):
        raise ValueError(f"{ADD_CSS_CLASSES_KEY} must be a dict")

    soup: BeautifulSoup = BeautifulSoup(content, "html.parser")

    for element, classes in replacements.items():
        add_css_classes_for_selector(soup, element, classes)

    return soup.decode()


def merge_replacements(
    replacements: ClassAttributeReplacements,
    page_replacements: Optional[ClassAttributeReplacements],
    article_replacements: Optional[ClassAttributeReplacements],
    content_type: str,
):
    if content_type not in ("pelican_page", "pelican_article"):
        raise ValueError(
            f'content_type must be "{PELICAN_PAGE}" or "{PELICAN_ARTICLE}".'
        )

    result = replacements.copy()

    if page_replacements and content_type == PELICAN_PAGE:
        result.update(page_replacements)

    if article_replacements and content_type == PELICAN_ARTICLE:
        result.update(article_replacements)

    return result


def pelican_add_css_classes(content: Content):
    if isinstance(content, contents.Static):
        return

    replacements: ClassAttributeReplacements = merge_replacements(
        content.settings.get(ADD_CSS_CLASSES_KEY),
        content.settings.get(ADD_CSS_CLASSES_TO_PAGE_KEY),
        content.settings.get(ADD_CSS_CLASSES_TO_ARTICLE_KEY),
        PELICAN_PAGE if isinstance(content, contents.Page) else PELICAN_ARTICLE,
    )

    if replacements and len(replacements):
        content._content = add_css_classes(content._content, replacements)


def register():
    signals.content_object_init.connect(pelican_add_css_classes)

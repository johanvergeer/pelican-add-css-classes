from bs4 import BeautifulSoup
from plugins.add_css_classes import (
    ClassAttributeReplacements,
    add_css_classes,
    add_css_classes_for_selector,
    merge_replacements,
)
import pytest


@pytest.fixture
def content() -> str:
    return """
    <html>
        <head>
        </head>
        <body>
            <table>
                <th>
                    <td>col1</td>
                    <td>col2</td>
                    <td>col3</td>
                </th>
                <tr>
                    <td>value 1</td>
                    <td>value 2</td>
                    <td>value 3</td>
                </tr>
            </table>
        </body>
    </html>
    """


def soupify(content: str) -> BeautifulSoup:
    return BeautifulSoup(content, "html.parser")


@pytest.fixture
def soup(content: str) -> BeautifulSoup:
    return soupify(content)


@pytest.fixture
def replacements() -> ClassAttributeReplacements:
    return {"table": ["table", "table-fluid"]}


def test_add_css_classes_for_selector(soup):
    add_css_classes_for_selector(soup, "table", ["table", "table-fluid"])
    assert soup.select("table")[0].attrs.get("class") == ["table", "table-fluid"]


def test_add_css_classes(content, replacements):
    result = add_css_classes(content, replacements)

    assert soupify(result).select("table")[0].attrs.get("class") == [
        "table",
        "table-fluid",
    ]


def test_merge_replacements__invalid_content_type__raises(replacements):
    with pytest.raises(ValueError) as ex:
        merge_replacements(replacements, None, None, "foo")

    assert str(ex.value) == 'content_type must be "pelican_page" or "pelican_article".'


def test_merge_replacements_flat():
    replacements = {"table": ["table", "table-fluid"]}
    expected = {"table": ["table", "table-fluid"]}

    result = merge_replacements(replacements, None, None, "pelican_page")

    assert result == expected


def test_merge_replacements__page_with_extra_element_name():
    replacements = {
        "table": ["table", "table-fluid"],
    }
    page_replacements = {"div": ["page_div_class"]}
    article_replacements = {"p": ["article_p_class"]}

    expected = {"table": ["table", "table-fluid"], "div": ["page_div_class"]}

    result = merge_replacements(
        replacements, page_replacements, article_replacements, "pelican_page"
    )

    assert result == expected


def test_merge_replacements__article_with_extra_element_name():
    replacements = {
        "table": ["table", "table-fluid"],
    }
    page_replacements = {"div": ["page_div_class"]}
    article_replacements = {"p": ["article_p_class"]}

    expected = {"table": ["table", "table-fluid"], "p": ["article_p_class"]}

    result = merge_replacements(
        replacements, page_replacements, article_replacements, "pelican_article"
    )

    assert result == expected

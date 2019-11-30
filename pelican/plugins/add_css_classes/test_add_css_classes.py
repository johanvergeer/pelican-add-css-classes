from typing import Iterable

from bs4 import BeautifulSoup
from plugins.add_css_classes import (
    ClassAttributeReplacement,
    add_css_classes,
    add_css_classes_for_selector,
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
def replacements() -> Iterable[ClassAttributeReplacement]:
    return (("table", ("table", "table-fluid")),)


def test_add_css_classes_for_selector(soup):
    add_css_classes_for_selector(soup, "table", ["table", "table-fluid"])
    assert soup.select("table")[0].attrs.get("class") == ["table", "table-fluid"]


def test_add_css_classes(content, replacements):
    result = add_css_classes(content, replacements)

    assert soupify(result).select("table")[0].attrs.get("class") == [
        "table",
        "table-fluid",
    ]

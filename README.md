# Add css classes: A Plugin for Pelican

Adds CSS classes to html tags in Pelican documents

## Motivation

When we want to create a page or article we often use Markdown or RST. This allows us to
write content very fast, but it gives us little to no control over the styling of our page.

That is why I created this plugin for Pelican so we can add classes to HTML elements
inside `pelicanconf.py`.

## Usage

__Be aware that this plugin only changes the html that is generated from Markdown!__.
HTML from templates is not changed.

### Both pages and articles

To set css classes that should be added to elements in both
pages and articles you can use `ADD_CSS_CLASSES`.

You can also set which css classes should be added to elements
on pages with `ADD_CSS_CLASSES_TO_PAGE`.

And this can also be done with articles using `ADD_CSS_CLASSES_TO_ARTICLE`.

#### Example

Let's say you want to configure all tables to use Bootstrap, show black tables on pages
and red headers on articles.

```python
ADD_CSS_CLASSES = {
    "table": ["table"]
}

ADD_CSS_CLASSES_TO_PAGE = {
    "table": ["table", "table-dark"]
}

ADD_CSS_CLASSES_TO_ARTICLE = {
    "h1": ["text-danger"]
}
```

Installation
------------

This plugin can be installed via:

    pip install pelican-add-css-classes

Contributing
------------

Contributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].

To start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.

[existing issues]: https://github.com/johanvergeer/pelican-add-css-classes/issues
[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html

from django import template
from markdown import markdown as md
from nh3 import clean

register = template.Library()


@register.filter
def sanitized_markdown(text):
    return md(clean(text), extensions=[
        "markdown.extensions.fenced_code",
        "markdown.extensions.tables"
    ])

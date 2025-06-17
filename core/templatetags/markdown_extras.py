from django import template
from markdown import markdown as md
from nh3 import clean
from pymdownx.emoji import EmojiExtension, gemoji

register = template.Library()


@register.filter
def sanitized_markdown(text):
    return md(clean(text), extensions=[
        'markdown.extensions.fenced_code',
        'markdown.extensions.tables',
        'pymdownx.highlight',
        'pymdownx.magiclink',
        'pymdownx.betterem',
        'pymdownx.tilde',
        'pymdownx.tasklist',
        'pymdownx.superfences',
        'pymdownx.saneheaders',
        'pymdownx.magiclink',
        EmojiExtension(emoji_index=gemoji),
    ])

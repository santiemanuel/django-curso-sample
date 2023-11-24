from django import template
import markdown as md
from .note_extension import NoteExtension
from markdown.extensions.toc import TocExtension

register = template.Library()


@register.filter
def markdown_to_html(text, is_toc=False):
    md_extensions = [TocExtension(permalink=True), 'fenced_code', 'codehilite', 'tables', NoteExtension()]
    markdown = md.Markdown(extensions=md_extensions)
    html = markdown.convert(text)

    if is_toc:
        return markdown.toc
    return html

@register.filter(name='markdown')
def markdown_format(text):
    return markdown_to_html(text)

@register.filter(name='markdown_toc')
def markdown_toc_format(text):
    return markdown_to_html(text, is_toc=True)
from django.utils.safestring import mark_safe
import markdown
from django import template
register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
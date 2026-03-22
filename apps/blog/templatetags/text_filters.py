import re
import html
from django import template
from django.utils.html import strip_tags

register = template.Library()

@register.filter
def clean_preview(value):
    if not value:
        return ""

    # 1. Remove HTML tags
    text = strip_tags(value)

    # 2. Decode HTML entities (&oslash; → ø, &nbsp; → space)
    text = html.unescape(text)

    # 3. Replace non-breaking spaces
    text = text.replace('\xa0', ' ')

    # 4. Collapse multiple spaces/newlines into one
    text = re.sub(r'\s+', ' ', text)

    return text.strip()
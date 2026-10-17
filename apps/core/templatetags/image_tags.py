from django import template

from apps.core.images import thumb_name

register = template.Library()


@register.filter
def thumb(image):
    """URL of an ImageField's WebP thumbnail, falling back to the original."""
    if not image:
        return ""
    name = thumb_name(image.name)
    try:
        if image.storage.exists(name):
            return image.storage.url(name)
    except Exception:
        pass
    return image.url

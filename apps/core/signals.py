"""Optimize images automatically when they are uploaded."""
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.blog.models import Blog, BlogImage
from apps.core.images import make_thumbnail, optimize_image
from apps.core.models import Player, Sponsor

logger = logging.getLogger(__name__)


def _optimize_field(field, thumbnail=False):
    if not field:
        return
    try:
        path = field.path
        optimize_image(path)
        if thumbnail:
            make_thumbnail(path)
    except Exception:
        # Never let image processing break a save
        logger.exception("Could not optimize %s", field.name)


@receiver(post_save, sender=Blog)
@receiver(post_save, sender=BlogImage)
def optimize_blog_image(sender, instance, **kwargs):
    _optimize_field(instance.image, thumbnail=True)


@receiver(post_save, sender=Player)
def optimize_player_image(sender, instance, **kwargs):
    _optimize_field(instance.image)


@receiver(post_save, sender=Sponsor)
def optimize_sponsor_logo(sender, instance, **kwargs):
    _optimize_field(instance.logo)

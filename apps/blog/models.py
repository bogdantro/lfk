from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class BlogQuerySet(models.QuerySet):
    def public(self):
        """Only what visitors may see on the website (not in the trash)."""
        return self.filter(deleted_at__isnull=True)

    def trashed(self):
        """Posts moved to the trash in the dashboard – can still be restored."""
        return self.filter(deleted_at__isnull=False)

    def newest_first(self):
        """Posts written on this site (newest first), then the imported WordPress posts in import order."""
        return (list(self.filter(wordpress_id__isnull=True).order_by('-created_at', '-id'))
                + list(self.filter(wordpress_id__isnull=False).order_by('id')))


class Blog(models.Model):
    wordpress_id = models.BigIntegerField(unique=True, null=True, blank=True)
    title = models.CharField('Tittel', max_length=300)
    text = models.TextField('Tekst')
    slug = models.SlugField(max_length=350)
    created_at = models.DateTimeField(auto_now_add=True)
    # Editable so the dashboard can back-date a post or fix a wrong date.
    published_at = models.DateTimeField('Publisert', default=timezone.now, null=True, blank=True)
    image = models.ImageField('Hovedbilde', upload_to="static/images/blog/", blank=True)
    author = models.CharField('Forfatter', max_length=70)
    deleted_at = models.DateTimeField('Flyttet til papirkurven', null=True, blank=True)

    objects = BlogQuerySet.as_manager()

    class Meta:
        verbose_name = 'Nyhet'
        verbose_name_plural = 'Nyheter'
        ordering = ['-created_at', '-id']

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('blog_post', kwargs={
            'slug': self.slug,
            'id': self.id,
        })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField('Bilde', upload_to="static/images/blog/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Ekstra bilde'
        verbose_name_plural = 'Ekstra bilder'
        ordering = ["order"]

    def __str__(self):
        return f"{self.blog.title} image"

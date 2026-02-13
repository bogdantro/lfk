from django.db import models
from datetime import date
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class Blog(models.Model):
    wordpress_id = models.BigIntegerField(unique=True, null=True, blank=True)
    title = models.CharField(max_length=300)
    text = models.TextField()
    slug = models.SlugField(max_length=350)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    image = models.ImageField(upload_to="static/images/blog/", blank=True)
    author = models.CharField(max_length=70)

    def __str__(self):
        return self.slug
    
    def get_absolute_url(self):
        # Assuming you have a 'blog_post' URL pattern in your urls.py
        return reverse('blog_post', args=[self.slug, str(self.id)])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

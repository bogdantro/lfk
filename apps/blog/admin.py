from django.contrib import admin
from django.db import models  # Add this import line
from .models import Blog

from ckeditor.widgets import CKEditorWidget

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'created_at']
    list_editable = ['text']

    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget()},
    }

admin.site.register(Blog, BlogAdmin)

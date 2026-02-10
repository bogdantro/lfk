from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Blog

class BlogForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Blog
        fields = ['title', 'text', 'image']

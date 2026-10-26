from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Blog

MAX_EXTRA_IMAGES = 30
MAX_IMAGE_SIZE = 15 * 1024 * 1024  # 15MB – a phone photo is 3–8MB, and every upload is shrunk on save


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    """Several images in one input. Each one is checked with Pillow, so a renamed
    non-image file is rejected instead of breaking the slideshow."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput(attrs={'accept': 'image/*', 'id': 'extraImagesInput'}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        files = data if isinstance(data, (list, tuple)) else [data]
        files = [f for f in files if f]
        if len(files) > MAX_EXTRA_IMAGES:
            raise forms.ValidationError(f'Du kan laste opp maks {MAX_EXTRA_IMAGES} bilder om gangen.')
        single = forms.ImageField(error_messages={'invalid_image': 'Filen er ikke et bilde.'})
        for f in files:
            if f.size > MAX_IMAGE_SIZE:
                raise forms.ValidationError(f'«{f.name}» er større enn {MAX_IMAGE_SIZE // (1024 * 1024)} MB.')
            try:
                single.clean(f)
            except forms.ValidationError:
                raise forms.ValidationError(f'«{f.name}» er ikke et bilde vi kan lese. Prøv JPG, PNG eller WebP.')
        return files


class BlogForm(forms.ModelForm):
    text = forms.CharField(label='Tekst', widget=CKEditorWidget())
    extra_images = MultipleImageField(label='Ekstra bilder', required=False)

    class Meta:
        model = Blog
        fields = ['title', 'text', 'image', 'author', 'published_at']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'F.eks. Seier i seriestarten'}),
            'author': forms.TextInput(attrs={'placeholder': 'F.eks. Ola Nordmann', 'autocomplete': 'name'}),
            # The input is hidden in the template and replaced by the drag-and-drop uploader.
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
            'published_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        error_messages = {
            'title': {'required': 'Skriv en tittel.'},
            'author': {'required': 'Skriv hvem som har skrevet nyheten.'},
            'image': {'invalid_image': 'Hovedbildet er ikke et bilde vi kan lese. Prøv JPG, PNG eller WebP.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].error_messages['required'] = 'Skriv litt tekst i nyheten.'
        self.fields['published_at'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['published_at'].error_messages['invalid'] = 'Velg en gyldig dato og tid.'

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and getattr(image, 'size', 0) > MAX_IMAGE_SIZE:
            raise forms.ValidationError(f'Hovedbildet er større enn {MAX_IMAGE_SIZE // (1024 * 1024)} MB.')
        return image

import logging
import os
from html import unescape

from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static
from django.utils import timezone
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST

from apps.core.images import thumb_name
from apps.userprofile.decorators import staff_required

from .forms import BlogForm
from .models import Blog, BlogImage

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------
# Public pages
# ------------------------------------------------------------------

def blog(request):
    return render(request, 'core/blog.html', {'post': Blog.objects.public().newest_first()})


def blog_post(request, id, slug):
    post_info = get_object_or_404(Blog.objects.public(), id=id, slug=slug)
    post_text = strip_tags(unescape(post_info.text))

    images = []

    # always include main image first if it exists
    if post_info.image:
        images.append({"image": post_info.image})

    # then include extra images
    for img in post_info.images.all():
        images.append({"image": img.image})

    # The dashboard lets staff remove the main image, so share previews and the
    # slideshow fall back to the first extra image, then the club logo.
    share_image = images[0]["image"].url if images else static('images/logo/logo-8.png')

    return render(
        request,
        "core/blog-post.html",
        {
            "post_info": post_info,
            "post_text": post_text,
            "images": images,
            "share_image": share_image,
        },
    )


# ------------------------------------------------------------------
# Dashboard – write, edit and trash posts
# ------------------------------------------------------------------

def delete_image_file(field):
    """Remove an uploaded image and its blog-card thumbnail from disk, unless
    another post still uses the same file (imported posts can share one)."""
    if not field:
        return
    name = field.name
    if Blog.objects.filter(image=name).exists() or BlogImage.objects.filter(image=name).exists():
        return
    try:
        path = field.path
    except (ValueError, NotImplementedError):
        return
    for file_path in (path, thumb_name(path)):
        try:
            os.remove(file_path)
        except FileNotFoundError:
            pass
        except OSError:
            logger.warning('Could not delete image file %s', file_path, exc_info=True)


def save_extra_images(post, files):
    """New extra images go after the ones the post already has."""
    last = post.images.order_by('-order').values_list('order', flat=True).first()
    start = 0 if last is None else last + 1
    for i, image in enumerate(files):
        BlogImage.objects.create(blog=post, image=image, order=start + i)


@staff_required
def dashboard_blog_list(request):
    q = request.GET.get('q', '').strip()
    posts = Blog.objects.public()
    if q:
        posts = posts.filter(Q(title__icontains=q) | Q(author__icontains=q))

    return render(request, 'core/dashboard_blog_list.html', {
        'posts': posts.annotate(extra_count=Count('images')).order_by('-published_at', '-id'),
        'q': q,
        'trash_count': Blog.objects.trashed().count(),
        'is_trash': False,
    })


@staff_required
def dashboard_blog_trash(request):
    return render(request, 'core/dashboard_blog_list.html', {
        'posts': Blog.objects.trashed().order_by('-deleted_at'),
        'q': '',
        'trash_count': Blog.objects.trashed().count(),
        'is_trash': True,
    })


@staff_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save()
            save_extra_images(post, form.cleaned_data['extra_images'])
            messages.success(request, 'Nyheten ble publisert.')
            return redirect(post.get_absolute_url())
        messages.error(request, 'Noe må rettes før nyheten kan publiseres. Se feltene markert under. '
                                'Bilder du hadde valgt må velges på nytt.')
    else:
        form = BlogForm(initial={
            'author': request.user.get_full_name() or request.user.username,
            'published_at': timezone.localtime().replace(second=0, microsecond=0),
        })

    return render(request, 'core/blog_form.html', {'form': form})


@staff_required
def blog_edit(request, pk):
    post = get_object_or_404(Blog.objects.public(), pk=pk)
    # Keep the current file object: binding the form swaps post.image for the new upload.
    old_image = post.image

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            # Hidden checkbox ticked by "Fjern hovedbilde" – only counts when no new image was picked.
            if request.POST.get('remove_image') and 'image' not in request.FILES:
                post.image = ''
            post.save()

            if old_image and post.image.name != old_image.name:
                delete_image_file(old_image)

            remove_ids = request.POST.getlist('remove_images')
            for extra in post.images.filter(pk__in=[i for i in remove_ids if i.isdigit()]):
                extra.delete()
                delete_image_file(extra.image)

            save_extra_images(post, form.cleaned_data['extra_images'])

            messages.success(request, 'Endringene ble lagret.')
            return redirect('blog_edit', pk=post.pk)
        messages.error(request, 'Noe må rettes før nyheten kan lagres. Se feltene markert under. '
                                'Bilder du hadde valgt må velges på nytt.')
    else:
        form = BlogForm(instance=post)

    return render(request, 'core/blog_form.html', {'form': form, 'post': post})


@staff_required
@require_POST
def blog_trash(request, pk):
    post = get_object_or_404(Blog.objects.public(), pk=pk)
    post.deleted_at = timezone.now()
    post.save(update_fields=['deleted_at'])
    messages.success(request, f'«{post.title}» ble flyttet til papirkurven. Du kan gjenopprette den derfra.')
    return redirect('dashboard_blog_list')


@staff_required
@require_POST
def blog_restore(request, pk):
    post = get_object_or_404(Blog.objects.trashed(), pk=pk)
    post.deleted_at = None
    post.save(update_fields=['deleted_at'])
    messages.success(request, f'«{post.title}» ble gjenopprettet og er synlig på nettsiden igjen.')
    return redirect('dashboard_blog_trash')


@staff_required
@require_POST
def blog_delete_permanent(request, pk):
    post = get_object_or_404(Blog.objects.trashed(), pk=pk)
    title = post.title
    files = [post.image] + [extra.image for extra in post.images.all()]
    post.delete()
    for field in files:
        delete_image_file(field)
    messages.success(request, f'«{title}» ble slettet for godt.')
    return redirect('dashboard_blog_trash')

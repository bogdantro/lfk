from django.shortcuts import render, get_object_or_404
from .models import Blog
from django.utils.html import strip_tags
from html import unescape

def blog(request):
    site_posts = Blog.objects.filter(wordpress_id__isnull=True).order_by('-created_at', '-id')
    wp_posts   = Blog.objects.filter(wordpress_id__isnull=False).order_by('id')  # newest-imported first

    posts = list(site_posts) + list(wp_posts)

    return render(request, 'core/blog.html', {'post': posts})

def blog_post(request, id, slug):
    post_info = get_object_or_404(Blog, id=id, slug=slug) 

    post_text = strip_tags(unescape(post_info.text))

    return render(request, 'core/blog-post.html', {'post_info':post_info, 'post_text':post_text,})



from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required

from .models import Blog
from .forms import BlogForm



@staff_member_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)

        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user.get_full_name() or request.user.username
            blog.save()

            return redirect(blog.get_absolute_url())
    else:
        form = BlogForm()

    return render(request, 'core/blog_form.html', {'form': form})

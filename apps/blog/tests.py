import io
import os
import shutil
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import Blog, BlogImage

MEDIA_ROOT = tempfile.mkdtemp()


def image_file(name='bilde.jpg', size=(40, 30)):
    buf = io.BytesIO()
    Image.new('RGB', size, (200, 30, 30)).save(buf, 'JPEG')
    return SimpleUploadedFile(name, buf.getvalue(), content_type='image/jpeg')


def make_post(**kwargs):
    defaults = {'title': 'Seier i seriestarten', 'text': '<p>Kampreferat</p>', 'author': 'Ola Nordmann'}
    defaults.update(kwargs)
    return Blog.objects.create(**defaults)


def edit_data(post, **overrides):
    data = {
        'title': post.title,
        'text': post.text,
        'author': post.author,
        'published_at': '2026-05-17T12:00',
    }
    data.update(overrides)
    return data


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class DashboardBlogTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.staff = User.objects.create_user('redaktor', password='x' * 12, is_staff=True)
        self.client.force_login(self.staff)

    def test_visitor_is_sent_to_site_login_not_django_admin(self):
        self.client.logout()
        post = make_post()
        response = self.client.get(reverse('blog_edit', args=[post.pk]))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('blog_edit', args=[post.pk]),
                             fetch_redirect_response=False)

    def test_non_staff_user_cannot_edit(self):
        self.client.force_login(User.objects.create_user('vanlig', password='x' * 12))
        post = make_post()
        response = self.client.post(reverse('blog_edit', args=[post.pk]), edit_data(post, title='Hacket'))
        self.assertEqual(response.status_code, 302)
        post.refresh_from_db()
        self.assertEqual(post.title, 'Seier i seriestarten')

    def test_list_shows_posts_and_search_filters(self):
        make_post(title='Seier borte')
        make_post(title='Ny trener')
        response = self.client.get(reverse('dashboard_blog_list'), {'q': 'trener'})
        self.assertContains(response, 'Ny trener')
        self.assertNotContains(response, 'Seier borte')

    def test_edit_changes_text_fields_and_keeps_slug(self):
        post = make_post()
        response = self.client.post(reverse('blog_edit', args=[post.pk]),
                                    edit_data(post, title='Ny tittel', author='Kari', text='<p>Ny tekst</p>'))
        self.assertRedirects(response, reverse('blog_edit', args=[post.pk]))
        post.refresh_from_db()
        self.assertEqual((post.title, post.author, post.text), ('Ny tittel', 'Kari', '<p>Ny tekst</p>'))
        self.assertEqual(post.published_at.strftime('%Y-%m-%d'), '2026-05-17')
        # Links already shared on Facebook etc. keep working.
        self.assertEqual(post.slug, 'seier-i-seriestarten')

    def test_edit_adds_extra_images_after_existing_ones(self):
        post = make_post()
        BlogImage.objects.create(blog=post, image=image_file('gammel.jpg'), order=0)
        data = edit_data(post)
        data['extra_images'] = [image_file('ny1.jpg'), image_file('ny2.jpg')]
        self.client.post(reverse('blog_edit', args=[post.pk]), data)
        self.assertEqual(list(post.images.values_list('order', flat=True)), [0, 1, 2])

    def test_edit_removes_ticked_extra_images_and_their_files(self):
        post = make_post()
        keep = BlogImage.objects.create(blog=post, image=image_file('behold.jpg'))
        remove = BlogImage.objects.create(blog=post, image=image_file('fjern.jpg'), order=1)
        removed_path = remove.image.path
        data = edit_data(post)
        data['remove_images'] = [str(remove.pk)]
        self.client.post(reverse('blog_edit', args=[post.pk]), data)
        self.assertEqual(list(post.images.all()), [keep])
        self.assertFalse(os.path.exists(removed_path))

    def test_edit_replaces_main_image_and_deletes_old_file(self):
        post = make_post(image=image_file('gammel.jpg'))
        old_path = post.image.path
        data = edit_data(post)
        data['image'] = image_file('ny.jpg')
        self.client.post(reverse('blog_edit', args=[post.pk]), data)
        post.refresh_from_db()
        self.assertIn('ny', post.image.name)
        self.assertFalse(os.path.exists(old_path))

    def test_remove_main_image_checkbox_clears_it(self):
        post = make_post(image=image_file())
        self.client.post(reverse('blog_edit', args=[post.pk]), edit_data(post, remove_image='1'))
        post.refresh_from_db()
        self.assertFalse(post.image)

    def test_post_page_works_after_main_image_is_removed(self):
        post = make_post(image=image_file())
        self.client.post(reverse('blog_edit', args=[post.pk]), edit_data(post, remove_image='1'))
        response = self.client.get(post.get_absolute_url())
        self.assertContains(response, 'images/logo/logo-8.png')

    def test_saving_without_new_image_keeps_the_current_one(self):
        post = make_post(image=image_file())
        name = post.image.name
        self.client.post(reverse('blog_edit', args=[post.pk]), edit_data(post, title='Bare ny tittel'))
        post.refresh_from_db()
        self.assertEqual(post.image.name, name)

    def test_fake_image_is_rejected_with_norwegian_message(self):
        post = make_post()
        data = edit_data(post)
        data['extra_images'] = [SimpleUploadedFile('virus.jpg', b'not an image', content_type='image/jpeg')]
        response = self.client.post(reverse('blog_edit', args=[post.pk]), data)
        self.assertContains(response, '«virus.jpg» er ikke et bilde')
        self.assertEqual(post.images.count(), 0)

    def test_missing_title_shows_error_and_saves_nothing(self):
        post = make_post()
        response = self.client.post(reverse('blog_edit', args=[post.pk]), edit_data(post, title=''))
        self.assertContains(response, 'Skriv en tittel.')
        post.refresh_from_db()
        self.assertEqual(post.title, 'Seier i seriestarten')

    def test_create_uses_editable_author_and_saves_extra_images(self):
        data = {'title': 'Ny nyhet', 'text': '<p>Tekst</p>', 'author': 'Styret', 'published_at': '2026-10-01T09:30',
                'extra_images': [image_file()]}
        response = self.client.post(reverse('blog_create'), data)
        post = Blog.objects.get(title='Ny nyhet')
        self.assertRedirects(response, post.get_absolute_url(), fetch_redirect_response=False)
        self.assertEqual(post.author, 'Styret')
        self.assertEqual(post.images.count(), 1)


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class BlogTrashTests(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.create_user('redaktor', password='x' * 12, is_staff=True))

    def test_trash_hides_post_from_website_but_keeps_it(self):
        post = make_post()
        self.client.post(reverse('blog_trash', args=[post.pk]))
        self.client.logout()
        self.assertEqual(self.client.get(post.get_absolute_url()).status_code, 404)
        self.assertNotContains(self.client.get(reverse('blog')), 'Seier i seriestarten')
        self.assertNotContains(self.client.get('/sitemap.xml'), post.get_absolute_url())
        self.assertTrue(Blog.objects.filter(pk=post.pk).exists())

    def test_trash_cannot_be_done_with_get(self):
        post = make_post()
        self.assertEqual(self.client.get(reverse('blog_trash', args=[post.pk])).status_code, 405)
        post.refresh_from_db()
        self.assertIsNone(post.deleted_at)

    def test_restore_puts_post_back_on_website(self):
        post = make_post()
        self.client.post(reverse('blog_trash', args=[post.pk]))
        self.client.post(reverse('blog_restore', args=[post.pk]))
        self.assertEqual(self.client.get(post.get_absolute_url()).status_code, 200)

    def test_permanent_delete_only_works_from_trash_and_removes_files(self):
        post = make_post(image=image_file())
        path = post.image.path
        self.client.post(reverse('blog_delete_permanent', args=[post.pk]))
        self.assertTrue(Blog.objects.filter(pk=post.pk).exists())

        self.client.post(reverse('blog_trash', args=[post.pk]))
        self.client.post(reverse('blog_delete_permanent', args=[post.pk]))
        self.assertFalse(Blog.objects.filter(pk=post.pk).exists())
        self.assertFalse(os.path.exists(path))

    def test_trashed_post_cannot_be_edited(self):
        post = make_post()
        self.client.post(reverse('blog_trash', args=[post.pk]))
        self.assertEqual(self.client.get(reverse('blog_edit', args=[post.pk])).status_code, 404)

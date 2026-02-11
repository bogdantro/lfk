import os
from urllib.parse import urlparse

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime

from apps.blog.models import Blog


class Command(BaseCommand):
    help = "Import ALL WordPress posts via REST API pagination"

    def add_arguments(self, parser):
        parser.add_argument(
            "--base-url",
            default="https://lillehammerfk.no",
            help="Base site URL, e.g. https://example.com",
        )
        parser.add_argument("--per-page", type=int, default=100)
        parser.add_argument("--download-images", action="store_true")

    def handle(self, *args, **options):
        base_url = options["base_url"].rstrip("/")
        per_page = min(options["per_page"], 100)  # WP usually caps at 100
        download_images = options["download_images"]

        session = requests.Session()
        page = 1
        imported = 0

        while True:
            url = f"{base_url}/wp-json/wp/v2/posts"
            resp = session.get(
                url,
                params={
                    "per_page": per_page,
                    "page": page,
                    "status": "publish",
                    "_fields": "id,date,slug,title,content,author,jetpack_featured_media_url",
                },
                timeout=30,
            )

            # If we go past last page, WP often returns 400 with "rest_post_invalid_page_number"
            if resp.status_code == 400:
                break

            resp.raise_for_status()
            posts = resp.json()

            if not posts:
                break

            for item in posts:
                wp_id = item["id"]
                title = item["title"]["rendered"]
                slug = item.get("slug") or ""
                content_html = item["content"]["rendered"]
                author_id_or_name = "Jostein Wahl"
                wp_published_at = parse_datetime(item.get("date"))

                featured_url = item.get("jetpack_featured_media_url", "")

                obj, created = Blog.objects.update_or_create(
                    wordpress_id=wp_id,
                    defaults={
                        "title": title,
                        "text": content_html,
                        "slug": slug,
                        "author": author_id_or_name,
                        "published_at": wp_published_at,
                    },
                )

                if download_images and featured_url:
                    try:
                        img = session.get(featured_url, timeout=30)
                        img.raise_for_status()
                        filename = os.path.basename(urlparse(featured_url).path) or f"wp_{wp_id}.img"
                        obj.image.save(filename, ContentFile(img.content), save=True)
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(
                            f"Image download failed for {wp_id}: {e}"
                        ))

                imported += 1

            self.stdout.write(self.style.SUCCESS(f"Fetched page {page} ({len(posts)} posts)"))
            page += 1

        self.stdout.write(self.style.SUCCESS(f"Done. Imported/updated {imported} posts."))

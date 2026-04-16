from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.blog.models import Blog


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            "home",

            # Pages
            "xtravgs",
            "fotballextra",

            # Sport
            "senior",
            "senior_herrer",
            "senior_kvinner",
            "wednesday_united",
            "ungdom",
            "barn",
            "uefa_playmakers",
            "landslagsskolen",
            "fair_play",

            # Marked
            "vare_samarbeidspartnere",
            "baerekraft",
            "medlemsfordeler",
            "grasrotandelen",
            "la_stampa_magasin",
            "stampapodden",

            # Arrangement
            "tine_fotballskole",
            "thallaug_cup",
            "kiwi_cup",

            # Om klubben
            "historie",
            "klubbhandbok",
            "klubbkolleksjon",
            "medlemskap",
            "styret",
            "kontakt",
            "varsling",
            "forsikring",
            "dommere",
            "politiattest",
            "minibuss",
            "fotballfondet",
            "frivillighetsbanken",

            # Blog overview
            "blog",
        ]

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return Blog.objects.all().order_by("-published_at", "-created_at")

    def lastmod(self, obj):
        return obj.published_at or obj.created_at

    def location(self, obj):
        return obj.get_absolute_url()
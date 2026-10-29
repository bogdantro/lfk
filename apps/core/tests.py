from pathlib import Path
from unittest import mock

from django.conf import settings
from django.test import TestCase

from .views import PROMOTION_PHOTOS


class PromotionHeroTests(TestCase):
    def test_switching_back_shows_the_old_hero(self):
        with mock.patch('apps.core.views.HOMEPAGE_HERO', 'default'):
            response = self.client.get('/')
        self.assertContains(response, 'id="coverMainDes"')
        self.assertContains(response, 'images/covers/cover.mov')
        self.assertNotContains(response, 'id="promoHero"')
        self.assertNotContains(response, 'opprykk-herrer-1.webp')

    def test_home_shows_the_promotion_hero(self):
        response = self.client.get('/')
        self.assertContains(response, 'id="promoHero"')
        self.assertContains(response, 'js/promotion-hero.js')

    def test_hero_shows_every_photo_with_both_promoted_teams(self):
        response = self.client.get('/')
        for photo in PROMOTION_PHOTOS:
            self.assertContains(response, f"images/covers/{photo['file']}.webp")
            self.assertContains(response, f"images/covers/{photo['file']}.jpg")
        self.assertContains(response, 'Herrer&nbsp;·&nbsp;2.&nbsp;divisjon')
        self.assertContains(response, 'Kvinner&nbsp;·&nbsp;3.&nbsp;divisjon')

    def test_every_photo_file_exists(self):
        covers = Path(settings.BASE_DIR) / 'static' / 'images' / 'covers'
        for photo in PROMOTION_PHOTOS:
            for ext in ('webp', 'jpg'):
                self.assertTrue((covers / f"{photo['file']}.{ext}").exists(), f"{photo['file']}.{ext}")

    def test_only_the_first_mens_photo_shows_without_the_script(self):
        response = self.client.get('/')
        self.assertContains(response, 'class="promo-photo is-active"', count=1)
        self.assertContains(response, 'class="promo-photo is-active" data-team="herrer"')
        self.assertContains(response, 'class="division-line is-active" data-team="herrer"')
        self.assertContains(response, 'data-team="kvinner" aria-hidden="true">Kvinner')

    def test_photographer_is_credited(self):
        response = self.client.get('/')
        self.assertContains(response, 'Foto: Niklas Lyngfoss')

    def test_congratulate_button_opens_the_thank_you_popup(self):
        response = self.client.get('/')
        self.assertContains(response, 'id="promoCheerOpen"')
        self.assertContains(response, 'Send dine gratulasjoner')
        self.assertContains(response, 'role="dialog"')
        self.assertContains(response, 'Takk for at du heier!')

    def test_congratulate_button_is_visible_without_the_script(self):
        # Hidden-until-JS left it invisible for visitors with an old cached script
        response = self.client.get('/')
        self.assertNotContains(response, 'aria-controls="promoCheer" hidden')

    def test_ticker_band_and_season_link_are_gone(self):
        response = self.client.get('/')
        self.assertNotContains(response, 'class="ticker"')
        self.assertNotContains(response, 'Les om sesongen')

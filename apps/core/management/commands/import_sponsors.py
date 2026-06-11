import os
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.core.models import Sponsor


class Command(BaseCommand):
    help = "Import sponsors from image folder"

    def handle(self, *args, **kwargs):
        folder_path = os.path.join(settings.BASE_DIR, "static/images/partners")

        if not os.path.exists(folder_path):
            self.stdout.write(self.style.ERROR("Folder not found"))
            return

        for filename in os.listdir(folder_path):
            if filename.endswith(".png"):
                name = filename.replace("_white.png", "").replace("_", " ").title()

                file_path = os.path.join("static/images/partners", filename)

                sponsor, created = Sponsor.objects.get_or_create(
                    name=name,
                    defaults={"logo": file_path}
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Added: {name}"))
                else:
                    self.stdout.write(f"Already exists: {name}")
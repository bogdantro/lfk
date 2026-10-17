import sys
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.core.images import EXTENSIONS, THUMB_DIR, make_thumbnail, optimize_image

DEFAULT_PATHS = ["static/images", "players"]
THUMB_PATHS = ["static/images/blog"]


def _safe(text):
    # Windows consoles can't print every character in file names (e.g. "å")
    enc = sys.stdout.encoding or "utf-8"
    return text.encode(enc, "replace").decode(enc)


class Command(BaseCommand):
    help = (
        "Resize and recompress images in place (same names and formats) and "
        "create WebP thumbnails for blog images. Safe to run repeatedly."
    )

    def add_arguments(self, parser):
        parser.add_argument("paths", nargs="*", help=f"Folders to scan (default: {', '.join(DEFAULT_PATHS)})")
        parser.add_argument("--dry-run", action="store_true", help="Report savings without changing files")
        parser.add_argument("--max-side", type=int, default=1920, help="Longest side in pixels (default 1920)")

    def handle(self, *args, **opts):
        base = Path(settings.BASE_DIR)
        roots = [base / p for p in (opts["paths"] or DEFAULT_PATHS)]
        dry = opts["dry_run"]

        before = after = changed = failed = 0
        for root in roots:
            if not root.exists():
                continue
            for path in sorted(root.rglob("*")):
                if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
                    continue
                if THUMB_DIR in path.parts:
                    continue
                try:
                    old, new = optimize_image(path, max_side=opts["max_side"], dry_run=dry)
                except Exception as e:
                    failed += 1
                    self.stderr.write(_safe(f"  skipped {path.relative_to(base)}: {e}"))
                    continue
                before += old
                after += new
                if new < old:
                    changed += 1
                    self.stdout.write(_safe(f"  {path.relative_to(base)}: {old/1e6:.1f} MB -> {new/1e6:.2f} MB"))

        thumbs = 0
        if not dry:
            for rel in THUMB_PATHS:
                root = base / rel
                if not root.exists():
                    continue
                for path in sorted(root.iterdir()):
                    if path.is_file() and path.suffix.lower() in EXTENSIONS:
                        try:
                            make_thumbnail(path)
                            thumbs += 1
                        except Exception as e:
                            self.stderr.write(_safe(f"  no thumbnail for {path.relative_to(base)}: {e}"))

        verb = "Would save" if dry else "Saved"
        self.stdout.write(self.style.SUCCESS(
            f"{verb} {(before - after)/1e6:.0f} MB ({before/1e6:.0f} MB -> {after/1e6:.0f} MB) "
            f"across {changed} files; {thumbs} thumbnails ready; {failed} skipped."
        ))

"""Image optimization helpers.

Files are always rewritten in place with the same name and format, so paths
stored in the database and used in templates keep working.
"""
import io
import os
from pathlib import Path

from PIL import Image, ImageOps

MAX_SIDE = 1920        # longest side for full-size images
THUMB_WIDTH = 1200     # width of blog card thumbnails
JPEG_QUALITY = 82
WEBP_QUALITY = 80
MIN_SAVING = 0.10      # only replace a file when it gets at least 10% smaller
SKIP_BELOW = 300 * 1024  # files this small and within MAX_SIDE are left alone

EXTENSIONS = {".jpg", ".jpeg", ".jfif", ".png", ".webp", ".avif"}
THUMB_DIR = "thumbs"


def _encode(img, ext, icc=None):
    buf = io.BytesIO()
    extra = {"icc_profile": icc} if icc else {}
    if ext in (".jpg", ".jpeg", ".jfif"):
        img.save(buf, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True, **extra)
    elif ext == ".png":
        img.save(buf, "PNG", optimize=True, **extra)
    elif ext == ".webp":
        img.save(buf, "WEBP", quality=WEBP_QUALITY, method=6, **extra)
    elif ext == ".avif":
        img.save(buf, "AVIF", quality=60, **extra)
    return buf.getvalue()


def optimize_image(path, max_side=MAX_SIDE, dry_run=False):
    """Shrink and recompress one image in place.

    Returns (old_size, new_size); new_size equals old_size when the file
    was left untouched.
    """
    path = Path(path)
    ext = path.suffix.lower()
    old_size = path.stat().st_size
    if ext not in EXTENSIONS:
        return old_size, old_size

    with Image.open(path) as img:
        # Don't flatten animations (camera MPO files are just photos with extra frames)
        if getattr(img, "is_animated", False) and img.format != "MPO":
            return old_size, old_size
        if max(img.size) <= max_side and old_size <= SKIP_BELOW:
            return old_size, old_size

        img.load()
        icc = img.info.get("icc_profile")
        # Bake EXIF rotation into the pixels, since the metadata is dropped
        img = ImageOps.exif_transpose(img)
        if max(img.size) > max_side:
            img.thumbnail((max_side, max_side), Image.LANCZOS)
        if ext in (".jpg", ".jpeg", ".jfif") and img.mode not in ("RGB", "L"):
            # e.g. CMYK: its colour profile no longer matches after conversion
            if img.mode == "CMYK":
                icc = None
            img = img.convert("RGB")
        data = _encode(img, ext, icc)

    if len(data) > old_size * (1 - MIN_SAVING):
        return old_size, old_size
    if not dry_run:
        tmp = path.with_name(path.name + ".tmp")
        tmp.write_bytes(data)
        os.replace(tmp, path)
    return old_size, len(data)


def thumb_name(name):
    """'static/images/blog/x.jpg' -> 'static/images/blog/thumbs/x.webp'"""
    p = Path(name)
    return (p.parent / THUMB_DIR / (p.stem + ".webp")).as_posix()


def make_thumbnail(path, width=THUMB_WIDTH, force=False):
    """Write a WebP thumbnail next to the image; returns its path."""
    path = Path(path)
    out = Path(thumb_name(path))
    if out.exists() and not force and out.stat().st_mtime >= path.stat().st_mtime:
        return out
    out.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(path) as img:
        img = ImageOps.exif_transpose(img)
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA" if "transparency" in img.info else "RGB")
        if img.width > width:
            img.thumbnail((width, width * 10), Image.LANCZOS)
        tmp = out.with_name(out.name + ".tmp")
        img.save(tmp, "WEBP", quality=WEBP_QUALITY, method=6)
    os.replace(tmp, out)
    return out

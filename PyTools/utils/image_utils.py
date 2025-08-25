import os
import re
import posixpath  # Ensures forward slashes for HTML paths
from config import TOP_LEVEL_DIR  # <-- single variable from main.py

THUMBNAIL_DIR = os.path.join(TOP_LEVEL_DIR, "thumbnails")

def _web_rel(path_under_base: str) -> str:
    """Convert OS paths to forward-slash web paths."""
    return posixpath.join(*path_under_base.split(os.sep))

def sanitize_title(title: str) -> str:
    # Remove Windows-invalid filename chars + quotes, collapse spaces to underscores
    clean = re.sub(r'[<>:"/\\|?*\']', "", title)
    clean = clean.strip().lower().replace(" ", "_")
    # Optional: collapse multiple underscores
    return re.sub(r"_+", "_", clean)

def find_image_path(pattern: str) -> str:
    """
    Search thumbnails folder under TOP_LEVEL_DIR for pattern + ext.
    Returns a web-relative path like 'thumbnails/thumbnail_foo.png' or '' if not found.
    """
    for ext in (".png", ".jpg", ".jpeg"):
        filename = pattern + ext
        abs_candidate = os.path.join(THUMBNAIL_DIR, filename)
        if os.path.isfile(abs_candidate):
            # Return a web-safe relative path (no backslashes, no leading ../)
            return _web_rel(os.path.join(".", "thumbnails", filename))


    print(f"[WARN] No image found for pattern '{pattern}' in {THUMBNAIL_DIR}")
    return ""  # Safe fallback so HTML still renders

def thumb_path(title: str) -> str:
    return find_image_path(f"thumbnail_{sanitize_title(title)}")

def banner_path(title: str) -> str:
    return find_image_path(f"banner_{sanitize_title(title)}")

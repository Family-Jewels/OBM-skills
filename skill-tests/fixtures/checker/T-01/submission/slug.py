import re

def slugify(text):
    """Lowercase, and turn runs of non-alphanumerics into single hyphens."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")

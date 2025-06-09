# theme.py
import qdarktheme

_current = "light"

def setup(app):
    """
    Apply the current theme (light or dark) to the QApplication.
    Uses setup_theme() which applies palette, stylesheet, and icons.
    """
    qdarktheme.setup_theme(_current)      # Applies full theme :contentReference[oaicite:0]{index=0}

def toggle(app):
    """
    Toggle between light and dark themes at runtime.
    """
    global _current
    _current = "dark" if _current == "light" else "light"
    qdarktheme.setup_theme(_current)      # Re-apply the new theme :contentReference[oaicite:1]{index=1}

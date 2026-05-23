"""Shared Rich console singleton, themed to match Singularity (slides.scss).

Import as `from tour.console import console`. Everywhere else in the package
should use this instance so styling and width settings stay consistent.
"""

from __future__ import annotations

from rich.console import Console
from rich.theme import Theme

# Mirrors the Singularity palette in singularity.scss. Keep in sync if the
# slide theme changes.
_THEME = Theme(
    {
        "title": "bold #9B5CFF",          # void-violet
        "subtitle": "#38F8F2",            # void-cyan
        "section": "bold #FF4FCB",        # void-magenta
        "body": "#D8DBF5",                # void-fg1
        "muted": "#6E74A8",               # void-fg3
        "faint": "#4A4F7A",               # void-fg4
        "hint": "#38F8F2",                # void-cyan
        "ok": "#A6FF4D",                  # void-green
        "warning": "#FFB347",             # void-amber
        "error": "bold #FF4D6D",          # void-red
        "code": "#A6FF4D on #12132A",     # void-green on void-bg1
    }
)

console = Console(theme=_THEME, highlight=False)

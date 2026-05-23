"""Full-screen prompt_toolkit TUI: the demo picker.

prompt_toolkit was chosen over Rich-only because Rich can't reliably trap Esc
inside a Live display. prompt_toolkit's Application + KeyBindings is the right
primitive for keyboard-driven full-screen UIs.

Demo modules are *lazy-imported* via `resolve_runner` so the menu opens
instantly — heavy deps (numpy, torch, matplotlib, plotly) only load when their
demo is actually picked.
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Awaitable, Callable

from prompt_toolkit import Application
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import HSplit, Layout, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.styles import Style

from tour.settings import Settings

# Singularity-aligned prompt_toolkit style. Mirrors singularity.scss.
PT_STYLE = Style.from_dict(
    {
        "title": "fg:#9B5CFF bold",         # void-violet
        "subtitle": "fg:#38F8F2",           # void-cyan
        "body": "fg:#D8DBF5",               # void-fg1
        "muted": "fg:#6E74A8",              # void-fg3
        "faint": "fg:#4A4F7A italic",       # void-fg4
        "warning": "fg:#FFB347",            # void-amber
        "error": "fg:#FF4D6D bold",         # void-red
        "selected": "fg:#08080F bg:#38F8F2 bold",  # cyan highlight, void-bg0 text
        "selected.sub": "fg:#12132A bg:#38F8F2",
        "available": "fg:#A6FF4D",          # void-green
        "unavailable": "fg:#6E74A8 italic", # void-fg3
        "hint": "fg:#38F8F2",               # void-cyan
        "border": "fg:#2C2F5E",             # void-bg3
        "accent": "fg:#FF4FCB",             # void-magenta
    }
)


@dataclass(frozen=True)
class DemoEntry:
    id: str
    title: str
    subtitle: str
    runner_path: str  # e.g. "tour.demos.placeholder:run"
    available: bool = True


# Demos are deferred for the 2026-05-23 talk. Keep one placeholder so the menu
# renders honestly to anyone who clones — they see "TBD" rather than an empty
# screen. Add real entries here as demos land; the menu loop will pick them up
# without further changes.
DEMOS: tuple[DemoEntry, ...] = (
    DemoEntry(
        id="placeholder",
        title="(TBD) Demo placeholder",
        subtitle="Demos for this talk are deferred. Watch this space.",
        runner_path="tour.demos.placeholder:run",
        available=True,
    ),
)


def resolve_runner(path: str) -> Callable[[Settings], Awaitable[None]]:
    """Resolve a 'pkg.module:attr' dotted path to its callable. Imports happen
    lazily so heavy modules stay out of the menu's startup cost."""
    module_path, _, attr = path.partition(":")
    if not module_path or not attr:
        raise ValueError(f"Bad runner path: {path!r}. Expected 'pkg.module:attr'.")
    module = importlib.import_module(module_path)
    runner = getattr(module, attr)
    if not callable(runner):
        raise TypeError(f"{path!r} is not callable")
    return runner


def _render(selected_idx: int) -> FormattedText:
    """Build the formatted-text body of the menu for a given selection."""
    lines: list[tuple[str, str]] = []
    lines.append(("class:title", "Beyond the Chatbot — Tour CLI\n"))
    lines.append(
        (
            "class:subtitle",
            "A Tour of the AI Universe · Chattanooga AI Collective × Chatt*Lab\n",
        )
    )
    lines.append(("class:muted", "─" * 64 + "\n"))
    lines.append(("class:body", "Pick a demo:\n\n"))

    for i, demo in enumerate(DEMOS):
        is_sel = i == selected_idx
        marker = "▶ " if is_sel else "  "
        avail_cls = "class:available" if demo.available else "class:unavailable"
        sel_cls = "class:selected" if is_sel else avail_cls
        sub_cls = "class:selected.sub" if is_sel else "class:muted"
        lines.append((sel_cls, f"{marker}{demo.title}\n"))
        lines.append((sub_cls, f"    {demo.subtitle}\n"))
        lines.append(("", "\n"))

    lines.append(("class:muted", "─" * 64 + "\n"))
    lines.append(
        (
            "class:hint",
            "↑/↓ select   ⏎ launch   q / Esc quit\n",
        )
    )
    return FormattedText(lines)


async def run_menu(settings: Settings) -> str:
    """Show the menu and return either the selected demo id or 'quit'."""
    state = {"idx": 0, "choice": "quit"}

    def render_callable() -> FormattedText:
        return _render(state["idx"])

    body = Window(content=FormattedTextControl(text=render_callable), always_hide_cursor=True)

    kb = KeyBindings()

    @kb.add("up")
    def _up(event):  # noqa: ANN001
        state["idx"] = (state["idx"] - 1) % len(DEMOS)

    @kb.add("down")
    def _down(event):  # noqa: ANN001
        state["idx"] = (state["idx"] + 1) % len(DEMOS)

    @kb.add("enter")
    def _enter(event):  # noqa: ANN001
        state["choice"] = DEMOS[state["idx"]].id
        event.app.exit()

    @kb.add("escape")
    @kb.add("q")
    @kb.add("c-c")
    def _quit(event):  # noqa: ANN001
        state["choice"] = "quit"
        event.app.exit()

    app: Application = Application(
        layout=Layout(HSplit([body])),
        key_bindings=kb,
        style=PT_STYLE,
        full_screen=True,
        mouse_support=False,
    )

    await app.run_async()
    return state["choice"]

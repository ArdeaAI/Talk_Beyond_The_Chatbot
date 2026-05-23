"""Placeholder demo. Renders honestly when picked from the menu so the CLI
ships truthfully alongside the 2026-05-23 talk: demos are deferred.

Replace this file (or add siblings) once real demos land. The expected shape is
a single `async def run(settings: Settings) -> None` callable; the menu loop
will await it.
"""

from __future__ import annotations

import asyncio

from tour.console import console
from tour.settings import Settings


async def run(settings: Settings) -> None:
    """Print a TBD card, wait for the user, return to the menu."""
    console.print()
    console.rule("[section]TBD demo[/section]", style="#FF4FCB")
    console.print()
    console.print(
        "[body]This is a placeholder. Real demos are deferred for the talk on "
        "2026-05-23 - the menu shipped first so the repo is honest to anyone "
        "who clones along.[/body]"
    )
    console.print()
    console.print(
        "[muted]If you came here looking for an evolutionary toy, a Hopfield "
        "recall, an MCTS visualizer, or a tiny diffusion denoiser: not yet. "
        "Open an issue or ping me.[/muted]"
    )
    console.print()
    console.print(f"[faint]settings.demo_seed = {settings.demo_seed}[/faint]")
    console.print()

    try:
        console.input("[hint]Press Enter to return to the menu...[/hint] ")
    except (KeyboardInterrupt, EOFError):
        pass

    # Yield once so the event loop gets a tick before the menu re-renders.
    await asyncio.sleep(0)

"""tour CLI entrypoint - referenced by `[project.scripts] tour` in pyproject.

Dispatches to the menu loop. Heavy demo imports are deferred via
`menu.resolve_runner` so the menu always opens fast.
"""

from __future__ import annotations

import asyncio
import sys

from tour.console import console
from tour.menu import DEMOS, resolve_runner, run_menu
from tour.settings import Settings


async def _main_loop() -> int:
    settings = Settings()

    while True:
        choice = await run_menu(settings)
        if choice == "quit":
            console.print("[muted]Catch you out there.[/muted]")
            return 0

        entry = next((d for d in DEMOS if d.id == choice), None)
        if entry is None:
            console.print(f"[error]Unknown demo: {choice!r}[/error]")
            continue

        try:
            runner = resolve_runner(entry.runner_path)
            await runner(settings)
        except KeyboardInterrupt:
            # Esc / Ctrl-C inside a demo: clean return to menu.
            pass
        except Exception:
            console.print_exception(show_locals=False)
            console.print()
            try:
                console.input("[muted]Press Enter to return to the menu...[/muted]")
            except (KeyboardInterrupt, EOFError):
                return 1


def main() -> int:
    """Entry referenced by `[project.scripts] tour = tour.main:main`."""
    try:
        return asyncio.run(_main_loop())
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())

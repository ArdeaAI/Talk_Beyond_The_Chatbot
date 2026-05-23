# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A talk repo for **"Beyond the Chatbot: A Tour of the AI Universe"** — meetup co-hosted by the Chattanooga AI Collective and Chatt\*Lab on 2026-05-23. Speaker: John Gardner (Sinjhin).

The deliverable is a Quarto + Reveal.js slide deck plus a small companion Python CLI (`tour`) the audience can clone after the talk to poke at demos.

## Current state

The repo is pre-scaffold. The tracked tree is just `README.md`, `LICENSE`, `.gitignore`, and this file. Everything else listed below is planned but not yet built.

`ai/` is **gitignored on purpose** and holds the planning artifacts that drive structure:

- `ai/plan.md` — **source of truth** for intended repo layout, tech stack, theme, slide patterns, and order of operations. Read this first for any non-trivial work.
- `ai/meetup_description.md` — public-facing copy / agenda.
- `ai/ai_paradigms.md` — research table of paradigms with the curated subset for the talk.

Treat `ai/` as authoritative for *intent*, not current state of the code.

## Planned structure (from `ai/plan.md`)

```
slides.qmd                # single source of truth for the deck
_quarto.yml               # Quarto + Reveal.js config
singularity.scss          # custom "Singularity" theme
references.bib            # citations
assets/img/, assets/audio/
tour/                     # Python CLI scaffold
  main.py                 # `uv run tour` entrypoint
  menu.py                 # prompt_toolkit full-screen TUI
  console.py              # Rich console singleton
  settings.py             # pydantic-settings
  demos/placeholder.py    # one TBD stub
pyproject.toml            # uv + hatchling; [project.scripts] exposes `tour`
package.json              # Bun script runner only (start / render / publish)
```

`AGENTS.md` is the intended canonical agent-guidance filename; `CLAUDE.md` is expected to be a symlink to it once scaffolded. Until then, edit `CLAUDE.md` directly.

## Planned commands

None of these exist yet. Implement them when scaffolding the corresponding subsystem.

| Command | Purpose |
| --- | --- |
| `bun start` | Live preview via `quarto preview` |
| `bun run render` | Build the static deck |
| `bun run publish` | `quarto publish gh-pages` |
| `uv run tour` | Open the CLI menu |

## Conventions specific to this repo

- **Slide content pattern** (`ai/plan.md` §4): every system/paradigm module follows **Hook → Mechanism → Why it matters → Further reading**. Metaphor first, mechanism second. Always name the math so curious viewers can search later; never apologize for skipping it.
- **Theme — "Singularity"** (`ai/plan.md` §3): deep-space / hacker-terminal palette with concrete hex values, usage rules, and typography. Don't introduce new colors or fonts without updating that section first.
- **CLI lazy-import discipline**: heavy deps (numpy, torch, matplotlib, plotly) are never imported at module top-level. They load only inside the demo function the user selects, so the menu opens instantly. The voice-talk repo's `tour/` skeleton is the reference for this pattern.
- **Bun is the script runner, not the bundler.** It only orchestrates `quarto preview / render / publish`. There is no JS source to build.
- **Demos are deferred.** For 2026-05-23 the CLI ships a single `(TBD)` placeholder so the menu renders honestly to anyone who clones.

## Slide-flow anchor

High-level flow lives in `ai/plan.md` §5 (sponsor → Discord → cold open → agenda → round table → game-changers → intermission → paradigms → deep dive → Q&A). When adding a new slide, place it inside the matching numbered section there rather than inventing a new top-level arc.

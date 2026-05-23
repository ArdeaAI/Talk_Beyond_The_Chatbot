"""Runtime settings for the tour CLI.

Reads from environment variables (and `.env` if present). Add new knobs here as
the CLI grows — keep this module dependency-light so the menu can construct a
Settings instance instantly.
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Top-level runtime configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Demo behavior knobs (mostly unused while everything is TBD, but worth
    # keeping wired so adding a demo later doesn't require re-plumbing).
    demo_seed: int = Field(default=42, description="Default RNG seed for demos.")
    cache_dir: str = Field(
        default="~/.cache/beyond-the-chatbot",
        description="Where demos cache models, datasets, or intermediate artifacts.",
    )

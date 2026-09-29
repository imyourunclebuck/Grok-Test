#!/usr/bin/env python3
"""Grok Context Loader

Purpose: When a new Grok conversation starts, this script tells the assistant
how to bootstrap context from this repository before doing anything else.

Usage (from the repo root):
    python3 grok-context-loader.py

What it does:
1. Reads conversation-history.txt (the running transcript of our voice chats).
2. Prints a compact summary the assistant can paste into its first reply.
3. Lists the other files in the repo so the assistant knows what else exists.

Design notes:
- Plain text, no dependencies, runs on any machine with Python 3.
- The assistant should run this (or read the files directly) at the start of
  every session rather than relying on in-chat memory, which does not persist.
- New conversations should treat this repo as the source of truth.
"""

from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
HISTORY_FILE = REPO_ROOT / "conversation-history.txt"


def load_history(path: Path) -> str:
    if not path.exists():
        return "(no conversation history file found)"
    return path.read_text(encoding="utf-8")


def list_repo_files(root: Path) -> list[str]:
    entries = []
    for item in sorted(root.iterdir()):
        if item.name.startswith("."):
            continue
        kind = "dir" if item.is_dir() else "file"
        entries.append(f"{kind}: {item.name}")
    return entries


def main() -> None:
    print("=== GROK CONTEXT LOADER ===")
    print(f"Repo root: {REPO_ROOT}")
    print()
    print("--- Repository contents ---")
    for entry in list_repo_files(REPO_ROOT):
        print(f"  {entry}")
    print()
    print("--- Conversation history (full) ---")
    print(load_history(HISTORY_FILE))
    print()
    print("=== END OF CONTEXT ===")
    print("Assistant: treat the history above as prior context for this session.")
    print("Assistant: update conversation-history.txt after each session so the")
    print("Assistant: next conversation can pick up where this one left off.")


if __name__ == "__main__":
    main()

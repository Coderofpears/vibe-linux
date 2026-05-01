#!/usr/bin/env python3
"""Example Vibe plugin: print basic system information."""

from __future__ import annotations

import os
import platform
from pathlib import Path


def read_os_name() -> str:
    os_release = Path("/etc/os-release")
    if not os_release.exists():
        return "Unknown Linux"
    values = {}
    for line in os_release.read_text(encoding="utf-8", errors="ignore").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            values[key] = value.strip('"')
    return values.get("PRETTY_NAME", values.get("NAME", "Unknown Linux"))


def main() -> int:
    print(f"Plugin: {os.environ.get('VIBE_PLUGIN_ID', 'unknown')}")
    print(f"OS: {read_os_name()}")
    print(f"Kernel: {platform.release()}")
    print(f"Machine: {platform.machine()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


#!/usr/bin/env python3
"""Local-first OSS assistant plugin for Vibe-Linux OS."""

from __future__ import annotations

import argparse
import platform
from pathlib import Path


def read_key_value_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            values[key] = value.strip().strip('"')
    return values


def memory_summary() -> str:
    meminfo = read_key_value_file(Path("/proc/meminfo"))
    total = meminfo.get("MemTotal")
    if not total:
        return "Memory information is unavailable."
    gib = int(total.split()[0]) / 1024 / 1024
    mode = "Full Mode" if gib >= 15 else "Lite Mode"
    return f"{gib:.1f} GiB RAM detected. Suggested default: {mode}."


def diagnose() -> int:
    os_release = read_key_value_file(Path("/etc/os-release"))
    print("Vibe Copilot")
    print("============")
    print(f"System: {os_release.get('PRETTY_NAME', 'Unknown Linux')}")
    print(f"Kernel: {platform.release()}")
    print(memory_summary())
    print("Try: vibectl update")
    print("Try: vibectl diagnostics")
    print("Try: vibectl plugins list")
    return 0


def explain(topic: str) -> int:
    topics = {
        "update": "Updates are handled by pacman through vibectl: run `vibectl update`.",
        "apps": "Install apps with `vibectl install <name>`. Advanced users can still use pacman directly.",
        "plugins": "Plugins must declare permissions and run through vibe-plugin-runtime.",
        "modes": "Use `vibectl mode full`, `vibectl mode lite`, or `vibectl mode performance`.",
        "windows": "Vibe maps familiar Windows habits to KDE: Super opens Start, Super+E opens Files, Super+I opens Settings.",
    }
    print(topics.get(topic, "I can explain: update, apps, plugins, modes, windows."))
    return 0


def suggest(goal: str) -> int:
    goal = goal.lower()
    if "browser" in goal or "web" in goal:
        print("Suggested command: vibectl install firefox")
    elif "code" in goal or "develop" in goal:
        print("Suggested command: vibectl install git base-devel code")
    elif "fast" in goal or "performance" in goal:
        print("Suggested command: vibectl mode performance")
    elif "lite" in goal or "slow" in goal:
        print("Suggested command: vibectl mode lite")
    else:
        print("Suggested first step: vibectl diagnostics")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Vibe Copilot local assistant")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("diagnose", help="summarize system state")
    explain_parser = sub.add_parser("explain", help="explain a Vibe concept")
    explain_parser.add_argument("topic")
    suggest_parser = sub.add_parser("suggest", help="suggest a vibectl action")
    suggest_parser.add_argument("goal", nargs="+")

    args = parser.parse_args()
    if args.command == "explain":
        return explain(args.topic)
    if args.command == "suggest":
        return suggest(" ".join(args.goal))
    return diagnose()


if __name__ == "__main__":
    raise SystemExit(main())


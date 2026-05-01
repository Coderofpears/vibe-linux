#!/usr/bin/env python3
"""Example package-aware plugin that delegates system changes to vibectl."""

from __future__ import annotations

import shutil
import subprocess
import sys


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: plugin.py <package>")
        return 2
    vibectl = shutil.which("vibectl")
    if not vibectl:
        print("vibectl is unavailable in the sandbox", file=sys.stderr)
        return 2
    package = sys.argv[1]
    return subprocess.run([vibectl, "install", "--dry-run", package], check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())


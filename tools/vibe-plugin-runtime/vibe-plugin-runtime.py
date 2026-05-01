#!/usr/bin/env python3
"""Manifest-driven sandbox runtime for Vibe Plugin System plugins."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SYSTEM_LOG = Path("/var/log/vibe/plugins.log")
USER_LOG = Path.home() / ".local/state/vibe-linux/plugins.log"
SUPPORTED_RUNTIMES = {"python", "shell"}
PERMISSION_KEYS = {"filesystem", "network", "packages", "process", "system"}


class ManifestError(RuntimeError):
    pass


@dataclass(frozen=True)
class FileGrant:
    path: Path
    access: str


@dataclass(frozen=True)
class PluginManifest:
    plugin_id: str
    name: str
    version: str
    entry: str
    runtime: str
    permissions: dict[str, Any]


def read_manifest(plugin_dir: Path) -> PluginManifest:
    manifest_path = plugin_dir / "manifest.json"
    if not manifest_path.exists():
        raise ManifestError(f"manifest.json not found in {plugin_dir}")
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ManifestError(f"Invalid manifest JSON: {exc}") from exc

    required = ["id", "name", "version", "entry", "runtime", "permissions"]
    missing = [key for key in required if key not in data]
    if missing:
        raise ManifestError(f"Missing manifest keys: {', '.join(missing)}")

    runtime = data["runtime"]
    if runtime not in SUPPORTED_RUNTIMES:
        raise ManifestError(f"Unsupported runtime: {runtime}")

    entry = Path(data["entry"])
    if entry.is_absolute() or ".." in entry.parts:
        raise ManifestError("Entry point must be a relative path inside the plugin directory")
    if not (plugin_dir / entry).exists():
        raise ManifestError(f"Entry point not found: {entry}")

    permissions = data["permissions"]
    if not isinstance(permissions, dict):
        raise ManifestError("permissions must be an object")
    unknown = set(permissions) - PERMISSION_KEYS
    if unknown:
        raise ManifestError(f"Unknown permission keys: {', '.join(sorted(unknown))}")

    return PluginManifest(
        plugin_id=data["id"],
        name=data["name"],
        version=data["version"],
        entry=data["entry"],
        runtime=runtime,
        permissions=permissions,
    )


def file_grants(manifest: PluginManifest) -> list[FileGrant]:
    grants = manifest.permissions.get("filesystem", [])
    if grants in (None, False):
        return []
    if not isinstance(grants, list):
        raise ManifestError("filesystem permission must be a list")

    parsed: list[FileGrant] = []
    for grant in grants:
        if not isinstance(grant, dict):
            raise ManifestError("filesystem grants must be objects")
        path = Path(str(grant.get("path", ""))).resolve()
        access = grant.get("access", "read")
        if access not in {"read", "write"}:
            raise ManifestError(f"Invalid filesystem access for {path}: {access}")
        if not str(path).startswith("/"):
            raise ManifestError(f"Filesystem grant must be absolute: {path}")
        parsed.append(FileGrant(path=path, access=access))
    return parsed


def log_event(event: dict[str, Any]) -> None:
    event = {"timestamp": int(time.time()), **event}
    line = json.dumps(event, sort_keys=True)
    for path in (SYSTEM_LOG, USER_LOG):
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as handle:
                handle.write(line + "\n")
            return
        except OSError:
            continue
    print(line, file=sys.stderr)


def runtime_command(manifest: PluginManifest, args: list[str]) -> list[str]:
    entry = f"/plugin/{manifest.entry}"
    if manifest.runtime == "python":
        return ["/usr/bin/python", entry, *args]
    if manifest.runtime == "shell":
        return ["/usr/bin/bash", entry, *args]
    raise ManifestError(f"Unsupported runtime: {manifest.runtime}")


def build_bwrap_command(plugin_dir: Path, manifest: PluginManifest, args: list[str]) -> list[str]:
    bwrap = shutil.which("bwrap")
    if not bwrap:
        raise ManifestError("bubblewrap is required to run plugins on Linux")

    command = [
        bwrap,
        "--die-with-parent",
        "--new-session",
        "--ro-bind",
        "/usr",
        "/usr",
        "--tmpfs",
        "/etc",
        "--dev",
        "/dev",
        "--tmpfs",
        "/tmp",
        "--proc",
        "/proc",
        "--setenv",
        "HOME",
        "/tmp",
        "--setenv",
        "VIBE_PLUGIN_ID",
        manifest.plugin_id,
        "--ro-bind",
        str(plugin_dir),
        "/plugin",
        "--chdir",
        "/plugin",
    ]

    if args and args[0] == "--":
        args = args[1:]

    if not manifest.permissions.get("network", False):
        command.append("--unshare-net")
    else:
        for host_path in (Path("/etc/resolv.conf"), Path("/etc/ssl"), Path("/etc/ca-certificates")):
            if host_path.exists():
                command.extend(["--ro-bind", str(host_path), str(host_path)])

    if not manifest.permissions.get("process", False):
        command.extend(["--unshare-pid"])

    for grant in file_grants(manifest):
        if not grant.path.exists():
            raise ManifestError(f"Granted path does not exist: {grant.path}")
        bind_flag = "--bind" if grant.access == "write" else "--ro-bind"
        command.extend([bind_flag, str(grant.path), str(grant.path)])

    if manifest.permissions.get("packages", False):
        vibectl = shutil.which("vibectl")
        if not vibectl:
            raise ManifestError("packages permission requires vibectl in PATH")
        command.extend(["--ro-bind", str(Path(vibectl).resolve()), "/usr/bin/vibectl"])

    command.extend(["--", *runtime_command(manifest, args)])
    return command


def validate_plugin(plugin_dir: Path) -> PluginManifest:
    plugin_dir = plugin_dir.resolve()
    if not plugin_dir.is_dir():
        raise ManifestError(f"Plugin path is not a directory: {plugin_dir}")
    manifest = read_manifest(plugin_dir)
    file_grants(manifest)
    return manifest


def run_plugin(plugin_dir: Path, args: list[str], dry_run: bool = False) -> int:
    plugin_dir = plugin_dir.resolve()
    manifest = validate_plugin(plugin_dir)
    log_event(
        {
            "event": "plugin_run_requested",
            "plugin_id": manifest.plugin_id,
            "version": manifest.version,
            "permissions": manifest.permissions,
        }
    )

    if sys.platform != "linux":
        raise ManifestError("Plugin sandbox execution is only supported on Linux")

    command = build_bwrap_command(plugin_dir, manifest, args)
    if dry_run:
        print(" ".join(command))
        return 0

    completed = subprocess.run(command, check=False)
    log_event(
        {
            "event": "plugin_run_completed",
            "plugin_id": manifest.plugin_id,
            "returncode": completed.returncode,
        }
    )
    return completed.returncode


def cmd_validate(args: argparse.Namespace) -> int:
    manifest = validate_plugin(Path(args.plugin_dir))
    print(json.dumps({
        "id": manifest.plugin_id,
        "name": manifest.name,
        "version": manifest.version,
        "runtime": manifest.runtime,
        "entry": manifest.entry,
        "permissions": manifest.permissions,
    }, indent=2, sort_keys=True))
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    return run_plugin(Path(args.plugin_dir), args.args, args.dry_run)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="vibe-plugin-runtime", description="Run Vibe plugins in a sandbox")
    sub = parser.add_subparsers(required=True)

    validate = sub.add_parser("validate", help="validate a plugin manifest")
    validate.add_argument("plugin_dir")
    validate.set_defaults(func=cmd_validate)

    run_cmd = sub.add_parser("run", help="run a plugin")
    run_cmd.add_argument("plugin_dir")
    run_cmd.add_argument("--dry-run", action="store_true")
    run_cmd.add_argument("args", nargs=argparse.REMAINDER)
    run_cmd.set_defaults(func=cmd_run)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ManifestError as exc:
        print(f"vibe-plugin-runtime: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

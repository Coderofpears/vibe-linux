#!/usr/bin/env python3
"""Unified system management CLI for Vibe-Linux OS."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


SYSTEM_PLUGIN_DIR = Path("/usr/share/vibe-linux/plugins")
USER_PLUGIN_DIR = Path.home() / ".local/share/vibe-linux/plugins"
USER_STATE_DIR = Path.home() / ".local/state/vibe-linux"
ENABLED_PLUGINS = USER_STATE_DIR / "enabled-plugins.json"
SOURCE_ROOT = Path(__file__).resolve().parents[2]
MODE_DIRS = [Path("/usr/share/vibe-linux/modes"), SOURCE_ROOT / "configs/modes", Path.cwd() / "configs/modes"]
LOG_DIR = Path("/var/log/vibe")


class VibeError(RuntimeError):
    pass


def run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=check, text=True)


def require_command(name: str) -> str:
    found = shutil.which(name)
    if not found:
        raise VibeError(f"Required command not found: {name}")
    return found


def pacman_command(args: list[str], *, dry_run: bool = False) -> int:
    command = ["pacman", *args]
    if os.geteuid() != 0:
        command.insert(0, "sudo")
    print(" ".join(command))
    if dry_run:
        return 0
    require_command("pacman")
    if command[0] == "sudo":
        require_command("sudo")
    return run(command).returncode


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


@dataclass
class PluginRef:
    plugin_id: str
    path: Path
    enabled: bool
    name: str
    version: str


def plugin_manifest(plugin_path: Path) -> dict:
    manifest_path = plugin_path / "manifest.json"
    if not manifest_path.exists():
        raise VibeError(f"Plugin manifest not found: {manifest_path}")
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def discover_plugins() -> list[PluginRef]:
    enabled = set(load_json(ENABLED_PLUGINS, []))
    refs: list[PluginRef] = []
    for root in (SYSTEM_PLUGIN_DIR, USER_PLUGIN_DIR):
        if not root.exists():
            continue
        for plugin_path in sorted(path for path in root.iterdir() if path.is_dir()):
            try:
                manifest = plugin_manifest(plugin_path)
            except (OSError, json.JSONDecodeError, VibeError):
                continue
            plugin_id = manifest.get("id", plugin_path.name)
            refs.append(
                PluginRef(
                    plugin_id=plugin_id,
                    path=plugin_path,
                    enabled=plugin_id in enabled,
                    name=manifest.get("name", plugin_id),
                    version=manifest.get("version", "unknown"),
                )
            )
    return refs


def find_plugin(plugin_id: str) -> PluginRef:
    for ref in discover_plugins():
        if ref.plugin_id == plugin_id:
            return ref
    raise VibeError(f"Plugin not found: {plugin_id}")


def cmd_update(args: argparse.Namespace) -> int:
    return pacman_command(["-Syu"], dry_run=args.dry_run)


def cmd_install(args: argparse.Namespace) -> int:
    return pacman_command(["-S", "--needed", *args.packages], dry_run=args.dry_run)


def cmd_remove(args: argparse.Namespace) -> int:
    return pacman_command(["-Rns", *args.packages], dry_run=args.dry_run)


def cmd_diagnostics(_args: argparse.Namespace) -> int:
    print("Vibe-Linux diagnostics")
    print("======================")
    print(f"system: {platform.platform()}")
    print(f"python: {sys.version.split()[0]}")
    print(f"machine: {platform.machine()}")

    meminfo = Path("/proc/meminfo")
    if meminfo.exists():
        for line in meminfo.read_text(encoding="utf-8", errors="ignore").splitlines()[:3]:
            print(line)

    for command in ("pacman", "systemctl", "bwrap", "vibe-plugin-runtime"):
        print(f"{command}: {shutil.which(command) or 'missing'}")
    return 0


def load_mode(mode: str) -> dict:
    for root in MODE_DIRS:
        candidate = root / f"{mode}.json"
        if candidate.exists():
            return json.loads(candidate.read_text(encoding="utf-8"))
    raise VibeError(f"Unknown mode: {mode}")


def systemctl(action: str, unit: str, dry_run: bool) -> None:
    command = ["systemctl", action, unit]
    if os.geteuid() != 0:
        command.insert(0, "sudo")
    print(" ".join(command))
    if not dry_run:
        subprocess.run(command, check=False)


def cmd_mode(args: argparse.Namespace) -> int:
    mode = load_mode(args.mode)
    print(f"Applying mode: {mode['name']}")
    print(mode.get("description", ""))

    for unit in mode.get("enable_services", []):
        systemctl("enable", unit, args.dry_run)
        systemctl("start", unit, args.dry_run)
    for unit in mode.get("disable_services", []):
        systemctl("disable", unit, args.dry_run)
        systemctl("stop", unit, args.dry_run)

    mode_file = Path("/etc/vibe-mode")
    command = ["tee", str(mode_file)]
    if os.geteuid() != 0:
        command.insert(0, "sudo")
    print(" ".join(command))
    if not args.dry_run:
        subprocess.run(command, input=args.mode + "\n", text=True, check=True)
    return 0


def cmd_plugins_list(_args: argparse.Namespace) -> int:
    refs = discover_plugins()
    if not refs:
        print("No plugins installed.")
        return 0
    for ref in refs:
        status = "enabled" if ref.enabled else "disabled"
        print(f"{ref.plugin_id}\t{ref.version}\t{status}\t{ref.path}")
    return 0


def cmd_plugins_install(args: argparse.Namespace) -> int:
    source = Path(args.path).expanduser().resolve()
    manifest = plugin_manifest(source)
    plugin_id = manifest.get("id")
    if not plugin_id:
        raise VibeError(f"Plugin manifest is missing id: {source}")
    destination_root = SYSTEM_PLUGIN_DIR if args.system else USER_PLUGIN_DIR
    destination = destination_root / plugin_id

    if args.system and os.geteuid() != 0:
        raise VibeError("System plugin install must run as root. Try sudo vibectl plugins install --system <path>.")
    if destination.exists() and not args.force:
        raise VibeError(f"Plugin already installed: {plugin_id}. Use --force to replace it.")
    if destination.exists():
        shutil.rmtree(destination)
    destination_root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination)
    print(f"Installed {plugin_id} to {destination}")
    return 0


def cmd_plugins_enable(args: argparse.Namespace) -> int:
    find_plugin(args.plugin_id)
    enabled = set(load_json(ENABLED_PLUGINS, []))
    enabled.add(args.plugin_id)
    write_json(ENABLED_PLUGINS, sorted(enabled))
    print(f"Enabled {args.plugin_id}")
    return 0


def cmd_plugins_disable(args: argparse.Namespace) -> int:
    enabled = set(load_json(ENABLED_PLUGINS, []))
    enabled.discard(args.plugin_id)
    write_json(ENABLED_PLUGINS, sorted(enabled))
    print(f"Disabled {args.plugin_id}")
    return 0


def cmd_plugins_run(args: argparse.Namespace) -> int:
    ref = find_plugin(args.plugin_id)
    enabled = set(load_json(ENABLED_PLUGINS, []))
    if ref.plugin_id not in enabled and not args.once:
        raise VibeError(f"Plugin is not enabled: {ref.plugin_id}. Use --once to run without enabling.")

    runtime = shutil.which("vibe-plugin-runtime")
    if not runtime:
        local_runtime = Path(__file__).resolve().parents[1] / "vibe-plugin-runtime" / "vibe-plugin-runtime.py"
        runtime = str(local_runtime) if local_runtime.exists() else None
    if not runtime:
        raise VibeError("vibe-plugin-runtime not found.")

    command = [runtime, "run", str(ref.path), *args.plugin_args]
    if args.plugin_args:
        command = [runtime, "run", str(ref.path), "--", *args.plugin_args]
    return run(command).returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="vibectl", description="Vibe-Linux system control")
    sub = parser.add_subparsers(required=True)

    update = sub.add_parser("update", help="update the system through pacman")
    update.add_argument("--dry-run", action="store_true")
    update.set_defaults(func=cmd_update)

    install = sub.add_parser("install", help="install packages through pacman")
    install.add_argument("packages", nargs="+")
    install.add_argument("--dry-run", action="store_true")
    install.set_defaults(func=cmd_install)

    remove = sub.add_parser("remove", help="remove packages through pacman")
    remove.add_argument("packages", nargs="+")
    remove.add_argument("--dry-run", action="store_true")
    remove.set_defaults(func=cmd_remove)

    diagnostics = sub.add_parser("diagnostics", help="print system diagnostics")
    diagnostics.set_defaults(func=cmd_diagnostics)

    mode = sub.add_parser("mode", help="switch performance profile")
    mode.add_argument("mode", choices=["full", "lite", "performance"])
    mode.add_argument("--dry-run", action="store_true")
    mode.set_defaults(func=cmd_mode)

    plugins = sub.add_parser("plugins", help="manage Vibe plugins")
    plugins_sub = plugins.add_subparsers(required=True)

    plugins_list = plugins_sub.add_parser("list", help="list installed plugins")
    plugins_list.set_defaults(func=cmd_plugins_list)

    plugins_install = plugins_sub.add_parser("install", help="install a plugin directory")
    plugins_install.add_argument("path")
    plugins_install.add_argument("--system", action="store_true", help="install to the system plugin directory")
    plugins_install.add_argument("--force", action="store_true", help="replace an existing plugin")
    plugins_install.set_defaults(func=cmd_plugins_install)

    plugins_enable = plugins_sub.add_parser("enable", help="enable a plugin")
    plugins_enable.add_argument("plugin_id")
    plugins_enable.set_defaults(func=cmd_plugins_enable)

    plugins_disable = plugins_sub.add_parser("disable", help="disable a plugin")
    plugins_disable.add_argument("plugin_id")
    plugins_disable.set_defaults(func=cmd_plugins_disable)

    plugins_run = plugins_sub.add_parser("run", help="run an enabled plugin")
    plugins_run.add_argument("--once", action="store_true", help="run without enabling first")
    plugins_run.add_argument("plugin_id")
    plugins_run.add_argument("plugin_args", nargs=argparse.REMAINDER)
    plugins_run.set_defaults(func=cmd_plugins_run)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except VibeError as exc:
        print(f"vibectl: {exc}", file=sys.stderr)
        return 2
    except subprocess.CalledProcessError as exc:
        return exc.returncode


if __name__ == "__main__":
    raise SystemExit(main())

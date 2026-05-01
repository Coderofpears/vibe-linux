#!/usr/bin/env python3
"""Guided installer entry point for the Vibe-Linux live ISO."""

from __future__ import annotations

import argparse
import getpass
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path


LOG_PATH = Path("/var/log/vibe-installer.log")
ARCHINSTALL_CONFIG = Path("/tmp/vibe-archinstall.json")
ARCHINSTALL_CREDS = Path("/tmp/vibe-creds.json")
REPO_ROOT = Path("/opt/vibe-linux")


@dataclass
class InstallPlan:
    mode: str
    disk: str
    hostname: str
    username: str
    timezone: str
    keyboard: str
    desktop: str
    performance_profile: str
    packages: list[str]
    services: list[str]
    driver_notes: list[str]


def log(message: str) -> None:
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as handle:
            handle.write(message + "\n")
    except OSError:
        pass


def run_capture(command: list[str]) -> str:
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def detect_memory_gib() -> float:
    meminfo = Path("/proc/meminfo")
    if not meminfo.exists():
        return 0
    for line in meminfo.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("MemTotal:"):
            return int(line.split()[1]) / 1024 / 1024
    return 0


def detect_drivers() -> tuple[list[str], list[str]]:
    lspci = run_capture(["lspci", "-nnk"]).lower()
    packages: set[str] = set()
    notes: list[str] = []

    if "nvidia" in lspci:
        packages.update({"mesa", "vulkan-nouveau", "xf86-video-nouveau"})
        notes.append("NVIDIA GPU detected; OSS Nouveau/Mesa driver packages selected. Proprietary drivers are not installed by default.")
    if "amd" in lspci or "advanced micro devices" in lspci:
        packages.update({"mesa", "vulkan-radeon", "xf86-video-amdgpu"})
        notes.append("AMD graphics detected; open-source Mesa/Vulkan packages selected.")
    if "intel corporation" in lspci:
        packages.update({"mesa", "vulkan-intel", "intel-media-driver", "xf86-video-intel"})
        notes.append("Intel hardware detected; Intel graphics/media packages selected.")
    if "wireless" in lspci or "wi-fi" in lspci or "wifi" in lspci:
        packages.update({"networkmanager", "iwd", "wpa_supplicant"})
        notes.append("Wireless hardware detected; NetworkManager and Wi-Fi tooling selected.")

    return sorted(packages), notes or ["No special driver packages detected."]


def list_disks() -> list[str]:
    output = run_capture(["lsblk", "-dnpo", "NAME,TYPE,SIZE,MODEL"])
    disks = []
    for line in output.splitlines():
        parts = line.split(None, 2)
        if len(parts) >= 2 and parts[1] == "disk":
            disks.append(parts[0])
    return disks


def prompt(label: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or (default or "")


def choose(label: str, options: list[str], default_index: int = 0) -> str:
    print(f"\n{label}")
    for idx, option in enumerate(options, start=1):
        marker = " (default)" if idx - 1 == default_index else ""
        print(f"  {idx}. {option}{marker}")
    raw = prompt("Choose", str(default_index + 1))
    try:
        selected = int(raw) - 1
    except ValueError:
        selected = default_index
    if selected < 0 or selected >= len(options):
        selected = default_index
    return options[selected]


def build_plan() -> InstallPlan:
    print("Vibe-Linux OS Installer")
    print("=======================\n")
    print("This guided flow will prepare an Arch-based Vibe-Linux installation.")

    install_mode = choose("Install mode", ["full", "custom"], 0)
    disks = list_disks()
    if not disks:
        raise SystemExit("No installable disks found.")
    disk = choose("Target disk. Full install will erase the selected disk.", disks, 0)

    mem_gib = detect_memory_gib()
    suggested_profile = "full" if mem_gib >= 15 else "lite"

    hostname = prompt("Hostname", "vibe-linux")
    username = prompt("Username", "vibe")
    timezone = prompt("Timezone", "America/New_York")
    keyboard = prompt("Keyboard layout", "us")
    desktop = choose("Desktop session", ["kde", "kde+hyprland"], 0)
    profile = choose("Performance profile", ["full", "lite", "performance"], 0 if suggested_profile == "full" else 1)

    driver_packages, driver_notes = detect_drivers()
    base_packages = [
        "base-devel",
        "git",
        "firefox",
        "konsole",
        "dolphin",
        "kate",
        "python",
        "python-psutil",
        "bubblewrap",
        "plasma-meta",
        "kde-system-meta",
        "sddm",
        "kdeconnect",
        "kio-extras",
        "partitionmanager",
        "touchegg",
        "pipewire",
        "wireplumber",
        "reflector",
        "pacman-contrib",
    ]
    if desktop == "kde+hyprland":
        base_packages.extend(["hyprland", "waybar", "wofi", "kitty"])

    services = ["NetworkManager", "sddm", "touchegg"]

    return InstallPlan(
        mode=install_mode,
        disk=disk,
        hostname=hostname,
        username=username,
        timezone=timezone,
        keyboard=keyboard,
        desktop=desktop,
        performance_profile=profile,
        packages=sorted(set(base_packages + driver_packages)),
        services=services,
        driver_notes=driver_notes,
    )


def generate_archinstall_config(plan: InstallPlan) -> dict:
    return {
        "config_version": "2.8.0",
        "hostname": plan.hostname,
        "timezone": plan.timezone,
        "ntp": True,
        "parallel downloads": 5,
        "kernels": ["linux"],
        "bootloader": "grub-install",
        "swap": True,
        "locale_config": {
            "kb_layout": plan.keyboard,
            "sys_enc": "UTF-8",
            "sys_lang": "en_US",
        },
        "network_config": {"type": "nm"},
        "audio_config": {"audio": "pipewire"},
        "disk_config": {
            "config_type": "default_layout",
            "device_modifications": [
                {
                    "device": plan.disk,
                    "wipe": True,
                }
            ],
        },
        "profile_config": {
            "gfx_driver": "All open-source",
            "greeter": "sddm",
            "profile": {
                "main": "Desktop",
                "details": ["KDE Plasma"],
                "custom_settings": {},
            },
        },
        "packages": plan.packages,
        "services": plan.services,
        "custom-commands": [
            "mkdir -p /usr/share/vibe-linux /var/lib/vibe/plugins /var/log/vibe",
            f"printf '%s\\n' '{plan.performance_profile}' > /etc/vibe-mode",
            "systemctl enable NetworkManager sddm touchegg",
        ],
        "version": "2.8.0",
    }


def write_creds(username: str) -> None:
    print("\nSet passwords")
    root_pw = getpass.getpass("Root password: ")
    user_pw = getpass.getpass(f"Password for {username}: ")
    creds = {
        "!root-password": root_pw,
        "!users": [
            {
                "username": username,
                "!password": user_pw,
                "sudo": True,
            }
        ],
    }
    ARCHINSTALL_CREDS.write_text(json.dumps(creds, indent=2), encoding="utf-8")
    ARCHINSTALL_CREDS.chmod(0o600)


def print_review(plan: InstallPlan) -> None:
    print("\nInstall Review")
    print("==============")
    for key, value in asdict(plan).items():
        if key == "packages":
            print(f"{key}: {len(value)} packages")
        elif key == "driver_notes":
            print("driver notes:")
            for note in value:
                print(f"  - {note}")
        else:
            print(f"{key}: {value}")


def run_archinstall(dry_run: bool) -> None:
    if dry_run:
        print(f"\nDry run complete. Generated config: {ARCHINSTALL_CONFIG}")
        print(ARCHINSTALL_CONFIG.read_text(encoding="utf-8"))
        return

    if shutil.which("archinstall") is None:
        raise SystemExit("archinstall not found in PATH.")

    command = [
        "archinstall",
        "--config",
        str(ARCHINSTALL_CONFIG),
        "--creds",
        str(ARCHINSTALL_CREDS),
    ]
    log("Running: " + " ".join(command))
    subprocess.run(command, check=True)


def install_vibe_tools(dry_run: bool) -> None:
    script = REPO_ROOT / "scripts" / "install-vibe-tools.sh"
    if dry_run:
        print(f"\nWould install Vibe tools with: {script} /mnt")
        return
    if script.exists() and Path("/mnt").is_dir():
        subprocess.run([str(script), "/mnt"], check=True)
    else:
        log("Skipped Vibe tool install; script or /mnt not available after archinstall.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Vibe-Linux guided installer")
    parser.add_argument("--dry-run", action="store_true", help="generate and print archinstall config without installing")
    args = parser.parse_args()

    plan = build_plan()
    print_review(plan)

    if not args.dry_run:
        confirmation = prompt("\nType INSTALL to erase the disk and continue")
        if confirmation != "INSTALL":
            print("Install cancelled.")
            return 1
        write_creds(plan.username)

    config = generate_archinstall_config(plan)
    ARCHINSTALL_CONFIG.write_text(json.dumps(config, indent=2), encoding="utf-8")
    run_archinstall(args.dry_run)
    install_vibe_tools(args.dry_run)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nInstaller cancelled.")
        raise SystemExit(130)

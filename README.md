# Vibe-Linux OS

Vibe-Linux OS is an Arch-based distribution foundation focused on a simple installer, a polished KDE-first desktop, developer tooling, and a secure plugin runtime.

This repository contains the first working scaffold:

- ArchISO profile customization for building a Vibe installer ISO.
- A Windows-style guided installer flow backed by `archinstall`.
- `vibectl`, a unified system CLI for updates, packages, modes, diagnostics, and plugins.
- `vibe-plugin-runtime`, a manifest-driven plugin runner with explicit permissions and bubblewrap sandboxing.
- KDE Plasma and Hyprland defaults.
- A sample plugin that demonstrates the Vibe Plugin System.
- OSS-first defaults under the MIT License.
- Windows-familiar shortcuts, gestures, copy, and UX mappings.
- A local-first `Vibe Copilot` assistant plugin that runs through VPS.

## Quick Start

On an Arch Linux build host:

```bash
sudo pacman -Syu --needed archiso archinstall python python-psutil bubblewrap git rsync
sudo ./scripts/build-iso.sh
```

The ISO output is written to `out/`.

For local CLI syntax checks on any machine with Python 3.11+:

```bash
python -m compileall tools installer
python tools/vibectl/vibectl.py --help
python tools/vibe-plugin-runtime/vibe-plugin-runtime.py --help
./scripts/smoke-test.sh
```

## Repository Layout

```text
.
├── archiso/                    # ArchISO profile for the installer image
├── configs/                    # Desktop, mode, and system defaults
├── docs/                       # Architecture, installer, security docs
├── examples/plugins/           # Example VPS plugins
├── installer/                  # Guided installer and archinstall profiles
├── packaging/                  # Pacman package metadata templates
├── scripts/                    # ISO and install bootstrap scripts
├── systemd/                    # Service units used by Vibe-Linux
└── tools/
    ├── vibectl/                # Unified system management CLI
    └── vibe-plugin-runtime/    # Secure plugin runtime
```

## Design Goals

Vibe-Linux OS should feel easy at the surface and transparent underneath:

- KDE Plasma by default, with sane Windows/macOS-like ergonomics.
- Arch Linux rolling base with pacman compatibility.
- A plugin ecosystem that uses manifests, permission prompts, scoped filesystem access, and sandboxed execution instead of arbitrary privileged scripts.
- Full and Lite performance profiles for machines from lower-spec laptops to 16GB+ developer workstations.
- A direct Windows alternative for daily use: familiar taskbar, launcher, shortcuts, touchpad gestures, phone integration, GUI settings, and assistant workflows.
- Open-source defaults. Proprietary drivers or cloud assistants are optional add-ons, not base-system requirements.

## Windows Alternative Layer

See [docs/windows-alternative.md](docs/windows-alternative.md). The default UX maps familiar Windows concepts to KDE Plasma and Vibe tools:

- Start: KDE Application Launcher.
- Files: Dolphin with `Super+E`.
- Settings: KDE System Settings with `Super+I`.
- Updates: `vibectl update`.
- Copilot-style help: `vibectl plugins run --once dev.vibe.copilot`.

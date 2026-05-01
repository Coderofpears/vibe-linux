# Vibe-Linux OS Architecture

## System Diagram

```text
┌─────────────────────────────────────────────────────────────────────┐
│                           Vibe-Linux OS                              │
├─────────────────────────────────────────────────────────────────────┤
│ Desktop Layer                                                        │
│  ├─ KDE Plasma default session                                       │
│  ├─ Optional Hyprland advanced session                               │
│  └─ Vibe themes, icons, panels, gestures, shortcuts, mode profiles   │
├─────────────────────────────────────────────────────────────────────┤
│ User Management Layer                                                │
│  ├─ vibectl                                                          │
│  │  ├─ update/install/remove wrappers around pacman                   │
│  │  ├─ diagnostics                                                   │
│  │  ├─ performance mode switching                                    │
│  │  └─ plugin manager commands                                       │
│  └─ Vibe Installer                                                   │
│     ├─ guided install                                                │
│     ├─ custom install                                                │
│     └─ archinstall backend                                           │
├─────────────────────────────────────────────────────────────────────┤
│ Secure Extension Layer                                               │
│  ├─ Vibe Plugin System manifests                                     │
│  ├─ vibe-plugin-runtime                                              │
│  ├─ bubblewrap sandbox                                               │
│  ├─ scoped permission grants                                         │
│  └─ privileged action log                                            │
├─────────────────────────────────────────────────────────────────────┤
│ Core OS Layer                                                        │
│  ├─ Arch Linux base                                                  │
│  ├─ pacman                                                           │
│  ├─ systemd                                                          │
│  ├─ Linux kernel                                                     │
│  └─ hardware detection and driver packages                           │
└─────────────────────────────────────────────────────────────────────┘
```

## Foundation Principles

1. Arch remains the base. Vibe-Linux adds opinionated defaults and safer management surfaces instead of forking the package model.
2. `vibectl` is the front door for system-changing actions. It wraps pacman, plugin activation, mode switching, diagnostics, and approved privileged operations.
3. Plugins are untrusted by default. A plugin must declare permissions in `manifest.json`, and runtime execution is sandboxed with `bubblewrap` when run on Linux.
4. Installation is guided first, advanced second. The default flow automates partitioning, bootloader installation, desktop setup, driver detection, and user creation.
5. Desktop configuration is modular. KDE is the default, Hyprland is shipped as an opt-in advanced session.

## Boot and Install Flow

```text
Firmware
  ↓
Vibe ArchISO bootloader
  ↓
Live ISO session
  ↓
vibe-installer guided TUI
  ↓
archinstall profile generation
  ↓
Base install + KDE + drivers + vibectl + VPS
  ↓
First boot into Vibe-Linux OS
```

## Runtime Components

### `vibectl`

The unified CLI lives in `tools/vibectl`. It exposes:

- `vibectl update`
- `vibectl install <pkg>`
- `vibectl remove <pkg>`
- `vibectl plugins list|install|enable|run`
- `vibectl mode full|lite|performance`
- `vibectl diagnostics`

### `vibe-plugin-runtime`

The runtime lives in `tools/vibe-plugin-runtime`. It validates plugin manifests, builds a constrained sandbox, logs execution, and only grants declared permissions.

### Windows Alternative Layer

The Windows alternative layer lives under `configs/kde`, `configs/gestures`, and `configs/vibe`. It defines familiar shortcut mappings, touchpad gestures, system language, and the default visual personality.

### Installer

The installer lives in `installer/`. It uses a Python TUI to collect install choices and generates an `archinstall` configuration. Low-level ISO and chroot tasks stay in shell scripts.

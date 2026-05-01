# Windows Alternative UX

Vibe-Linux OS aims to be a direct daily-driver alternative for Windows users while remaining open and Arch-compatible underneath.

## Desktop Mapping

```text
Windows concept          Vibe-Linux equivalent
Start menu               KDE Application Launcher
Taskbar                  KDE bottom panel with pinned apps and tray
Action center            KDE system tray and notifications
Settings                 KDE System Settings
File Explorer            Dolphin
Phone Link               KDE Connect
Disk Management          KDE Partition Manager
Microsoft Store          Discover for app browsing, vibectl for system packages
Copilot                  Vibe Copilot plugin, OSS local-first by default
Windows Update           vibectl update
Task Manager             Plasma System Monitor
Snap Assist              KDE window tiling and shortcuts
```

## Keyboard Shortcuts

The default shortcuts intentionally mirror familiar Windows behavior:

- Super: open launcher.
- Super+E: open Dolphin.
- Super+I: open System Settings.
- Super+L: lock the session.
- Super+R: open command runner.
- Super+V: clipboard history.
- Print: screenshot.
- Super+Left/Right/Up/Down: tile, maximize, or minimize windows.

## Touchpad Gestures

Touchegg is included for cross-desktop gesture support:

- Three-finger swipe left/right: switch workspace.
- Three-finger swipe up: overview.
- Three-finger swipe down: show desktop.
- Four-finger swipe left/right: switch workspace.
- Four-finger pinch in: app launcher.

## Language Style

System-facing copy should be plain and reassuring:

- Say "Apps", not "packages", in beginner-facing UI.
- Say "Update your system", not "sync package databases".
- Say "Performance mode", not "governor profile".
- Show advanced Arch terms only after the user asks for detail.


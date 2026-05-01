# Vibe Installer Workflow

## User Experience

The installer should present three simple screens before confirmation:

1. Welcome and install mode.
2. Disk, locale, keyboard, timezone, username, hostname, and desktop choices.
3. Review, driver detection results, and install confirmation.

## Modes

- Full install: automated partitioning, KDE Plasma, common drivers, developer tools, `vibectl`, and plugin runtime.
- Custom install: exposes filesystem, bootloader, desktop, optional Hyprland, package groups, and mode defaults.

## Backend

The first implementation uses `archinstall` because it preserves Arch compatibility and avoids maintaining a bespoke installer backend. The Vibe installer generates a profile in `/tmp/vibe-archinstall.json` and launches:

```bash
archinstall --config /tmp/vibe-archinstall.json --creds /tmp/vibe-creds.json
```

## Driver Detection

The installer uses these signals:

- `lspci -nnk` for GPU, Wi-Fi, Bluetooth, and storage controllers.
- `lsusb` for USB Wi-Fi and peripheral hints.
- `/sys/firmware/efi` to detect UEFI.
- memory from `/proc/meminfo` to choose Full or Lite defaults.

Recommended package mappings are defined in `installer/vibe_installer/hardware.py`.

## Safety

- Full install requires explicit confirmation before destructive disk operations.
- Custom install can opt out of auto-partitioning.
- The generated archinstall profile is shown before execution when `--dry-run` is used.
- The installer writes logs to `/var/log/vibe-installer.log` on the live ISO.


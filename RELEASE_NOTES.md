# Vibe-Linux OS v0.1.0 Release Notes

**Release Date:** 2026-05-15  
**Version:** 0.1.0 (First Public Release, Finalized)

## Overview

Vibe-Linux OS is a modern Arch-based distribution designed to feel familiar on the surface (Windows-like UX) while remaining transparent and developer-friendly underneath. This first release includes a complete foundational system with installer, package management, and a secure plugin ecosystem.

## What's New

### Core System Components
- **ArchISO Profile**: Customized ArchISO profile for building Vibe-Linux installer ISOs
- **Guided Installer**: Windows-style multi-step installer powered by archinstall
- **Desktop Environments**: KDE Plasma by default, with Hyprland option
- **System CLI (vibectl)**: Unified command-line tool for:
  - System updates via pacman
  - Package installation/removal
  - Performance mode switching (Full/Lite/Performance)
  - System diagnostics
  - Plugin management and execution

### Plugin System
- **Secure Runtime**: Manifest-driven plugin execution with bubblewrap sandboxing
- **Permission Model**: Explicit permissions for filesystem, network, packages, process, and system access
- **Granular Filesystem Access**: Scoped read/write grants to specific paths
- **Multiple Runtimes**: Support for Python and Shell (Bash) entry points
- **Sample Plugins**: Three example plugins included:
  - Package Search: Search Arch repositories
  - System Info: Display hardware and OS information
  - Vibe Copilot: Local-first AI assistant integration

### Windows-Familiar UX Layer
Familiar shortcuts and UI patterns mapped to KDE Plasma:
- **Start/Apps**: KDE Application Launcher
- **File Manager**: Dolphin (Super+E)
- **Settings**: KDE System Settings (Super+I)
- **Updates**: `vibectl update`
- **System Assistant**: `vibectl plugins run --once dev.vibe.copilot`
- **Taskbar**: Native KDE panel
- **Notifications**: KDE notification system

### Open Source & Security
- MIT License - fully open source
- No proprietary cloud dependencies
- Optional proprietary drivers (not pre-installed)
- Security-focused plugin sandboxing

## Bug Fixes

### Fixed Issues (v0.1.0)
- **Plugin Argument Handling**: Corrected logic error in `vibectl plugins run` command
  - Issue: Plugin CLI arguments were incorrectly processed twice
  - Fix: Proper if-else logic for command construction with/without arguments
  - Impact: Plugins now correctly receive command-line arguments
- **Performance Mode Coverage**: Fixed `vibectl mode` to expose all shipped mode profiles
  - Issue: CLI hard-coded mode choices to `full`, `lite`, and `performance` only
  - Fix: Mode choices are now discovered dynamically from `configs/modes/*.json`
  - Impact: `gaming` and `development` modes are now selectable from the CLI

## System Requirements

### Build Host
- Arch Linux (or compatible system with archiso)
- Required packages: `archiso`, `archinstall`, `python`, `python-psutil`, `bubblewrap`, `git`, `rsync`

### Target Hardware
- x86_64 architecture
- **Minimum**: 4GB RAM (Lite profile)
- **Recommended**: 8GB+ RAM (Full profile)
- Any modern solid-state or hard drive

## Installation & Testing

### Build the Installer ISO
```bash
# On an Arch Linux build host
sudo pacman -Syu --needed archiso archinstall python python-psutil bubblewrap git rsync
cd /path/to/vibe-linux
sudo ./scripts/build-iso.sh
# Output ISO: out/vibe-linux-*.iso
```

### Local Testing (without building ISO)
```bash
# On any system with Python 3.11+
python3 -m compileall tools installer
python3 tools/vibectl/vibectl.py --help
python3 tools/vibe-plugin-runtime/vibe-plugin-runtime.py --help
./scripts/smoke-test.sh
```

### Installation Flow (on target hardware)
1. Boot from vibe-linux-*.iso
2. Run through guided installer
3. Choose installation mode (Full/Custom)
4. Select target disk, timezone, keyboard layout
5. Choose desktop session (KDE or KDE+Hyprland)
6. Select performance profile
7. System automatically detects hardware and configures drivers
8. Reboot and enjoy Vibe-Linux

## Repository Structure

```
vibe-linux/
 archiso/                    # Custom ArchISO profile
 configs/                    # Desktop configs, modes, system defaults
 docs/                       # Architecture and design documentation
 examples/
 plugins/                # Sample plugins (3 examples)   
 installer/                  # Guided installer scripts
 packaging/                  # Pacman package metadata
 scripts/                    # Build scripts and bootstrap
 systemd/                    # systemd service units
 tools/
 vibectl/                # System management CLI   
 vibe-plugin-runtime/    # Plugin sandbox runtime   
 CONTRIBUTING.md             # Contributing guidelines
 LICENSE                     # MIT License
 README.md                   # Main documentation
```

## Key Features

### Performance Profiles
- **Full**: For systems with 15GB+ RAM; all features enabled
- **Lite**: For systems with 4GB+ RAM; optimized defaults
- **Performance**: For developer workstations; custom resource tuning

### Plugin System Architecture
Plugins are defined by a `manifest.json`:
```json
{
  "id": "org.example.my-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "runtime": "python",
  "entry": "main.py",
  "permissions": {
    "filesystem": [
      { "path": "/home", "access": "read" }
    ],
    "network": false,
    "packages": false
  }
}
```

Plugins run in isolated bubblewrap environments with only declared permissions.

### Desktop & UX
- **KDE Plasma 6**: Default modern desktop environment
- **Hyprland**: Optional dynamic tiling WM for advanced users
- **Windows Mappings**: Familiar shortcuts (Win key, Alt+Tab, etc.)
- **Touchpad Gestures**: Multi-finger gestures via touchegg

## Known Limitations

- Plugin sandbox is Linux-only (bubblewrap requirement)
- ISO builds require Arch Linux build host
- Some proprietary drivers require manual installation
- Network during installation assumes internet connectivity

## Documentation

See additional documentation:
- **[docs/architecture.md](docs/architecture.md)** - System design and component details
- **[docs/windows-alternative.md](docs/windows-alternative.md)** - UX mapping guide
- **[docs/plugin-development.md](docs/plugin-development.md)** - Plugin development guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contributing guidelines
- **[README.md](README.md)** - Quick start and overview

## Community & Support

### Getting Help
- Check the documentation in `docs/` directory
- Review example plugins in `examples/plugins/`
- Open an issue on GitHub for bugs or feature requests

### Contributing
Contributions welcome! Please:
1. Read CONTRIBUTING.md
2. Fork the repository
3. Create a feature branch
4. Submit a pull request

### License
Vibe-Linux OS is released under the MIT License. See LICENSE file for full details.

## Roadmap (Future Releases)

Planned features for future releases:
- Package manager GUI (KDE)
- Plugin marketplace/discovery
- System backup and recovery tools
- Expanded Copilot AI features
- Community plugin repository
- Mobile device integration improvements
- Extended driver support

## Reporting Bugs

Found an issue? Please report it on GitHub with:
- System information (CPU, RAM, GPU)
- Steps to reproduce
- Expected vs. actual behavior
- Log output (if applicable)

## Credits

Vibe-Linux OS is built on:
- Arch Linux
- ArchISO
- archinstall
- KDE Plasma
- Hyprland
- And the broader open-source community

## Release Verification

To verify the integrity of this release:
```bash
git verify-tag v0.1.0
git log --oneline | head -n 10
```

---

**Questions?** Open an issue on GitHub or check the documentation.

**Ready to install?** See Installation & Testing section above.

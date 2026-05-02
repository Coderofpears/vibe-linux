# Vibe-Linux OS

**A modern, user-friendly Linux distribution that looks and feels like Windows or macOS, but runs on Arch Linux.**

Vibe-Linux brings the familiar comfort of Windows 11 and macOS to Linux, with the power and flexibility of Arch. Choose your desktop personality during installation and enjoy a seamless, productive experience.

## Why Vibe-Linux?

- 🎨 **Multiple UI Presets**: Default KDE, Windows 11-style, or macOS Ventura-style
- 🔧 **Familiar Tools**: If you know Windows or macOS, you already know Vibe
- ⚡ **Arch Stability**: Rolling releases with pacman package management
- 🔒 **Secure by Design**: Sandboxed plugins with explicit permissions
- 🎯 **Lightweight & Fast**: From old laptops to gaming rigs
- 🌍 **Multi-Architecture**: Works on x86_64 and ARM64 devices
- 📦 **Out-of-the-box**: Everything you need is included

## Key Features

- **Guided Installation**: Simple, visual installer with sensible defaults
- **KDE Plasma**: Beautiful, customizable desktop environment
- **Multiple Presets**: Windows 11, macOS, or default KDE Plasma
- **vibectl**: Unified command-line tool for updates, packages, and plugins
- **Plugin System**: Safe, sandboxed third-party extensions
- **Performance Profiles**: Full, Lite, Performance, Gaming, or Development modes
- **Multi-Architecture Support**: Install on Intel, AMD, Apple Silicon, or ARM servers
- **Vibe Copilot**: AI-powered assistant plugin (local-first)
- **System Monitor**: Real-time CPU, RAM, disk, and temperature monitoring
- **Quick Settings**: Fast access to WiFi, Bluetooth, brightness, and system settings
- **System Cleaner**: Analyze and optimize storage usage
- **First-Run Wizard**: Personalize your system on first login

## Installation

### Download & Install

1. **Download the latest ISO** from [Releases](https://github.com/Coderofpears/vibe-linux/releases)
2. **Choose your architecture**:
   - **x86_64** for Intel/AMD systems
   - **aarch64** for Apple Silicon or ARM devices
3. **Create a bootable USB** using Etcher, Ventoy, or `dd`
4. **Boot and follow the guided installer**

For detailed instructions, see [INSTALLATION.md](INSTALLATION.md).

### Build Your Own ISO

On an Arch Linux build host:

```bash
# Install dependencies
sudo pacman -Syu --needed archiso archinstall python python-psutil bubblewrap git rsync

# Build for x86_64
sudo ./scripts/build-iso-arch.sh x86_64

# Build for ARM64
sudo ./scripts/build-iso-arch.sh aarch64

# Or build both
sudo ./scripts/build-all-iso.sh
```

Output is written to `out/`.

### Development

For local development and testing:

```bash
# Run smoke tests
bash scripts/smoke-test.sh

# Python syntax check
python -m compileall tools installer examples/plugins

# Help commands
python tools/vibectl/vibectl.py --help
python tools/vibe-plugin-runtime/vibe-plugin-runtime.py --help
```

### Multi-Architecture Builds

Vibe-Linux supports building for multiple architectures:

#### Build for x86_64 (Intel/AMD)
```bash
sudo ./scripts/build-iso-arch.sh x86_64
```

#### Build for ARM64 (aarch64)
```bash
sudo ./scripts/build-iso-arch.sh aarch64
```

#### Build for all supported architectures
```bash
sudo ./scripts/build-all-iso.sh
# or specify architectures:
sudo ./scripts/build-all-iso.sh x86_64 aarch64
```

ISO outputs are written to `out/` with architecture-specific naming.

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

### Windows 11 UI/UX Preset

A complete KDE Plasma configuration that replicates Windows 11's look and feel is available in `configs/windows11/`. This preset is completely separate from the default KDE and Hyprland configurations.

**Features:**
- Bottom taskbar with centered task buttons
- Light color scheme with Windows 11 gray tones
- Segoe UI font for authentic Windows typography
- Windows-style keyboard shortcuts (Meta+Left/Right for snap, etc.)
- Single-click file opening
- Familiar window decorations and animations

See [configs/windows11/README.md](configs/windows11/README.md) for installation and customization instructions.

### macOS Ventura UI/UX Preset

A complete KDE Plasma configuration that replicates macOS Ventura's look and feel is available in `configs/macos/`. This preset is completely separate from the default KDE and Hyprland configurations.

**Features:**
- Top menu bar (like macOS)
- Light color scheme with macOS Ventura colors
- SF Pro Display font for authentic macOS appearance
- macOS-style keyboard shortcuts (Cmd key mapping)
- Double-click to open (macOS-style)
- Minimal window decorations with red/yellow/green buttons on left

See [configs/macos/README.md](configs/macos/README.md) for installation and customization instructions.

## System Requirements

### Minimum
- **CPU**: 64-bit x86_64 or ARM64 (aarch64)
- **RAM**: 2 GB
- **Storage**: 15 GB free
- **Display**: 1024x768 or higher

### Recommended
- **CPU**: Modern multi-core processor
- **RAM**: 8 GB or more
- **Storage**: 25+ GB (SSD preferred)
- **Display**: 1440x900 or higher

## Tools & Features

### vibectl - System Management
```bash
# Update system
vibectl update

# Install packages
vibectl install firefox

# Switch performance mode
vibectl mode lite

# Manage plugins
vibectl plugins list
vibectl plugins run vibe.copilot

# Get diagnostics
vibectl diagnostics
```

### vibe-plugin-runtime - Secure Extensions
- Manifest-driven plugin system
- Explicit permission grants
- Bubblewrap sandboxing
- Network, filesystem, and process permissions

### KDE Plasma
- Fully customizable desktop
- Multiple workspaces and activities
- Built-in widgets and applets
- Integration with system tools

## Documentation

- **[INSTALLATION.md](INSTALLATION.md)** - Detailed installation guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute
- **[docs/architecture.md](docs/architecture.md)** - System architecture
- **[docs/plugin-system.md](docs/plugin-system.md)** - Plugin development
- **[docs/security.md](docs/security.md)** - Security model
- **[docs/roadmap.md](docs/roadmap.md)** - Future plans

## Support & Community

### Getting Help
- 📖 Check [INSTALLATION.md](INSTALLATION.md) for setup issues
- 🐛 [Report bugs](https://github.com/Coderofpears/vibe-linux/issues)
- 💬 [Ask questions](https://github.com/Coderofpears/vibe-linux/discussions)
- 📝 Read the [docs/](docs/) folder

### Feedback
- Feature requests welcome via GitHub Issues
- Design feedback appreciated
- Plugin ideas and examples

## Contributing

Vibe-Linux is MIT licensed and welcomes contributions:

- Report bugs with reproduction steps
- Submit feature requests with rationale
- Submit pull requests with clear descriptions
- Help with documentation and examples
- Test on different hardware

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Competitive Analysis

### vs. Windows
- ✅ Open source and free
- ✅ Rolling updates (no forced reboots)
- ✅ Full control over your system
- ✅ Better privacy (no telemetry)
- ⚠️ Less software support for enterprise/gaming

### vs. macOS
- ✅ Works on any hardware
- ✅ Free and open source
- ✅ More customizable
- ⚠️ Steeper learning curve
- ⚠️ Some software may not be available

### vs. Other Linux Distributions
- ✅ Familiar Windows/macOS UX
- ✅ Simple installation
- ✅ Arch Linux stability (rolling base)
- ✅ Secure plugin system
- ✅ Multi-architecture support

## License

Vibe-Linux is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

Built on:
- [Arch Linux](https://archlinux.org/)
- [KDE Plasma](https://kde.org/)
- [Hyprland](https://hyprland.org/)
- [ArchISO](https://wiki.archlinux.org/title/Archiso)

## Repository

- **GitHub**: https://github.com/Coderofpears/vibe-linux
- **Releases**: https://github.com/Coderofpears/vibe-linux/releases
- **Issues**: https://github.com/Coderofpears/vibe-linux/issues

---

**Ready to experience Vibe-Linux?** [Download the latest ISO](https://github.com/Coderofpears/vibe-linux/releases) and install today!

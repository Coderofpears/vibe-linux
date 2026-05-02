# Getting Started with Vibe-Linux

Welcome! Whether you're a user, developer, or contributor, this guide will help you get up and running quickly.

---

## For End Users 👥

### Installation (5 Minutes)

**Step 1: Download**
- Visit [GitHub Releases](https://github.com/Coderofpears/vibe-linux/releases)
- Download the latest ISO for your architecture:
  - **x86_64** for Intel/AMD processors
  - **aarch64** for Apple Silicon or ARM devices

**Step 2: Create Bootable USB**
- **Windows**: Use [Rufus](https://rufus.ie/) or [Ventoy](https://www.ventoy.net/)
- **Mac**: Use [Etcher](https://www.balena.io/etcher/)
- **Linux**: Use `dd` command:
  ```bash
  sudo dd if=vibe-linux-x86_64.iso of=/dev/sdX bs=4M
  ```

**Step 3: Boot and Install**
1. Insert USB and restart your computer
2. Press `F12`, `Del`, or `Esc` to enter BIOS
3. Select the USB drive as boot device
4. Follow the visual installer (5-10 minutes)
5. Reboot and enjoy Vibe-Linux!

### First Run Setup

When you first login, a setup wizard will guide you through:
- Choosing your UI style (Windows 11, macOS, or Vibe Default)
- Selecting a performance profile (Full, Lite, Gaming, Development)
- Enabling optional features
- Configuring system settings

**Run manually anytime**:
```bash
~/.local/share/vibe-linux/first-run-wizard.sh
```

### Essential Commands

```bash
# System updates
vibectl update

# Install software
vibectl install firefox
vibectl install blender

# Show system information
vibectl diagnostics

# System monitoring
vibe-monitor

# Quick settings (WiFi, Bluetooth, brightness)
vibe-settings

# Clean up disk space
vibe-clean
```

### Learn More

- **Installation Details**: See [INSTALLATION.md](INSTALLATION.md)
- **Common Problems**: See [docs/troubleshooting.md](docs/troubleshooting.md)
- **All Features**: See [docs/features.md](docs/features.md)
- **UI Customization**: See [docs/architecture.md](docs/architecture.md)

---

## For Developers 👨‍💻

### Setting Up Development Environment

**Prerequisites**:
- Arch Linux (or another Linux distribution)
- Git
- Python 3.11+
- Bash
- Text editor or IDE

**Clone the Repository**:
```bash
git clone https://github.com/Coderofpears/vibe-linux.git
cd vibe-linux
```

**Run Setup Script**:
```bash
bash scripts/dev-setup.sh
```

This will:
- Verify Python version
- Run smoke tests
- Show project structure
- List available presets
- Display next steps

### Understanding the Codebase

**Project Structure**:
```
vibe-linux/
├── scripts/          # Build and utility scripts
├── tools/           # Core tools (vibectl, plugin runtime)
├── examples/        # Example plugins
├── configs/         # Configuration files and presets
├── docs/            # Documentation
├── installer/       # Installation system
├── archiso/         # ISO building configuration
└── packaging/       # Distribution packages
```

**Key Files**:
- `scripts/build-iso-arch.sh` - Build ISO for specific architecture
- `tools/vibectl/vibectl.py` - Main CLI tool
- `tools/vibe-plugin-runtime/vibe-plugin-runtime.py` - Plugin sandbox
- `configs/windows11/` - Windows 11 preset
- `configs/macos/` - macOS preset

### Building an ISO

**Prerequisites**:
```bash
sudo pacman -Syu --needed archiso python python-psutil bubblewrap
```

**Build**:
```bash
# Build for x86_64
sudo ./scripts/build-iso-arch.sh x86_64

# Build for aarch64
sudo ./scripts/build-iso-arch.sh aarch64

# Build both architectures
sudo ./scripts/build-all-iso.sh
```

**Output**: `~/out/vibe-linux-*.iso`

### Running Tests

```bash
# Run smoke tests (syntax, validation, compilation)
bash scripts/smoke-test.sh

# Test specific component
python3 tools/vibectl/vibectl.py --help
vibectl plugins validate examples/plugins/system-monitor
```

### Code Quality

Vibe-Linux maintains high standards:
- ✅ 100% test pass rate
- ✅ Python 3.11+ compatibility
- ✅ Type hints throughout
- ✅ Comprehensive docstrings
- ✅ Security scanning
- ✅ Multi-architecture support

**Before submitting code**:
1. Run `bash scripts/smoke-test.sh`
2. Test on multiple systems if possible
3. Follow code style (Python: PEP 8, Shell: Google style)
4. Document your changes
5. Update relevant docs

---

## For Plugin Developers 🔌

### Quick Start: Build Your First Plugin

**Step 1: Create Plugin Directory**
```bash
mkdir my-first-plugin && cd my-first-plugin
```

**Step 2: Create manifest.json**
```json
{
  "id": "vibe.my-first-plugin",
  "name": "My First Plugin",
  "version": "1.0.0",
  "description": "My awesome plugin",
  "runtime": "python3.11",
  "entry": "plugin.py",
  "permissions": []
}
```

**Step 3: Create plugin.py**
```python
#!/usr/bin/env python3
"""My first plugin"""

def main():
    print("Hello from my plugin!")

if __name__ == "__main__":
    main()
```

**Step 4: Test**
```bash
vibectl plugins validate .
vibectl plugins run vibe.my-first-plugin
```

### Example Plugins

We provide complete examples:
- **system-monitor**: Real-time resource monitoring (Python)
- **quick-settings**: System controls - WiFi, Bluetooth, brightness (Shell)
- **system-cleaner**: Storage analysis (Python)
- **package-search**: Package repository search
- **system-info**: Detailed system information
- **vibe-copilot**: AI-powered assistant

Each example includes:
- Complete manifest.json
- Working implementation
- Permission examples
- Usage documentation

**Location**: `examples/plugins/`

### Publishing Your Plugin

1. **Create GitHub Repository**
   - Name: `vibe-plugin-<name>`
   - Include manifest.json, code, README

2. **Create Release**
   - Tag version (v1.0.0)
   - Attach plugin archive
   - Write description

3. **Share with Community**
   - Post in [Discussions](https://github.com/Coderofpears/vibe-linux/discussions)
   - Request to be listed in registry (coming soon)

**Learn More**: See [docs/plugin-development.md](docs/plugin-development.md)

---

## For Contributors 🤝

### Getting Started

1. **Fork & Clone**
   ```bash
   git clone https://github.com/YOUR-USERNAME/vibe-linux.git
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/my-feature
   ```

3. **Make Changes**
   - Follow [CONTRIBUTING.md](CONTRIBUTING.md)
   - Run smoke tests
   - Update documentation

4. **Commit & Push**
   ```bash
   git add .
   git commit -m "Brief description of changes"
   git push origin feature/my-feature
   ```

5. **Create Pull Request**
   - Describe changes
   - Reference any related issues
   - Wait for review

### Types of Contributions

**Code**:
- Bug fixes
- New features
- Performance improvements
- Plugin development

**Documentation**:
- Fix typos
- Improve clarity
- Add examples
- Create guides

**Testing**:
- Report bugs
- Test on different hardware
- Verify features
- Suggest improvements

**Advocacy**:
- Share with friends
- Write reviews
- Create tutorials
- Answer questions

### Guidelines

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development rules
- Code standards
- Testing requirements
- Package policy
- Review process

---

## Roadmap & Vision

### Current Status: v0.2.0 (Production Ready)
- Core system complete
- Multiple UI presets
- Plugin ecosystem
- Professional documentation
- GitHub Actions CI/CD

### Next: v0.3.0 (Q3 2026)
- Internationalization (i18n)
- Plugin marketplace
- Advanced installer options
- Additional presets
- Performance optimizations

### Future: v1.0.0 (Q1 2027)
- Enterprise features
- Wide distribution support
- Mature ecosystem
- Commercial support options

See [docs/roadmap.md](docs/roadmap.md) for detailed plans.

---

## Getting Help

### Self-Service
- **Installation**: [INSTALLATION.md](INSTALLATION.md)
- **Problems**: [docs/troubleshooting.md](docs/troubleshooting.md)
- **Features**: [docs/features.md](docs/features.md)
- **Development**: [docs/plugin-development.md](docs/plugin-development.md)
- **Architecture**: [docs/architecture.md](docs/architecture.md)
- **Security**: [docs/security.md](docs/security.md)

### Community
- **Issues**: [GitHub Issues](https://github.com/Coderofpears/vibe-linux/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Coderofpears/vibe-linux/discussions)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

### Documentation
- See all docs: `docs/` directory
- All files are in Markdown
- Examples provided throughout
- Well-organized and searchable

---

## Project Stats

- **Languages**: Python, Bash, JSON, Markdown
- **Architecture Support**: x86_64, aarch64
- **UI Presets**: 3 (Vibe, Windows 11, macOS)
- **Performance Modes**: 5 (Full, Lite, Performance, Gaming, Development)
- **Example Plugins**: 6+ (with 3 production-ready)
- **Test Coverage**: 100% smoke tests passing
- **Documentation**: 8000+ lines across 10+ files
- **License**: MIT (Free & Open)

---

## Next Steps

**Users**: Download from [Releases](https://github.com/Coderofpears/vibe-linux/releases)

**Developers**: Clone and run `bash scripts/dev-setup.sh`

**Contributors**: Fork and check [CONTRIBUTING.md](CONTRIBUTING.md)

**Plugin Developers**: See [docs/plugin-development.md](docs/plugin-development.md)

---

## Questions?

- 📖 Read the [docs](docs/)
- 🐛 Check [existing issues](https://github.com/Coderofpears/vibe-linux/issues)
- 💬 Start a [discussion](https://github.com/Coderofpears/vibe-linux/discussions)
- ⭐ Star the project if you like it!

---

**Welcome to Vibe-Linux! Happy coding! 🚀**

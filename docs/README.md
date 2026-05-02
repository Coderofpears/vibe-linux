# Documentation Index

Welcome to the Vibe-Linux documentation! This index will help you find what you're looking for.

---

## Quick Links

**New to Vibe-Linux?** → Start with [GETTING_STARTED.md](../GETTING_STARTED.md)

**Want to install?** → Go to [INSTALLATION.md](../INSTALLATION.md)

**Contributing?** → Read [CONTRIBUTING.md](../CONTRIBUTING.md)

**Building plugins?** → See [plugin-development.md](plugin-development.md)

---

## Documentation by Role

### 👥 **End Users**

| Document | Purpose |
|----------|---------|
| [GETTING_STARTED.md](../GETTING_STARTED.md) | Installation and first-run setup |
| [INSTALLATION.md](../INSTALLATION.md) | Detailed installation guide with troubleshooting |
| [troubleshooting.md](troubleshooting.md) | Solve common problems |
| [features.md](features.md) | Complete feature overview |
| [performance-profiles.md](performance-profiles.md) | Understanding Full, Lite, Gaming, Development modes |

### 👨‍💻 **Developers**

| Document | Purpose |
|----------|---------|
| [GETTING_STARTED.md](../GETTING_STARTED.md) | Setup dev environment |
| [architecture.md](architecture.md) | System design and structure |
| [plugin-development.md](plugin-development.md) | Build custom plugins |
| [plugin-system.md](plugin-system.md) | How the plugin system works |
| [security.md](security.md) | Security model and sandbox |

### 🤝 **Contributors**

| Document | Purpose |
|----------|---------|
| [CONTRIBUTING.md](../CONTRIBUTING.md) | How to contribute |
| [GETTING_STARTED.md](../GETTING_STARTED.md) | Developer setup |
| [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) | Release procedures |

### 🔌 **Plugin Developers**

| Document | Purpose |
|----------|---------|
| [plugin-development.md](plugin-development.md) | Complete SDK guide |
| [plugin-system.md](plugin-system.md) | Architecture and design |
| [security.md](security.md) | Sandbox and permissions |
| [../examples/plugins/](../examples/plugins/) | Working code examples |

---

## Documentation by Topic

### Getting Started
- [GETTING_STARTED.md](../GETTING_STARTED.md) - Overview for all roles
- [INSTALLATION.md](../INSTALLATION.md) - Installation walkthrough

### System Documentation
- [architecture.md](architecture.md) - System design and components
- [performance-profiles.md](performance-profiles.md) - Performance modes explained
- [security.md](security.md) - Security model and privacy

### Plugin Development
- [plugin-development.md](plugin-development.md) - Complete SDK (600+ lines)
- [plugin-system.md](plugin-system.md) - Plugin architecture
- [../examples/plugins/](../examples/plugins/) - Example plugins (3 complete)

### Operation & Support
- [troubleshooting.md](troubleshooting.md) - Problem solving guide
- [RELEASE_NOTES.md](../RELEASE_NOTES.md) - Version history
- [windows-alternative.md](windows-alternative.md) - Windows comparison

### Project Management
- [roadmap.md](roadmap.md) - Future direction
- [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) - Release procedures
- [../CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines

### Product Information
- [../PRODUCT_SPEC.md](../PRODUCT_SPEC.md) - Product specification
- [../README.md](../README.md) - Project overview
- [../GETTING_STARTED.md](../GETTING_STARTED.md) - Quick start

---

## All Documents

### Root Level
```
/
├── README.md                    - Project overview & marketing
├── INSTALLATION.md              - Installation guide
├── GETTING_STARTED.md           - Getting started guide (NEW)
├── CONTRIBUTING.md              - Contribution guidelines
├── PRODUCT_SPEC.md              - Product specification (NEW)
├── CODE_OF_CONDUCT.md           - Community standards
├── LICENSE                      - MIT License
├── NOTICE                       - Attribution
└── RELEASE_NOTES.md             - Changelog
```

### docs/ Directory
```
docs/
├── README.md (this file)         - Documentation index
├── architecture.md              - System design
├── plugin-development.md         - SDK guide (NEW - 600+ lines)
├── plugin-system.md             - Plugin architecture
├── security.md                  - Security model
├── performance-profiles.md      - Mode descriptions
├── troubleshooting.md           - Support guide (NEW)
├── windows-alternative.md       - Feature comparison
├── roadmap.md                   - Future plans
└── RELEASE_CHECKLIST.md         - Release procedures
```

---

## Finding Information

### By Question

**"How do I install Vibe-Linux?"**
→ [INSTALLATION.md](../INSTALLATION.md) or [GETTING_STARTED.md](../GETTING_STARTED.md)

**"What are the system requirements?"**
→ [INSTALLATION.md](../INSTALLATION.md#requirements) or [features.md](features.md)

**"How do I switch UI themes?"**
→ [features.md](features.md#ui-presets) or [architecture.md](architecture.md)

**"What should I do if X doesn't work?"**
→ [troubleshooting.md](troubleshooting.md)

**"How do I create a plugin?"**
→ [plugin-development.md](plugin-development.md) + [../examples/plugins/](../examples/plugins/)

**"Is this really free/open source?"**
→ [PRODUCT_SPEC.md](../PRODUCT_SPEC.md#business-model) and [../LICENSE](../LICENSE)

**"How can I contribute?"**
→ [CONTRIBUTING.md](../CONTRIBUTING.md)

**"What's the security model?"**
→ [security.md](security.md)

**"How do I optimize performance?"**
→ [performance-profiles.md](performance-profiles.md)

### By Document Length

**Quick Read (5 min)**
- [PRODUCT_SPEC.md](../PRODUCT_SPEC.md) Executive Summary
- [features.md](features.md) Overview

**Medium Read (15 min)**
- [INSTALLATION.md](../INSTALLATION.md)
- [architecture.md](architecture.md)
- [troubleshooting.md](troubleshooting.md)

**Deep Dive (30+ min)**
- [plugin-development.md](plugin-development.md) Complete SDK
- [security.md](security.md) Full security model
- [CONTRIBUTING.md](../CONTRIBUTING.md) Development guide

---

## Documentation Quality

All Vibe-Linux documentation features:

✅ **Complete** - Every topic covered thoroughly
✅ **Accurate** - Updated with latest code
✅ **Examples** - Real, working code snippets
✅ **Professional** - Business-ready content
✅ **Searchable** - Well-organized and indexed
✅ **Multilingual** - Ready for translation
✅ **Accessible** - Clear language, no jargon

---

## Contributing to Documentation

Found a typo? Want to improve something? Excellent!

1. **Edit in GitHub** (for small changes):
   - Click "Edit" button on any markdown file
   - Make your changes
   - Submit pull request

2. **Clone locally** (for major changes):
   ```bash
   git clone https://github.com/Coderofpears/vibe-linux.git
   cd vibe-linux
   # Edit files
   git add .
   git commit -m "Improve documentation"
   git push
   ```

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

## Documentation Roadmap

### Currently Available ✅
- Installation guide
- Developer setup
- Plugin development SDK
- System architecture
- Security model
- Performance profiles
- Troubleshooting guide
- Product specification

### Planned 📋
- Video tutorials
- Internationalization (i18n)
- Interactive documentation
- API documentation (Sphinx)
- FAQ based on user questions

---

## Getting Help

### Stuck?
1. **Search docs** - Use browser Ctrl+F to search
2. **Check FAQ** - Most common questions answered
3. **Search issues** - Others might have solved it
4. **Ask in discussions** - Community can help
5. **File an issue** - For bugs and missing info

### Links
- [GitHub Issues](https://github.com/Coderofpears/vibe-linux/issues) - Bug reports
- [GitHub Discussions](https://github.com/Coderofpears/vibe-linux/discussions) - Q&A
- [CONTRIBUTING.md](../CONTRIBUTING.md) - How to help

---

## Quick Navigation

**For Installation**: [INSTALLATION.md](../INSTALLATION.md)

**For Development**: [GETTING_STARTED.md](../GETTING_STARTED.md) → [architecture.md](architecture.md)

**For Plugins**: [plugin-development.md](plugin-development.md) + [../examples/plugins/](../examples/plugins/)

**For Help**: [troubleshooting.md](troubleshooting.md) → [GitHub Discussions](https://github.com/Coderofpears/vibe-linux/discussions)

**For Contributing**: [CONTRIBUTING.md](../CONTRIBUTING.md) → [roadmap.md](roadmap.md)

---

**Last Updated**: May 2, 2026

**All documentation is open source** - Improve it at [GitHub](https://github.com/Coderofpears/vibe-linux)!

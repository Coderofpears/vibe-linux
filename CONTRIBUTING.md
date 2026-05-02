# Contributing to Vibe-Linux

Thank you for your interest in contributing to Vibe-Linux! We welcome contributions of all types.

## Code of Conduct

Please review our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## Development Rules

- Keep default packages open source unless a file clearly marks an optional proprietary path.
- Prefer Python for system tools and shell only for low-level ISO or chroot work.
- Route privileged actions through `vibectl`.
- Route plugins through `vibe-plugin-runtime`.
- Update docs when changing installer, security, or plugin behavior.

## How to Contribute

### 1. Report Bugs

Found a bug? Create an issue with:
- **Title**: Clear, concise description
- **Description**: What happened and what should happen
- **Steps to reproduce**: Exact steps to trigger the bug
- **Environment**: OS, architecture, KDE version, etc.
- **Diagnostic output**: Run `vibectl diagnostics`

### 2. Suggest Features

Have an idea? Create an issue with:
- **Title**: Feature name
- **Description**: What problem does it solve?
- **Rationale**: Why is this important?
- **Examples**: Similar features in other projects

### 3. Submit Code

#### Fork & Clone
```bash
git clone https://github.com/yourusername/vibe-linux.git
cd vibe-linux
git checkout -b feature/your-feature-name
```

#### Make Changes
```bash
# Create your changes
git add .
git commit -m "Descriptive commit message"
git push origin feature/your-feature-name
```

#### Create Pull Request
1. Push to your fork
2. Click "Compare & pull request"
3. Fill in PR template
4. Reference related issues: "Fixes #123"

## Code Standards

### Python (3.11+)
- Follow PEP 8 style guide
- Use type hints
- Include docstrings
- Test with: `python -m compileall`

```python
def example_function(arg1: str, arg2: int) -> bool:
    """Brief description of function."""
    return True
```

### Shell Scripts
```bash
#!/usr/bin/env bash
set -euo pipefail

function do_something() {
    local param="$1"
    echo "Doing: $param"
}
```

### JSON
- Use 2-space indentation
- Sort keys alphabetically
- Validate with: `python -m json.tool`

## Local Checks

Before submitting code, run:

```bash
# Smoke tests
bash scripts/smoke-test.sh

# Python syntax
python3 -m compileall tools installer examples/plugins

# JSON validation
python3 -m json.tool configs/modes/*.json

# Shell syntax
bash -n scripts/*.sh
```

## Testing

```bash
# Test plugin validation
python3 tools/vibe-plugin-runtime/vibe-plugin-runtime.py validate examples/plugins/system-info
python3 tools/vibe-plugin-runtime/vibe-plugin-runtime.py validate examples/plugins/vibe-copilot

# Test vibectl help
python3 tools/vibectl/vibectl.py --help
```

## Package Policy

Default ISO and full-install packages should come from official Arch repositories. AUR and proprietary packages may be documented as optional add-ons, but should not be required for the base system.

## Areas We Need Help With

### High Priority
- Installer improvements and localization
- Plugin ecosystem expansion
- Documentation and tutorials
- ARM64 hardware testing

### Medium Priority
- Performance optimizations
- UI/UX refinements
- Additional presets
- Build system improvements

### Nice to Have
- Example plugins
- Desktop theming
- Community feedback portal
- Upstream contributions

## Questions?

- Check [docs/](docs/) directory
- Search existing issues
- Create a discussion
- Read [INSTALLATION.md](INSTALLATION.md)

Thank you for making Vibe-Linux better! 🎉


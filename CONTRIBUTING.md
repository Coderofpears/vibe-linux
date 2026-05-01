# Contributing

Vibe-Linux OS is MIT licensed and OSS-first.

## Development Rules

- Keep default packages open source unless a file clearly marks an optional proprietary path.
- Prefer Python for system tools and shell only for low-level ISO or chroot work.
- Route privileged actions through `vibectl`.
- Route plugins through `vibe-plugin-runtime`.
- Update docs when changing installer, security, or plugin behavior.

## Local Checks

```bash
python3 -m compileall tools installer examples/plugins
python3 tools/vibectl/vibectl.py --help
python3 tools/vibe-plugin-runtime/vibe-plugin-runtime.py validate examples/plugins/system-info
python3 tools/vibe-plugin-runtime/vibe-plugin-runtime.py validate examples/plugins/vibe-copilot
```

## Package Policy

Default ISO and full-install packages should come from official Arch repositories. AUR and proprietary packages may be documented as optional add-ons, but should not be required for the base system.


# Security Model

## Privilege Boundary

Vibe-Linux OS treats package installation, service control, and filesystem writes outside user-owned plugin storage as privileged actions.

Approved entry points:

- `vibectl` for package and mode changes.
- `vibe-plugin-runtime` for plugin execution.
- systemd units owned by Vibe packages.

## Plugin Rules

1. No plugin receives unrestricted root access by default.
2. Plugins declare permissions before installation.
3. The runtime validates manifests before execution.
4. Package operations must go through a pacman wrapper, never direct `pacman` calls from plugins.
5. Privileged operations are logged.
6. First-party elevated plugins must be signed in a later milestone.

## Current Foundation Limitations

This scaffold provides local manifest validation and bubblewrap sandboxing. Production hardening should add:

- package signing for plugin bundles,
- a repository trust database,
- reproducible builds,
- PolicyKit integration for graphical prompts,
- SELinux or Landlock profile experiments,
- systemd transient unit execution for privileged workflows.

## OSS Policy

The default ISO and installer profiles are open-source first. For example, NVIDIA hardware uses Nouveau/Mesa packages by default. Proprietary GPU drivers and proprietary assistant backends may be documented as optional user choices, but they are not part of the base profile.

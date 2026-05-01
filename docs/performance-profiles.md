# Performance Profiles

Vibe-Linux OS ships two primary mode profiles.

## Full Mode

Target: 16GB+ RAM systems.

- KDE Plasma effects enabled.
- Baloo file indexing enabled.
- Developer services available.
- Plugin runtime and plugin update timers enabled.
- Heavier default app set.

## Lite Mode

Target: 8GB RAM or constrained systems.

- KDE animation speed reduced.
- Baloo disabled.
- Optional background services disabled.
- Lightweight app defaults preferred.
- Plugin services run on demand.

## Mode Switching

The user-facing command is:

```bash
vibectl mode full
vibectl mode lite
vibectl mode performance
```

`performance` is an alias for Full Mode with power settings adjusted toward responsiveness.


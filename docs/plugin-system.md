# Vibe Plugin System

The Vibe Plugin System replaces arbitrary install scripts with manifest-based plugins that run through a controlled runtime.

## Manifest

Each plugin must include `manifest.json`:

```json
{
  "id": "dev.vibe.system-info",
  "name": "System Info",
  "version": "1.0.0",
  "entry": "plugin.py",
  "runtime": "python",
  "permissions": {
    "filesystem": [{"path": "/proc", "access": "read"}],
    "network": false,
    "packages": false,
    "process": false
  }
}
```

## Permission Model

- `filesystem`: explicit read or write paths only.
- `network`: opt-in network namespace sharing.
- `packages`: package operations through `vibectl` only.
- `process`: opt-in access to host process information.
- `system`: reserved for first-party plugins and requires policy approval.

## Runtime Enforcement

On Linux, `vibe-plugin-runtime` requires `bubblewrap` and creates a minimal sandbox:

- read-only system paths,
- a private `/tmp`,
- a minimal `/dev`,
- plugin directory mounted read-only,
- explicitly declared filesystem mounts,
- isolated network unless `network: true`.

All plugin executions are logged as JSON lines under `/var/log/vibe/plugins.log` when writable, otherwise under the user's state directory.

## Vibe Copilot Plugin

`examples/plugins/vibe-copilot` is the default assistant example. It is local-first and rule-based so the OSS base does not depend on a proprietary cloud service. Future cloud or local LLM backends should be optional plugins with explicit `network` permission.

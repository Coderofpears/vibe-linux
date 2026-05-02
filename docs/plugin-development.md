# Vibe-Linux Plugin Development Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Plugin Structure](#plugin-structure)
3. [Manifest Format](#manifest-format)
4. [Runtime & Permissions](#runtime--permissions)
5. [Example Plugins](#example-plugins)
6. [Testing & Debugging](#testing--debugging)
7. [Publishing](#publishing)

---

## Getting Started

### Prerequisites
- Python 3.11+ (for Python plugins)
- Bash/Shell knowledge (for shell plugins)
- Basic understanding of JSON
- A text editor or IDE

### Quick Start
1. Create a plugin directory: `mkdir my-plugin && cd my-plugin`
2. Create `manifest.json` with plugin metadata
3. Create plugin implementation (Python or shell)
4. Test with `vibectl plugins run my-plugin`

### Project Structure
```
my-plugin/
├── manifest.json              # Plugin metadata
├── plugin.py                 # Main implementation (Python)
└── README.md                 # Documentation (optional)
```

---

## Plugin Structure

### manifest.json

**Purpose**: Metadata that describes your plugin to Vibe-Linux

**Location**: Root directory of plugin

**Required Fields**:
```json
{
  "id": "vibe.my-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "description": "What this plugin does",
  "runtime": "python3.11",
  "entry": "plugin.py"
}
```

**Optional Fields**:
```json
{
  "author": "Your Name",
  "license": "MIT",
  "repo": "https://github.com/yourname/vibe-my-plugin",
  "icon": "base64-encoded-png-here",
  "category": "utility",
  "permissions": ["read:/home", "write:/tmp"],
  "tags": ["system", "monitoring"],
  "dependencies": ["psutil", "requests"]
}
```

### Implementation File

**Python Plugin Example** (plugin.py):
```python
#!/usr/bin/env python3
"""
My Plugin
A template plugin demonstrating best practices.
"""

def main():
    """Main entry point - called by vibectl"""
    print("Hello from my plugin!")

def read_config(key: str) -> str:
    """Read configuration from system"""
    # Implementation here
    pass

def setup():
    """Run once on first installation"""
    print("Plugin installed successfully")

if __name__ == "__main__":
    main()
```

**Shell Plugin Example** (plugin.sh):
```bash
#!/usr/bin/env bash
# My Plugin
# A template plugin for shell scripts

main() {
    echo "Hello from my shell plugin!"
}

read_config() {
    local key="$1"
    # Implementation here
}

main "$@"
```

---

## Manifest Format

### Complete Reference

```json
{
  // Required: Unique plugin identifier
  "id": "vibe.namespace.plugin-name",
  
  // Required: Human-readable name
  "name": "Plugin Display Name",
  
  // Required: Semantic version
  "version": "1.2.3",
  
  // Required: Description shown in plugin store
  "description": "What this plugin does in one sentence",
  
  // Required: Runtime environment
  "runtime": "python3.11",
  
  // Required: Entry point file
  "entry": "plugin.py",
  
  // Optional: Plugin author
  "author": "Your Name <email@example.com>",
  
  // Optional: License identifier
  "license": "MIT",
  
  // Optional: Source code repository
  "repo": "https://github.com/yourname/vibe-my-plugin",
  
  // Optional: Base64-encoded PNG icon (256x256)
  "icon": "iVBORw0KGgoAAAANSUhEUgAAA...",
  
  // Optional: Plugin category
  "category": "utility",
  
  // Optional: Permissions required by plugin
  "permissions": [
    "read:/home",
    "write:/tmp",
    "network",
    "exec"
  ],
  
  // Optional: Search tags
  "tags": ["system", "monitoring"],
  
  // Optional: Python packages to install
  "dependencies": ["psutil", "requests"],
  
  // Optional: Supported platforms
  "platforms": ["linux"],
  
  // Optional: Minimum supported version
  "min_vibe_version": "0.2.0"
}
```

### Permission Types

Permissions control what resources your plugin can access:

| Permission | Allows |
|-----------|---------|
| `read:PATH` | Read files in PATH (e.g., `read:/proc`) |
| `write:PATH` | Write to PATH |
| `exec` | Run external commands |
| `network` | Internet access |
| `audio` | Audio device access |
| `video` | Camera access |
| `usb` | USB device access |
| `dbus` | D-Bus communication |

**Permission Inheritance**:
- `/home` includes all user subdirectories
- `/sys` includes all system interfaces
- `read:/home` does NOT include write

---

## Runtime & Permissions

### Python Runtime

**Best for**: Data processing, system monitoring, complex logic

**Advantages**:
- Rich standard library
- Easy package installation via pip
- Great for prototyping

**Entry Point**:
```python
def main():
    # Your plugin logic
    pass

if __name__ == "__main__":
    main()
```

**Accessing Config**:
```python
import os
config = os.environ.get("VIBE_CONFIG_PATH", "$HOME/.config/vibe")
```

### Shell Runtime

**Best for**: System commands, quick scripts, minimal dependencies

**Advantages**:
- No external dependencies
- Direct system command access
- Perfect for admin tasks

**Entry Point**:
```bash
#!/usr/bin/env bash
main() {
    # Your plugin logic
}
main "$@"
```

### Permission Enforcement

Plugins run in a sandbox with limited permissions:

1. **Declaration**: List permissions in `manifest.json`
2. **Isolation**: Bubblewrap sandbox enforces restrictions
3. **Prompts**: User confirms unusual permissions
4. **Audit**: All permission access logged

---

## Example Plugins

### 1. System Monitor (Python)

**Purpose**: Display system resource usage

**manifest.json**:
```json
{
  "id": "vibe.system-monitor",
  "name": "System Monitor",
  "version": "1.0.0",
  "description": "Real-time CPU, RAM, disk monitoring",
  "runtime": "python3.11",
  "entry": "monitor.py",
  "permissions": ["read:/proc", "read:/sys"],
  "category": "system",
  "dependencies": ["psutil"]
}
```

**monitor.py**:
```python
#!/usr/bin/env python3
import psutil
import json

def get_cpu_usage() -> float:
    """Get CPU usage percentage"""
    return psutil.cpu_percent(interval=1)

def get_memory_usage() -> dict:
    """Get memory statistics"""
    mem = psutil.virtual_memory()
    return {
        "total_mb": mem.total // (1024 * 1024),
        "used_mb": mem.used // (1024 * 1024),
        "percent": mem.percent
    }

def get_disk_usage(path: str = "/") -> dict:
    """Get disk usage for path"""
    disk = psutil.disk_usage(path)
    return {
        "total_gb": disk.total // (1024**3),
        "used_gb": disk.used // (1024**3),
        "free_gb": disk.free // (1024**3),
        "percent": disk.percent
    }

def main():
    """Display system stats"""
    print("CPU:", get_cpu_usage(), "%")
    print("Memory:", json.dumps(get_memory_usage()))
    print("Disk:", json.dumps(get_disk_usage()))

if __name__ == "__main__":
    main()
```

### 2. Quick Settings (Shell)

**Purpose**: System controls (WiFi, Bluetooth, brightness)

**manifest.json**:
```json
{
  "id": "vibe.quick-settings",
  "name": "Quick Settings",
  "version": "1.0.0",
  "description": "WiFi, Bluetooth, brightness controls",
  "runtime": "shell",
  "entry": "settings.sh",
  "permissions": ["write:/sys/class/backlight", "exec"],
  "category": "system"
}
```

**settings.sh**:
```bash
#!/usr/bin/env bash

toggle_wifi() {
    rfkill toggle wlan0
    echo "WiFi toggled"
}

toggle_bluetooth() {
    rfkill toggle bluetooth
    echo "Bluetooth toggled"
}

set_brightness() {
    local percent=$1
    local max=$(cat /sys/class/backlight/*/max_brightness)
    local value=$((max * percent / 100))
    echo "$value" > /sys/class/backlight/*/brightness
    echo "Brightness set to $percent%"
}

main() {
    case "$1" in
        wifi) toggle_wifi ;;
        bt) toggle_bluetooth ;;
        brightness) set_brightness "$2" ;;
        *) echo "Usage: $0 [wifi|bt|brightness <percent>]" ;;
    esac
}

main "$@"
```

### 3. Analysis Plugin (Python)

**Purpose**: Analyze system without making changes

**manifest.json**:
```json
{
  "id": "vibe.system-analyzer",
  "name": "System Analyzer",
  "version": "1.0.0",
  "description": "Deep system analysis and reporting",
  "runtime": "python3.11",
  "entry": "analyzer.py",
  "permissions": ["read:/", "read:/proc", "read:/sys"],
  "category": "diagnostic"
}
```

**analyzer.py**:
```python
#!/usr/bin/env python3
import os
import subprocess

def analyze_performance():
    """Analyze system performance"""
    try:
        load = os.getloadavg()
        return {"load": load}
    except Exception as e:
        return {"error": str(e)}

def analyze_drivers():
    """Check loaded drivers"""
    try:
        result = subprocess.run(
            ["lspci"],
            capture_output=True,
            text=True
        )
        return {"devices": len(result.stdout.split('\n'))}
    except Exception as e:
        return {"error": str(e)}

def main():
    print("Performance:", analyze_performance())
    print("Devices:", analyze_drivers())

if __name__ == "__main__":
    main()
```

---

## Testing & Debugging

### Local Testing

**Validate Plugin**:
```bash
vibectl plugins validate /path/to/plugin
```

**Run Plugin**:
```bash
vibectl plugins run vibe.my-plugin
```

**Debug Output**:
```bash
VIBE_DEBUG=1 vibectl plugins run vibe.my-plugin
```

### Testing Permissions

Create test plugin that requires different permissions:

```python
import os

def main():
    # Test read permission
    try:
        with open("/proc/cpuinfo") as f:
            print("Read /proc: OK")
    except PermissionError:
        print("Read /proc: DENIED")
    
    # Test write permission
    try:
        with open("/tmp/test", "w") as f:
            f.write("test")
        print("Write /tmp: OK")
    except PermissionError:
        print("Write /tmp: DENIED")

if __name__ == "__main__":
    main()
```

### Common Issues

**ImportError**: Install missing dependencies
```bash
pip install missing-package
```

**Permission Denied**: Add permission to manifest
```json
{
  "permissions": ["read:/proc", "read:/sys"]
}
```

**File Not Found**: Check entry point path
```json
{
  "entry": "correct-filename.py"
}
```

---

## Publishing

### Before Publishing

- [x] Test on multiple systems
- [x] Validate manifest.json
- [x] Document all permissions
- [x] Create comprehensive README
- [x] Include example usage
- [x] License your plugin (MIT, GPL, etc.)

### Publishing Steps

1. **Create GitHub Repository**
   - Name format: `vibe-plugin-<name>`
   - Include manifest.json and code

2. **Add to GitHub Releases**
   - Create versioned releases
   - Include plugin archive

3. **Register in Vibe Plugin Registry** (future)
   - Submit plugin metadata
   - Community review
   - Listed in plugin store

4. **Promote**
   - Share on Vibe community
   - Document on GitHub
   - Get feedback and iterate

### README Template

```markdown
# Vibe Plugin: My Plugin

Simple description of what this plugin does.

## Installation

```bash
vibectl plugins install <plugin-name>
```

## Usage

```bash
vibectl plugins run vibe.my-plugin <args>
```

## Permissions

This plugin requires:
- `read:/home` - Access to home directory
- `exec` - Execute system commands

## Development

See [Plugin Development Guide](../PLUGIN_DEVELOPMENT.md)

## License

MIT License
```

---

## API Reference

### Standard Input/Output

Plugins receive input via command-line arguments and environment variables:

```python
import sys
import os

plugin_id = os.environ.get("VIBE_PLUGIN_ID")
config_path = os.environ.get("VIBE_CONFIG_PATH")
args = sys.argv[1:]
```

### Return Values

- `Exit code 0`: Success
- `Exit code 1`: Error
- `stdout`: Normal output
- `stderr`: Error messages

### JSON Output

For structured data, output JSON:

```python
import json

result = {
    "status": "success",
    "data": {...}
}
print(json.dumps(result))
```

---

## Best Practices

✅ **Do**:
- Validate user input
- Handle errors gracefully
- Log important events
- Document your plugin
- Keep plugins focused
- Test on multiple systems

❌ **Don't**:
- Request excessive permissions
- Run in infinite loops
- Ignore errors
- Make breaking changes
- Store sensitive data
- Run background services

---

## Getting Help

- **Documentation**: [docs/plugin-system.md](../docs/plugin-system.md)
- **Examples**: [examples/plugins/](../examples/plugins/)
- **Issues**: [GitHub Issues](https://github.com/Coderofpears/vibe-linux/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Coderofpears/vibe-linux/discussions)

---

**Ready to build? Start with our [example plugins](../examples/plugins/) and create something amazing!** 🚀

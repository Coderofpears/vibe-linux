# macOS Ventura UI/UX Preset for Vibe-Linux

A comprehensive KDE Plasma configuration that replicates the look and feel of macOS Ventura.

## Features

### Visual Design
- **Light theme** with macOS Ventura color palette
- **Top menu bar** positioned at the top (like macOS)
- **Minimal window decorations** with red/yellow/green buttons on the left (macOS-style)
- **Breeze Light** color scheme for a clean, modern appearance
- **SF Pro Display font** for authentic macOS typography

### User Experience
- **Double-click** file/folder opening (macOS-style)
- **macOS-style keyboard shortcuts**:
  - `Cmd + Left/Right` - Snap windows to sides (⌘ = Ctrl in this mapping)
  - `Cmd + Up` - Show desktop
  - `Cmd + Tab` - Application switcher
  - `Cmd + Space` - Spotlight-like search (File manager)
  - `Cmd + Shift + 3` - Screenshot
  - `Cmd + H` - Hide window
  - `Cmd + Q` - Activity switcher
- **Menu bar features**:
  - Application menu on the left
  - System tray on the right
  - Digital clock on the far right
- **Smooth animations** with shorter durations (macOS-style responsiveness)
- **No electric borders** (unlike Windows)
- **Focus on click** (macOS standard)

### System Components
- **SDDM Login Screen** - Configured with Breeze Light theme
- **KDE Window Manager (kwin)** - Optimized for macOS-style behavior
- **Plasma Shell** - Top panel configuration
- **Global Shortcuts** - macOS-style key bindings

## Installation

### Option 1: Apply During Installation
The macOS preset is available as a selectable option during the Vibe-Linux installation process.

### Option 2: Apply to Existing System
If you already have Vibe-Linux installed:

```bash
# Copy the configuration files to your KDE config directory
cp -r configs/macos/* ~/.config/

# Restart KDE Plasma (or log out and log back in)
kquitapp5 kstart5 plasmashell &
```

### Option 3: Use vibectl
If `vibectl` supports preset management:

```bash
vibectl preset apply macos
```

## Configuration Files

The preset consists of the following KDE configuration files:

- **kdeglobals** - Global KDE settings (colors, fonts, appearance)
- **plasmashellrc** - Plasma shell configuration (top panel layout, widgets)
- **kwinrc** - KDE window manager settings (effects, decorations, shortcuts)
- **kglobalshortcutsrc** - Global keyboard shortcuts
- **kscreenlockerrc** - Screen locker settings
- **sddm.conf** - SDDM login screen configuration

## Customization

To customize the macOS preset:

1. Edit the configuration files in `configs/macos/`
2. For color customization, modify the `[Colors:*]` sections in `kdeglobals`
3. For menu bar layout, edit the `[Containments][1][General]` section in `plasmashellrc`
4. For window behavior, modify the `[Windows]` section in `kwinrc`

## Key Differences from macOS

- Uses Cmd (Ctrl) mapping for keyboard shortcuts due to Linux conventions
- Uses KDE Plasma instead of macOS Aqua UI framework
- File manager uses Dolphin instead of Finder
- System settings use KDE System Settings instead of macOS System Preferences
- Virtual spaces use KDE Activities terminology
- No Dock (equivalent is taskbar in panel)

## Reverting to Default

To revert to the default Vibe-Linux KDE configuration:

```bash
# Remove the macOS preset
rm ~/.config/kdeglobals ~/.config/plasmashellrc ~/.config/kwinrc ~/.config/kglobalshortcutsrc

# Restart Plasma to load default settings
kquitapp5 kstart5 plasmashell &
```

Or use your backup/system restore options.

## Compatibility

- **KDE Plasma**: 5.24+
- **Arch Linux** and derivatives
- **CPU**: x86_64 and ARM64 (aarch64)

## Contributing

To improve the macOS preset, submit issues or pull requests to the Vibe-Linux repository.

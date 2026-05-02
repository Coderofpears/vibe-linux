# Windows 11 UI/UX Preset for Vibe-Linux

A comprehensive KDE Plasma configuration preset that replicates the look and feel of Windows 11.

## Features

### Visual Design
- **Light theme** with Windows 11 color palette (gray tones)
- **Bottom taskbar** positioned at the bottom with centered task buttons
- **Minimalist window decorations** with subtle shadows
- **Breeze Light** color scheme for a clean, modern appearance
- **Segoe UI font** for authentic Windows typography

### User Experience
- **Single-click** file/folder opening (Windows-style)
- **Windows-style keyboard shortcuts**:
  - `Meta + Left/Right` - Snap windows to sides
  - `Meta + Up` - Maximize window
  - `Meta + Down` - Minimize window
  - `Meta + D` - Show desktop
  - `Meta + E` - Open file manager (Dolphin)
  - `Ctrl + Alt + T` - Open terminal
  - `Print` - Screenshot
- **Taskbar features**:
  - Application menu on the left
  - Task buttons in the center
  - System tray on the right
  - Digital clock on the far right
- **Auto-raise and focus on click** (Windows-style behavior)

### System Components
- **SDDM Login Screen** - Configured with Breeze Light theme
- **KDE Window Manager (kwin)** - Optimized for snap windows and smooth animations
- **Plasma Shell** - Bottom panel configuration
- **Global Shortcuts** - Windows 11-style key bindings

## Installation

### Option 1: Apply During Installation
The Windows 11 preset is available as a selectable option during the Vibe-Linux installation process.

### Option 2: Apply to Existing System
If you already have Vibe-Linux installed:

```bash
# Copy the configuration files to your KDE config directory
cp -r configs/windows11/* ~/.config/

# Restart KDE Plasma (or log out and log back in)
kquitapp5 kstart5 plasmashell &
```

### Option 3: Use vibectl
If `vibectl` supports preset management:

```bash
vibectl preset apply windows11
```

## Configuration Files

The preset consists of the following KDE configuration files:

- **kdeglobals** - Global KDE settings (colors, fonts, appearance)
- **plasmashellrc** - Plasma shell configuration (panel layout, widgets)
- **kwinrc** - KDE window manager settings (effects, decorations, shortcuts)
- **kglobalshortcutsrc** - Global keyboard shortcuts
- **kscreenlockerrc** - Screen locker settings
- **sddm.conf** - SDDM login screen configuration

## Customization

To customize the Windows 11 preset:

1. Edit the configuration files in `configs/windows11/`
2. For color customization, modify the `[Colors:*]` sections in `kdeglobals`
3. For taskbar layout, edit the `[Containments][1][General]` section in `plasmashellrc`
4. For window behavior, modify the `[Windows]` section in `kwinrc`

## Known Differences from Windows 11

- Activities and virtual desktops use Plasma-specific terminology
- Some Windows 11 exclusive features (rounded corners, Mica material) are simulated with KDE styling
- File manager uses Dolphin instead of Windows Explorer
- Application launcher uses KDE Application Menu instead of Windows Start Menu

## Reverting to Default

To revert to the default Vibe-Linux KDE configuration:

```bash
# Remove the Windows 11 preset
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

To improve the Windows 11 preset, submit issues or pull requests to the Vibe-Linux repository.

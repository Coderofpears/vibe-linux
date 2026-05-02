# Installation Guide - Vibe-Linux OS

Welcome to Vibe-Linux! This guide will walk you through installing Vibe-Linux on your hardware.

## System Requirements

### Minimum Requirements
- **CPU**: 64-bit x86_64 or ARM64 (aarch64) processor
- **RAM**: 2 GB (4 GB recommended for comfortable usage)
- **Storage**: 15 GB free disk space (20 GB recommended)
- **Display**: 1024x768 or higher resolution
- **Internet**: Required for installation and package downloads

### Supported Hardware
- **Desktops**: Modern x86_64 systems
- **Laptops**: Intel/AMD/Apple Silicon (via ARM64 ISO)
- **Servers**: ARM64 servers and single-board computers
- **GPU**: NVIDIA (Nouveau), AMD (AMDGPU), Intel (i915) - open-source drivers

## Getting Started

### 1. Download the ISO

Visit the [Releases page](https://github.com/Coderofpears/vibe-linux/releases) and download the appropriate ISO for your system:

- **x86_64 (Intel/AMD)**: `vibe-linux-x86_64-*.iso`
- **ARM64 (Apple Silicon/ARM servers)**: `vibe-linux-aarch64-*.iso`

### 2. Verify the ISO

```bash
# Download the SHA256SUMS file from the release
# Then verify:
sha256sum -c SHA256SUMS
```

### 3. Create Bootable USB

#### Option A: Using Etcher (Recommended)
```bash
# Download Balena Etcher from https://www.balena.io/etcher/
# Open Etcher, select the ISO, select your USB drive, and click "Flash"
```

#### Option B: Using Ventoy
```bash
# Download and install Ventoy
# Copy the ISO file to the Ventoy USB drive
# Boot from Ventoy and select the ISO
```

#### Option C: Using `dd` (Linux/macOS)
```bash
# Find your USB device
lsblk

# Unmount the USB (example: /dev/sdb)
umount /dev/sdb*

# Flash the ISO
sudo dd if=vibe-linux-x86_64-*.iso of=/dev/sdb bs=4M status=progress && sync
```

### 4. Boot from USB

1. Insert the USB drive into your computer
2. Restart your computer
3. Press the boot key during startup:
   - **Dell**: F12
   - **HP**: F9 or ESC
   - **Lenovo**: F12
   - **Apple**: Hold ALT (Option) key
   - **ASUS**: F8 or DEL
4. Select the USB drive from the boot menu
5. Wait for the system to load

### 5. Run the Installer

Once booted into the live environment:

```bash
# The installer should start automatically
# If not, run:
sudo vibe-installer
```

### 6. Installation Steps

Follow the guided installer prompts:

#### Hostname
Enter a name for your computer (e.g., `vibe-machine`)

#### User Account
- **Username**: Your login username (lowercase, no spaces)
- **Password**: Your account password (will need this to log in)

#### Disk & Partition
- Select the target disk (⚠️ WARNING: This will be formatted)
- Confirm the partition scheme

#### Timezone
Select your timezone (UTC, America/New_York, Europe/London, etc.)

#### Keyboard Layout
Choose your keyboard layout (en-US, en-GB, de-DE, etc.)

#### Desktop Environment
- **KDE Plasma** (recommended): Full-featured desktop with widgets
- **Hyprland**: Tiling window manager for power users

#### UI Preset
- **Default**: Standard KDE Plasma
- **Windows 11**: Look and feel like Windows 11
- **macOS**: Look and feel like macOS Ventura

#### Performance Mode
- **Full**: All features, suitable for modern systems
- **Lite**: Minimal features, suitable for older hardware
- **Performance**: Balanced, optimized for gaming/development

#### Confirmation
Review your selections and confirm installation

### 7. Installation Completion

The installer will:
1. Partition and format the disk
2. Install Arch Linux base system
3. Install KDE Plasma or Hyprland
4. Install Vibe tools and plugins
5. Configure system settings

This typically takes 10-20 minutes depending on internet speed.

### 8. Reboot

When installation completes:
```bash
# The installer will prompt you to reboot
# Remove the USB drive and press Enter
```

## First Boot

### SDDM Login Screen
1. Enter your username
2. Enter your password
3. Click "Login" or press Enter

### Initial Setup
- **Welcome**: KDE may show a welcome screen
- **Defaults**: System will apply your chosen preset
- **Updates**: Check for system updates using `vibectl update`

## Post-Installation

### Update System
```bash
sudo vibectl update
```

### Install Additional Packages
```bash
# Browse available packages
pacman -S firefox chromium vlc

# Or use vibectl
vibectl install firefox
```

### Switch UI Presets
```bash
# Apply macOS preset
cp -r /opt/vibe-linux/configs/macos/* ~/.config/

# Apply Windows 11 preset
cp -r /opt/vibe-linux/configs/windows11/* ~/.config/

# Restart Plasma
kquitapp5 kstart5 plasmashell &
```

### Install Plugins
```bash
vibectl plugins list
vibectl plugins run vibe.copilot
```

## Troubleshooting

### Boot Issues

**Black screen after logo**
- Wait 30 seconds (first boot is slow)
- Check graphics drivers: `lspci | grep -i vga`

**Stuck at UEFI splash**
- Try disabling Secure Boot in UEFI/BIOS
- Try disabling Fast Boot

### Network Issues

**No internet connection**
```bash
# Check network status
nmtui  # Network manager TUI

# Or manually:
sudo systemctl restart NetworkManager
```

### Display Issues

**No display/black screen**
```bash
# Try different display server
# Edit: ~/.config/plasmarc
# Set: Sessions=plasmawayland or Sessions=plasmax11

# Or revert to X11:
echo "export DISPLAY=:0" >> ~/.bashrc
```

### Installation Failed

**Disk space error**
- Ensure you have at least 20 GB free
- Run `lsblk` to verify disk detection

**Package download failed**
- Check internet connection
- Try a different mirror:
  ```bash
  sudo pacman-mirrors --geoip
  ```

## Getting Help

- **Documentation**: [docs/](../docs/) folder
- **GitHub Issues**: [Report bugs](https://github.com/Coderofpears/vibe-linux/issues)
- **Community**: Ask on Arch Linux forums
- **Diagnostic info**: Run `vibectl diagnostics`

## Advanced Installation

### Offline Installation
1. Build your own ISO with all packages
2. Use `archinstall` directly (advanced users)

### Custom Partitioning
During installation, if you want manual partition control:
```bash
# Exit the installer
# Manually partition:
sudo cfdisk /dev/sda
sudo mkfs.ext4 /dev/sda2
sudo mount /dev/sda2 /mnt

# Then run installer again
```

### Dual Boot
1. Partition from another OS (20+ GB for Vibe-Linux)
2. During Vibe-Linux installation, select "Use existing partition"
3. Ensure EFI partition is detected
4. Complete installation

## What's Next?

After installation:
1. Run `vibectl diagnostics` to verify hardware detection
2. Check for driver packages: `pacman -Qe | grep vulkan`
3. Enable time sync: `timedatectl set-ntp true`
4. Secure your system: `sudo passwd root` (set root password)
5. Explore KDE settings: System Settings (or `systemsettings`)

## Feedback

Encountered an issue? Have suggestions? 
- [Create an issue](https://github.com/Coderofpears/vibe-linux/issues/new)
- [Join discussions](https://github.com/Coderofpears/vibe-linux/discussions)

Welcome to Vibe-Linux! 🚀

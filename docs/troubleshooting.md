# Vibe-Linux Troubleshooting Guide

## Common Installation Issues

### Issue: USB Boot Not Appearing in BIOS

**Symptoms**: USB drive doesn't show up as boot option

**Solutions**:
1. Try different USB ports (especially USB 3.0 if booting from 2.0)
2. Disable Secure Boot in BIOS settings
3. Change BIOS boot mode from UEFI to Legacy or vice versa
4. Recreate USB using Rufus (Windows) or `dd` (Linux/Mac)

**Command (Unix/Linux)**:
```bash
# Find USB device
lsblk

# Write ISO to USB
sudo dd if=vibe-linux-x86_64.iso of=/dev/sdX bs=4M status=progress sync
```

---

### Issue: Black Screen After Boot

**Symptoms**: ISO loads but screen goes black

**Solutions**:
1. **Wait longer** - First boot can take 2-3 minutes
2. **Graphics driver issue** - Try safe mode:
   - At GRUB: Press `e`
   - Add `nomodeset` to kernel line
   - Press `Ctrl+X` to boot
3. **If still black**, try older graphics profile:
   - At boot prompt, select "Compatibility Mode"

---

### Issue: "No Space Left on Device" During Installation

**Symptoms**: Installation fails with disk space error

**Solutions**:
1. Ensure you have 15+ GB free on target disk
2. If dual-booting, shrink Windows/macOS partition first
3. Restart installation and try again
4. Use command-line tools:
   ```bash
   sudo cfdisk /dev/sdX  # Replace X with your disk
   ```

---

### Issue: WiFi Not Available During Installation

**Symptoms**: Network adapter not detected

**Solutions**:
1. **Reconnect USB after boot** (some drivers need time)
2. **Use Ethernet** if available
3. **Update drivers after installation**:
   ```bash
   vibectl update
   ```
4. **Check supported hardware**:
   ```bash
   vibectl diagnostics
   ```

---

## Common Runtime Issues

### Issue: KDE Plasma Freezes or Crashes

**Symptoms**: Desktop becomes unresponsive

**Solutions**:
1. **Restart Plasma** (without full reboot):
   ```bash
   killall plasmashell
   kstart5 plasmashell &
   ```

2. **Disable animations** (if hardware is slow):
   - System Settings > Workspace Behavior > General
   - Set Animation Speed to "Instant"

3. **Reset KDE config** (last resort):
   ```bash
   rm -rf ~/.config/plasmashellrc
   kstart5 plasmashell &
   ```

---

### Issue: Very Slow System Performance

**Symptoms**: System lags, applications slow to open

**Solutions**:
1. **Check RAM usage**:
   ```bash
   vibe-monitor
   # or
   free -h
   ```

2. **Switch to Lite mode** (if under 4GB RAM):
   ```bash
   vibectl mode lite
   ```

3. **Disable desktop search** (Baloo):
   ```bash
   balooctl disable
   ```

4. **Check disk space**:
   ```bash
   df -h
   ```

5. **Disable visual effects**:
   - System Settings > Workspace > Desktop Effects
   - Set to "none"

---

### Issue: Can't Access Files/Permissions Denied

**Symptoms**: "Permission denied" errors when accessing files

**Solutions**:
1. **Check file ownership**:
   ```bash
   ls -l /path/to/file
   ```

2. **Fix permissions**:
   ```bash
   chmod u+r /path/to/file      # Add read for user
   chmod u+w /path/to/file      # Add write for user
   chmod u+x /path/to/file      # Add execute for user
   ```

3. **For system files, use sudo**:
   ```bash
   sudo nano /etc/config-file
   ```

4. **Check user groups**:
   ```bash
   groups $(whoami)
   ```

---

### Issue: Sound/Audio Not Working

**Symptoms**: No audio output, speakers muted

**Solutions**:
1. **Unmute speakers**:
   ```bash
   pactl set-sink-mute @DEFAULT_SINK@ false
   pactl set-sink-volume @DEFAULT_SINK@ 50%
   ```

2. **Check audio devices**:
   ```bash
   pactl list short sinks
   ```

3. **Restart audio service**:
   ```bash
   systemctl --user restart pulseaudio
   ```

4. **Check ALSA levels**:
   ```bash
   amixer
   ```

---

## Package & Updates

### Issue: Updates Fail or Packages Can't Install

**Symptoms**: `pacman` or `vibectl update` fails

**Solutions**:
1. **Sync package databases**:
   ```bash
   sudo pacman -Sy
   ```

2. **Try full update**:
   ```bash
   sudo pacman -Syu
   ```

3. **Fix broken packages**:
   ```bash
   sudo pacman -Suu  # Downgrade if needed
   ```

4. **Clear package cache**:
   ```bash
   sudo pacman -Scc
   ```

5. **Check if disc is full**:
   ```bash
   df -h /
   vibe-clean
   ```

---

### Issue: AUR Packages Won't Install

**Symptoms**: `yay` or `paru` fails to build

**Solutions**:
1. **Install AUR helper** (if not present):
   ```bash
   sudo pacman -S yay
   ```

2. **Build dependencies**:
   ```bash
   yay -Sy --needed base-devel
   ```

3. **Try building manually**:
   ```bash
   git clone https://aur.archlinux.org/package-name
   cd package-name
   makepkg -si
   ```

---

## Plugin System

### Issue: Plugin Won't Run

**Symptoms**: `vibectl plugins run` returns error

**Solutions**:
1. **Validate plugin manifest**:
   ```bash
   vibectl plugins validate /path/to/plugin
   ```

2. **Check permissions**:
   - View required permissions in `manifest.json`
   - Ensure user has permission to access

3. **Try with debug output**:
   ```bash
   VIBE_DEBUG=1 vibectl plugins run plugin-id
   ```

4. **Check plugin logs**:
   ```bash
   cat ~/.local/state/vibe-linux/setup.log
   ```

---

### Issue: Permission Denied When Running Plugin

**Symptoms**: Plugin tries to access file but gets permission error

**Solutions**:
1. **Check plugin permissions**:
   ```bash
   grep "permissions" manifest.json
   ```

2. **Add required permissions**:
   ```json
   {
     "permissions": ["read:/path/to/file"]
   }
   ```

3. **Run with proper privileges**:
   - Some plugins need `sudo` (not recommended)
   - Better: Add plugin to sudoers or change file ownership

---

## Networking

### Issue: No Internet Connection

**Symptoms**: Can't browse or download updates

**Solutions**:
1. **Check connection status**:
   ```bash
   nmtui    # Interactive network manager
   # or
   nmcli device show
   ```

2. **Connect to WiFi**:
   ```bash
   nmcli device wifi list
   nmcli device wifi connect "SSID" password "PASSWORD"
   ```

3. **Test connection**:
   ```bash
   ping 8.8.8.8
   ```

4. **Restart network manager**:
   ```bash
   sudo systemctl restart NetworkManager
   ```

5. **Check DNS**:
   ```bash
   cat /etc/resolv.conf
   ```

---

### Issue: WiFi Disconnects Frequently

**Symptoms**: WiFi drops connection randomly

**Solutions**:
1. **Reduce WiFi power saving**:
   ```bash
   sudo iwconfig wlan0 power off
   ```

2. **Check signal strength**:
   ```bash
   nmcli device wifi list
   ```

3. **Update network drivers**:
   ```bash
   vibectl update
   ```

4. **Try different channel**:
   - Access router settings
   - Try channels 1, 6, or 11 (2.4GHz) or auto (5GHz)

---

## Dual-Boot Issues

### Issue: Windows/macOS Entry Missing from GRUB

**Symptoms**: Only Vibe-Linux boots, other OS not available

**Solutions**:
1. **Reinstall GRUB**:
   ```bash
   sudo grub-mkconfig -o /boot/grub/grub.cfg
   ```

2. **Enable other OS detection** (if GRUB didn't find it):
   ```bash
   sudo pacman -S os-prober
   sudo os-prober
   sudo grub-mkconfig -o /boot/grub/grub.cfg
   ```

3. **Check BIOS boot order**:
   - Restart, enter BIOS
   - Change boot order to Vibe-Linux first

---

## Performance Diagnostics

### Issue: Need Complete System Health Check

**Run comprehensive diagnostics**:
```bash
vibectl diagnostics
```

This shows:
- CPU model and speed
- RAM total and available
- Disk usage
- GPU information
- Kernel version
- Network status
- Loaded plugins

---

## Getting More Help

### When to Seek Help

- **Issue not in this guide**: Search GitHub Issues
- **Reproducible bug**: File an issue with:
  - Error message
  - Steps to reproduce
  - System information (`vibectl diagnostics`)
  - Output of relevant commands

### Where to Get Help

1. **Documentation**: [GitHub Docs](https://github.com/Coderofpears/vibe-linux/tree/main/docs)
2. **Issues**: [GitHub Issues](https://github.com/Coderofpears/vibe-linux/issues)
3. **Discussions**: [GitHub Discussions](https://github.com/Coderofpears/vibe-linux/discussions)
4. **Community**: Share experience, help others

---

## Advanced Troubleshooting

### Access GRUB Console

If system won't boot:
1. Power on and quickly press `Shift` (GRUB menu)
2. Select entry and press `e` to edit
3. Add `single` or `rd.systemd.unit=rescue.target` to boot parameters
4. Press `Ctrl+X` to boot

### Boot from Live USB

If installation is corrupted:
1. Boot from Vibe-Linux USB
2. Load USB filesystem:
   ```bash
   mount /dev/sdX1 /mnt    # Replace X with your disk
   arch-chroot /mnt bash
   ```

### Check Kernel Logs

For deep system issues:
```bash
dmesg                    # Kernel messages
journalctl -xe          # System journal (last boot)
journalctl -b -p err    # Only errors
```

---

## Prevention

### Regular Maintenance

- **Weekly**: Check disk space (`df -h`)
- **Monthly**: Update system (`vibectl update`)
- **Quarterly**: Clean cache (`pacman -Scc`)
- **Annually**: Backup important data

### Avoid Common Mistakes

- ❌ Don't use `rm -rf` on system directories
- ❌ Don't modify `/etc/` files without backup
- ❌ Don't grant unnecessary plugin permissions
- ❌ Don't ignore security updates
- ✅ Do read error messages carefully
- ✅ Do backup before major changes
- ✅ Do test in VM before production

---

**Still stuck? Search the [knowledge base](https://github.com/Coderofpears/vibe-linux/discussions) or open an [issue](https://github.com/Coderofpears/vibe-linux/issues)!**

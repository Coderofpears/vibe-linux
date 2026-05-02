#!/usr/bin/env python3
"""Quick Settings plugin - access common settings."""

import subprocess
import sys
from pathlib import Path


def toggle_bluetooth() -> bool:
    """Toggle Bluetooth."""
    try:
        result = subprocess.run(
            ["rfkill", "list", "bluetooth"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        is_blocked = "Soft blocked: yes" in result.stdout or "Hard blocked: yes" in result.stdout
        
        if is_blocked:
            subprocess.run(["rfkill", "unblock", "bluetooth"], timeout=5, check=True)
            return True
        else:
            subprocess.run(["rfkill", "block", "bluetooth"], timeout=5, check=True)
            return False
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
        print("Note: rfkill command not available or Bluetooth unavailable")
        return False


def toggle_wifi() -> bool:
    """Toggle WiFi."""
    try:
        result = subprocess.run(
            ["rfkill", "list", "wlan"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        is_blocked = "Soft blocked: yes" in result.stdout or "Hard blocked: yes" in result.stdout
        
        if is_blocked:
            subprocess.run(["rfkill", "unblock", "wlan"], timeout=5, check=True)
            return True
        else:
            subprocess.run(["rfkill", "block", "wlan"], timeout=5, check=True)
            return False
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
        print("Note: rfkill command not available or WiFi unavailable")
        return False


def set_brightness(percent: int) -> bool:
    """Set screen brightness (0-100)."""
    percent = max(0, min(100, percent))
    
    try:
        # Find backlight device
        backlight_path = Path("/sys/class/backlight")
        if not backlight_path.exists():
            print("No backlight device found")
            return False
        
        devices = list(backlight_path.glob("*/"))
        if not devices:
            print("No backlight devices found")
            return False
        
        device = devices[0]
        max_brightness_file = device / "max_brightness"
        brightness_file = device / "brightness"
        
        if not max_brightness_file.exists() or not brightness_file.exists():
            print("Backlight files not accessible")
            return False
        
        max_brightness = int(max_brightness_file.read_text().strip())
        new_brightness = int(max_brightness * (percent / 100))
        
        brightness_file.write_text(str(new_brightness))
        return True
    except (OSError, ValueError, PermissionError) as e:
        print(f"Error setting brightness: {e}")
        return False


def show_settings_menu() -> None:
    """Show interactive settings menu."""
    print("\n╔══════════════════════════════════════════╗")
    print("║        VIBE QUICK SETTINGS v1.0          ║")
    print("╚══════════════════════════════════════════╝")
    print()
    print("Available settings:")
    print("  1. Toggle Bluetooth")
    print("  2. Toggle WiFi")
    print("  3. Set Screen Brightness")
    print("  4. Open Settings App")
    print("  5. Exit")
    print()
    print("Note: Run with arguments for non-interactive mode:")
    print("  monitor.py bluetooth [on|off|toggle]")
    print("  monitor.py wifi [on|off|toggle]")
    print("  monitor.py brightness [0-100]")


def main() -> None:
    """Main entry point."""
    args = sys.argv[1:]
    
    if not args:
        show_settings_menu()
        return
    
    command = args[0].lower()
    
    if command == "bluetooth":
        result = toggle_bluetooth()
        print(f"Bluetooth: {'ON' if result else 'OFF'}")
    
    elif command == "wifi":
        result = toggle_wifi()
        print(f"WiFi: {'ON' if result else 'OFF'}")
    
    elif command == "brightness":
        if len(args) > 1:
            try:
                percent = int(args[1])
                if set_brightness(percent):
                    print(f"Brightness set to {percent}%")
                else:
                    print("Failed to set brightness")
            except ValueError:
                print("Brightness must be a number 0-100")
        else:
            print("Usage: settings.py brightness <0-100>")
    
    elif command == "settings":
        subprocess.run(["systemsettings5"], timeout=30)
    
    else:
        print(f"Unknown command: {command}")
        show_settings_menu()


if __name__ == "__main__":
    main()

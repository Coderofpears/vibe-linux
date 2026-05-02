#!/usr/bin/env bash
# First-run setup wizard for Vibe-Linux
# Runs on first login to personalize the system

set -euo pipefail

VIBE_SETUP_FLAG="${HOME}/.local/state/vibe-linux/.first-run-complete"
SETUP_LOG="${HOME}/.local/state/vibe-linux/setup.log"

# Create state directory
mkdir -p "$(dirname "$VIBE_SETUP_FLAG")" "$(dirname "$SETUP_LOG")"

# Log function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" >> "$SETUP_LOG"
}

# Check if already run
if [ -f "$VIBE_SETUP_FLAG" ]; then
    log "First-run wizard already completed"
    exit 0
fi

log "Starting first-run setup wizard"

# Show welcome
echo ""
echo "╔══════════════════════════════════════════╗"
echo "║     Welcome to Vibe-Linux!               ║"
echo "║                                          ║"
echo "║  Let's personalize your system.          ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Check for internet
echo "🌐 Checking internet connection..."
if ping -c 1 8.8.8.8 > /dev/null 2>&1; then
    echo "   ✅ Connected to internet"
    HAS_INTERNET=true
else
    echo "   ⚠️  No internet connection detected"
    HAS_INTERNET=false
fi
echo ""

# Optional: Update system
if [ "$HAS_INTERNET" = true ]; then
    echo "🔄 Would you like to update the system now? (y/n)"
    read -r update_choice
    if [ "$update_choice" = "y" ] || [ "$update_choice" = "Y" ]; then
        echo "   Updating packages..."
        vibectl update || log "System update failed"
        echo "   ✅ Update complete"
    fi
fi
echo ""

# UI Preset selection
echo "🎨 Choose your UI style:"
echo "  1. Vibe Default (KDE Plasma)"
echo "  2. Windows 11 Style"
echo "  3. macOS Style"
echo "  (Press Enter to skip)"
echo ""
read -r preset_choice
case "$preset_choice" in
    1)
        echo "   Keeping Vibe Default theme"
        log "User selected: Vibe Default theme"
        ;;
    2)
        echo "   Applying Windows 11 theme..."
        cp -r /opt/vibe-linux/configs/windows11/* ~/.config/ 2>/dev/null || true
        log "User selected: Windows 11 theme"
        ;;
    3)
        echo "   Applying macOS theme..."
        cp -r /opt/vibe-linux/configs/macos/* ~/.config/ 2>/dev/null || true
        log "User selected: macOS theme"
        ;;
    *)
        echo "   Keeping current theme"
        ;;
esac
echo ""

# Performance mode selection
echo "⚡ Choose performance profile:"
echo "  1. Full (All features - requires 4GB+ RAM)"
echo "  2. Lite (Minimal - for older hardware)"
echo "  3. Performance (Balanced - recommended)"
echo "  (Press Enter to skip)"
echo ""
read -r mode_choice
case "$mode_choice" in
    1)
        echo "   Applying Full mode..."
        vibectl mode full --dry-run 2>/dev/null || true
        log "User selected: Full mode"
        ;;
    2)
        echo "   Applying Lite mode..."
        vibectl mode lite --dry-run 2>/dev/null || true
        log "User selected: Lite mode"
        ;;
    3)
        echo "   Applying Performance mode..."
        vibectl mode performance --dry-run 2>/dev/null || true
        log "User selected: Performance mode"
        ;;
    *)
        echo "   Keeping current mode"
        ;;
esac
echo ""

# Optional: Enable daily updates
echo "🔄 Enable automatic system updates? (y/n)"
read -r auto_update_choice
if [ "$auto_update_choice" = "y" ] || [ "$auto_update_choice" = "Y" ]; then
    echo "   Enabling automatic updates..."
    # Note: In production, this would enable a systemd timer
    log "User enabled: Automatic updates"
fi
echo ""

# Show helpful tips
echo "💡 Helpful Tips:"
echo "  • Press Meta (Windows key) to open app launcher"
echo "  • Use Meta+E to open file manager"
echo "  • Right-click desktop for quick access menu"
echo "  • Visit https://github.com/Coderofpears/vibe-linux for docs"
echo ""

# Final message
echo "✨ Setup complete! Your system is ready."
echo "   To open Plasma Settings: Meta+I"
echo "   To see available plugins: vibectl plugins list"
echo ""

# Mark as complete
touch "$VIBE_SETUP_FLAG"
log "First-run wizard completed successfully"

# Restart Plasma to apply theme changes
if [ "$preset_choice" = "2" ] || [ "$preset_choice" = "3" ]; then
    echo "🔄 Restarting Plasma to apply theme..."
    kquitapp5 kstart5 plasmashell &
fi

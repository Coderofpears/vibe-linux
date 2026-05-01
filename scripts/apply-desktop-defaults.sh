#!/usr/bin/env bash
set -euo pipefail

USER_HOME="${1:-${HOME}}"
VIBE_SHARE="${2:-/usr/share/vibe-linux}"

install -d "${USER_HOME}/.config"

for config in kdeglobals kwinrc plasmashellrc kscreenlockerrc kglobalshortcutsrc; do
  if [[ -f "${VIBE_SHARE}/kde/${config}" ]]; then
    install -m 0644 "${VIBE_SHARE}/kde/${config}" "${USER_HOME}/.config/${config}"
  fi
done

if [[ -f "${VIBE_SHARE}/hyprland/hyprland.conf" ]]; then
  install -d "${USER_HOME}/.config/hypr"
  install -m 0644 "${VIBE_SHARE}/hyprland/hyprland.conf" "${USER_HOME}/.config/hypr/hyprland.conf"
fi

echo "Applied Vibe desktop defaults for ${USER_HOME}."

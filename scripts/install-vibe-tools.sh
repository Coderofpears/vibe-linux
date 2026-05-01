#!/usr/bin/env bash
set -euo pipefail

TARGET_ROOT="${1:-/mnt}"
REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

install -Dm755 "${REPO_ROOT}/tools/vibectl/vibectl.py" "${TARGET_ROOT}/usr/bin/vibectl"
install -Dm755 "${REPO_ROOT}/tools/vibe-plugin-runtime/vibe-plugin-runtime.py" "${TARGET_ROOT}/usr/bin/vibe-plugin-runtime"

install -Dm644 "${REPO_ROOT}/systemd/vibe-plugin-audit.service" \
  "${TARGET_ROOT}/usr/lib/systemd/system/vibe-plugin-audit.service"

install -Dm644 "${REPO_ROOT}/configs/modes/full.json" "${TARGET_ROOT}/usr/share/vibe-linux/modes/full.json"
install -Dm644 "${REPO_ROOT}/configs/modes/lite.json" "${TARGET_ROOT}/usr/share/vibe-linux/modes/lite.json"
install -Dm644 "${REPO_ROOT}/configs/modes/performance.json" "${TARGET_ROOT}/usr/share/vibe-linux/modes/performance.json"

install -Dm644 "${REPO_ROOT}/configs/kde/kdeglobals" "${TARGET_ROOT}/usr/share/vibe-linux/kde/kdeglobals"
install -Dm644 "${REPO_ROOT}/configs/kde/kwinrc" "${TARGET_ROOT}/usr/share/vibe-linux/kde/kwinrc"
install -Dm644 "${REPO_ROOT}/configs/kde/plasmashellrc" "${TARGET_ROOT}/usr/share/vibe-linux/kde/plasmashellrc"
install -Dm644 "${REPO_ROOT}/configs/kde/kscreenlockerrc" "${TARGET_ROOT}/usr/share/vibe-linux/kde/kscreenlockerrc"
install -Dm644 "${REPO_ROOT}/configs/kde/sddm.conf" "${TARGET_ROOT}/etc/sddm.conf.d/10-vibe.conf"
install -Dm644 "${REPO_ROOT}/configs/hyprland/hyprland.conf" "${TARGET_ROOT}/usr/share/vibe-linux/hyprland/hyprland.conf"
install -Dm644 "${REPO_ROOT}/configs/shell/vibe-profile.sh" "${TARGET_ROOT}/etc/profile.d/vibe.sh"
install -Dm644 "${REPO_ROOT}/configs/kde/kglobalshortcutsrc" "${TARGET_ROOT}/usr/share/vibe-linux/kde/kglobalshortcutsrc"
install -Dm644 "${REPO_ROOT}/configs/gestures/touchegg.conf" "${TARGET_ROOT}/etc/touchegg/touchegg.conf"
install -Dm644 "${REPO_ROOT}/configs/vibe/locale/en-US.json" "${TARGET_ROOT}/usr/share/vibe-linux/locale/en-US.json"
install -Dm644 "${REPO_ROOT}/configs/vibe/style.json" "${TARGET_ROOT}/usr/share/vibe-linux/style.json"

if [[ -d "${REPO_ROOT}/examples/plugins/vibe-copilot" ]]; then
  mkdir -p "${TARGET_ROOT}/usr/share/vibe-linux/plugins/dev.vibe.copilot"
  cp -a "${REPO_ROOT}/examples/plugins/vibe-copilot/." "${TARGET_ROOT}/usr/share/vibe-linux/plugins/dev.vibe.copilot/"
fi

mkdir -p "${TARGET_ROOT}/usr/share/vibe-linux/plugins" \
  "${TARGET_ROOT}/var/lib/vibe/plugins" \
  "${TARGET_ROOT}/var/log/vibe"

echo "Installed Vibe tooling into ${TARGET_ROOT}."

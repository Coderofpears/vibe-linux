#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

python3 -m compileall tools installer examples/plugins
python3 tools/vibectl/vibectl.py --help >/dev/null
python3 tools/vibectl/vibectl.py install --dry-run firefox >/dev/null
python3 tools/vibectl/vibectl.py mode lite --dry-run >/dev/null
python3 tools/vibe-plugin-runtime/vibe-plugin-runtime.py --help >/dev/null
python3 tools/vibe-plugin-runtime/vibe-plugin-runtime.py validate examples/plugins/system-info >/dev/null
python3 tools/vibe-plugin-runtime/vibe-plugin-runtime.py validate examples/plugins/package-search >/dev/null
python3 tools/vibe-plugin-runtime/vibe-plugin-runtime.py validate examples/plugins/vibe-copilot >/dev/null
python3 tools/vibe-plugin-runtime/vibe-plugin-runtime.py validate examples/plugins/system-monitor >/dev/null
python3 tools/vibe-plugin-runtime/vibe-plugin-runtime.py validate examples/plugins/quick-settings >/dev/null
python3 tools/vibe-plugin-runtime/vibe-plugin-runtime.py validate examples/plugins/system-cleaner >/dev/null
python3 -m json.tool configs/modes/full.json >/dev/null
python3 -m json.tool configs/modes/lite.json >/dev/null
python3 -m json.tool configs/modes/performance.json >/dev/null
python3 -m json.tool configs/modes/gaming.json >/dev/null
python3 -m json.tool configs/modes/development.json >/dev/null
python3 -m json.tool configs/modes/windows11.json >/dev/null
python3 -m json.tool configs/modes/macos.json >/dev/null
python3 -m json.tool configs/vibe/locale/en-US.json >/dev/null
python3 -m json.tool configs/vibe/style.json >/dev/null

# Validate KDE config files for presets
for preset in windows11 macos; do
  [ -f "configs/${preset}/kdeglobals" ] || exit 1
  [ -f "configs/${preset}/plasmashellrc" ] || exit 1
  [ -f "configs/${preset}/kwinrc" ] || exit 1
  [ -f "configs/${preset}/kglobalshortcutsrc" ] || exit 1
  [ -f "configs/${preset}/kscreenlockerrc" ] || exit 1
  [ -f "configs/${preset}/sddm.conf" ] || exit 1
done

# Validate architecture-specific package lists
[ -f archiso/packages.x86_64 ] || exit 1
[ -f archiso/packages.aarch64 ] || exit 1

echo "Smoke checks passed."

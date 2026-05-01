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
python3 -m json.tool configs/modes/full.json >/dev/null
python3 -m json.tool configs/modes/lite.json >/dev/null
python3 -m json.tool configs/modes/performance.json >/dev/null
python3 -m json.tool configs/vibe/locale/en-US.json >/dev/null
python3 -m json.tool configs/vibe/style.json >/dev/null

echo "Smoke checks passed."

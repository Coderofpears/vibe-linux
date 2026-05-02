#!/usr/bin/env bash
# Quick start script for Vibe-Linux development

set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "🚀 Vibe-Linux Development Quick Start"
echo "======================================"
echo ""

# Check Python version
echo "📦 Checking Python version..."
python_version=$(python3 --version | cut -d' ' -f2)
echo "  Python version: $python_version"

if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)'; then
    echo "  ⚠️  Warning: Python 3.11+ is recommended"
fi
echo ""

# Run smoke tests
echo "🧪 Running smoke tests..."
if bash scripts/smoke-test.sh > /dev/null 2>&1; then
    echo "  ✅ All smoke tests passed"
else
    echo "  ❌ Some tests failed"
    bash scripts/smoke-test.sh
    exit 1
fi
echo ""

# Show vibectl help
echo "📋 Available commands:"
echo "  vibectl:"
python3 tools/vibectl/vibectl.py --help 2>/dev/null | head -20 || true
echo ""

# Check for build requirements
echo "🔧 Build requirements for ISO:"
echo "  - archiso: $(command -v mkarchiso >/dev/null 2>&1 && echo '✅' || echo '❌ Not found')"
echo "  - rsync:   $(command -v rsync >/dev/null 2>&1 && echo '✅' || echo '❌ Not found')"
echo "  - bwrap:   $(command -v bwrap >/dev/null 2>&1 && echo '✅' || echo '❌ Not found')"
echo ""

# Show project structure
echo "📁 Project structure:"
echo "  configs/"
ls -la configs/ | grep "^d" | tail -n +2 | awk '{print "    - " $NF}' || true
echo "  tools/"
ls -la tools/ | grep "^d" | tail -n +2 | awk '{print "    - " $NF}' || true
echo ""

# Show available presets
echo "🎨 Available UI presets:"
ls -1 configs/modes/*.json | xargs -I {} basename {} .json | sed 's/^/  - /'
echo ""

# Show next steps
echo "✨ Next steps:"
echo "  1. Read the documentation: cat INSTALLATION.md"
echo "  2. Build an ISO:           sudo ./scripts/build-iso-arch.sh x86_64"
echo "  3. Make changes and test:  bash scripts/smoke-test.sh"
echo "  4. Commit and push:        git add . && git commit -m 'message' && git push"
echo ""

echo "🎉 Development environment ready!"

#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
ARCHS="${@:-x86_64 aarch64}"  # Build both by default

if [[ "${EUID}" -ne 0 ]]; then
  echo "build-all-iso.sh must run as root because mkarchiso creates device nodes and mounts." >&2
  exit 1
fi

echo "Building Vibe-Linux OS ISOs for architectures: ${ARCHS}"
echo "=================================================="

for ARCH in ${ARCHS}; do
  echo ""
  echo "Building for ${ARCH}..."
  sudo "${ROOT_DIR}/scripts/build-iso-arch.sh" "${ARCH}"
  
  if [ $? -eq 0 ]; then
    echo "✓ ${ARCH} build completed successfully"
  else
    echo "✗ ${ARCH} build failed"
    exit 1
  fi
done

echo ""
echo "=================================================="
echo "All ISO builds completed successfully!"
echo "Output files:"
ls -lh "${ROOT_DIR}/out/"*.iso 2>/dev/null || echo "No ISO files found"

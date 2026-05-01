#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
PROFILE_DIR="${ROOT_DIR}/archiso"
WORK_DIR="${ROOT_DIR}/work"
OUT_DIR="${ROOT_DIR}/out"
STAGED_PROFILE="${WORK_DIR}/profile"

if [[ "${EUID}" -ne 0 ]]; then
  echo "build-iso.sh must run as root because mkarchiso creates device nodes and mounts." >&2
  exit 1
fi

if ! command -v mkarchiso >/dev/null 2>&1; then
  echo "mkarchiso not found. Install the archiso package first." >&2
  exit 1
fi

if ! command -v rsync >/dev/null 2>&1; then
  echo "rsync not found. Install rsync first." >&2
  exit 1
fi

rm -rf "${STAGED_PROFILE}"
mkdir -p "${STAGED_PROFILE}" "${OUT_DIR}"
rsync -a "${PROFILE_DIR}/" "${STAGED_PROFILE}/"

mkdir -p "${STAGED_PROFILE}/airootfs/opt/vibe-linux"
rsync -a \
  --exclude ".git" \
  --exclude "out" \
  --exclude "work" \
  "${ROOT_DIR}/" \
  "${STAGED_PROFILE}/airootfs/opt/vibe-linux/"

echo "Building Vibe-Linux OS installer ISO..."
mkarchiso -v -w "${WORK_DIR}/mkarchiso" -o "${OUT_DIR}" "${STAGED_PROFILE}"

echo "ISO build complete. Output directory: ${OUT_DIR}"

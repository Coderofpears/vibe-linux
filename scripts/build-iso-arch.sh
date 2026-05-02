#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
ARCH="${1:-x86_64}"  # Default to x86_64 if not specified
PROFILE_DIR="${ROOT_DIR}/archiso"
WORK_DIR="${ROOT_DIR}/work-${ARCH}"
OUT_DIR="${ROOT_DIR}/out"
STAGED_PROFILE="${WORK_DIR}/profile"

# Validate architecture
if [[ "${ARCH}" != "x86_64" && "${ARCH}" != "aarch64" ]]; then
  echo "Unsupported architecture: ${ARCH}" >&2
  echo "Supported architectures: x86_64, aarch64" >&2
  exit 1
fi

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

echo "Building Vibe-Linux OS for ${ARCH}..."

# Clean and prepare working directories
rm -rf "${STAGED_PROFILE}"
mkdir -p "${STAGED_PROFILE}" "${OUT_DIR}"
rsync -a "${PROFILE_DIR}/" "${STAGED_PROFILE}/"

# Copy project files to airootfs
mkdir -p "${STAGED_PROFILE}/airootfs/opt/vibe-linux"
rsync -a \
  --exclude ".git" \
  --exclude "out" \
  --exclude "work*" \
  "${ROOT_DIR}/" \
  "${STAGED_PROFILE}/airootfs/opt/vibe-linux/"

# Update profiledef.sh for the target architecture
PROFILEDEF="${STAGED_PROFILE}/profiledef.sh"
sed -i.bak "s/^arch=.*/arch=\"${ARCH}\"/" "${PROFILEDEF}"

# Set appropriate boot modes and compression for architecture
if [[ "${ARCH}" == "aarch64" ]]; then
  # ARM64 boot configuration
  sed -i.bak 's/^bootmodes=.*/bootmodes=("uefi-aa64.grub.esp")/' "${PROFILEDEF}"
  sed -i.bak 's/^airootfs_image_tool_options=.*/airootfs_image_tool_options=("-comp" "xz" "-b" "1M" "-Xdict-size" "1M")/' "${PROFILEDEF}"
else
  # x86_64 boot configuration
  sed -i.bak 's/^bootmodes=.*/bootmodes=("bios.syslinux.mbr" "bios.syslinux.eltorito" "uefi-ia32.grub.esp" "uefi-x64.grub.esp")/' "${PROFILEDEF}"
  sed -i.bak 's/^airootfs_image_tool_options=.*/airootfs_image_tool_options=("-comp" "xz" "-Xbcj" "x86" "-b" "1M" "-Xdict-size" "1M")/' "${PROFILEDEF}"
fi

# Clean up backup files
rm -f "${PROFILEDEF}.bak"

echo "Building ISO with mkarchiso..."
mkarchiso -v -w "${WORK_DIR}/mkarchiso" -o "${OUT_DIR}" "${STAGED_PROFILE}"

echo "ISO build complete for ${ARCH}. Output directory: ${OUT_DIR}"
ls -lh "${OUT_DIR}"/*.iso 2>/dev/null || echo "Warning: No ISO files found in output directory"

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
echo "Details:"
echo "  Root directory: ${ROOT_DIR}"
echo "  Architecture: ${ARCH}"
echo "  Work directory: ${WORK_DIR}"
echo "  Output directory: ${OUT_DIR}"
echo "  Profile directory: ${PROFILE_DIR}"
echo ""

# Clean and prepare working directories
echo "Cleaning previous build artifacts..."
rm -rf "${STAGED_PROFILE}" "${WORK_DIR}/mkarchiso"
mkdir -p "${STAGED_PROFILE}" "${OUT_DIR}"

echo "Staging archiso profile..."
if ! rsync -a "${PROFILE_DIR}/" "${STAGED_PROFILE}/"; then
  echo "Error: Failed to sync archiso profile" >&2
  exit 1
fi

# Copy project files to airootfs
echo "Copying Vibe-Linux files to airootfs..."
mkdir -p "${STAGED_PROFILE}/airootfs/opt/vibe-linux"
if ! rsync -a \
  --exclude ".git" \
  --exclude "out" \
  --exclude "work*" \
  "${ROOT_DIR}/" \
  "${STAGED_PROFILE}/airootfs/opt/vibe-linux/"; then
  echo "Error: Failed to copy project files" >&2
  exit 1
fi

# Update profiledef.sh for the target architecture
echo "Configuring profiledef.sh for ${ARCH}..."
PROFILEDEF="${STAGED_PROFILE}/profiledef.sh"
if [ ! -f "${PROFILEDEF}" ]; then
  echo "Error: profiledef.sh not found at ${PROFILEDEF}" >&2
  exit 1
fi

sed -i.bak "s/^arch=.*/arch=\"${ARCH}\"/" "${PROFILEDEF}"

# Set appropriate boot modes and compression for architecture
if [[ "${ARCH}" == "aarch64" ]]; then
  echo "  Setting ARM64 boot configuration..."
  # ARM64 boot configuration
  sed -i.bak 's/^bootmodes=.*/bootmodes=("uefi.grub")/' "${PROFILEDEF}"
  sed -i.bak 's/^airootfs_image_tool_options=.*/airootfs_image_tool_options=("-comp" "xz" "-b" "1M" "-Xdict-size" "1M")/' "${PROFILEDEF}"
else
  echo "  Setting x86_64 boot configuration..."
  # x86_64 boot configuration
  sed -i.bak 's/^bootmodes=.*/bootmodes=("bios.syslinux" "uefi.grub")/' "${PROFILEDEF}"
  sed -i.bak 's/^airootfs_image_tool_options=.*/airootfs_image_tool_options=("-comp" "xz" "-Xbcj" "x86" "-b" "1M" "-Xdict-size" "1M")/' "${PROFILEDEF}"
fi

# Clean up backup files
rm -f "${PROFILEDEF}.bak"

# Ensure required bootloader config directories exist for selected boot modes
RELENG_PROFILE="/usr/share/archiso/configs/releng"
if [[ "${ARCH}" == "x86_64" ]]; then
  if [[ ! -d "${STAGED_PROFILE}/syslinux" ]]; then
    if [[ -d "${RELENG_PROFILE}/syslinux" ]]; then
      echo "Adding syslinux config from releng profile..."
      cp -a "${RELENG_PROFILE}/syslinux" "${STAGED_PROFILE}/syslinux"
    else
      echo "Error: Missing ${STAGED_PROFILE}/syslinux and releng syslinux template not found at ${RELENG_PROFILE}/syslinux" >&2
      exit 1
    fi
  fi
fi

if [[ ! -d "${STAGED_PROFILE}/grub" ]]; then
  if [[ -d "${RELENG_PROFILE}/grub" ]]; then
    echo "Adding grub config from releng profile..."
    cp -a "${RELENG_PROFILE}/grub" "${STAGED_PROFILE}/grub"
  else
    echo "Error: Missing ${STAGED_PROFILE}/grub and releng grub template not found at ${RELENG_PROFILE}/grub" >&2
    exit 1
  fi
fi


echo ""
echo "Starting mkarchiso build..."
echo "Command: mkarchiso -v -w ${WORK_DIR}/mkarchiso -o ${OUT_DIR} ${STAGED_PROFILE}"
echo ""

if ! mkarchiso -v -w "${WORK_DIR}/mkarchiso" -o "${OUT_DIR}" "${STAGED_PROFILE}"; then
  echo "Error: mkarchiso build failed" >&2
  echo "Last few lines of build output above ^"
  exit 1
fi

echo ""
echo "ISO build complete for ${ARCH}!"
echo "Output directory: ${OUT_DIR}"
echo ""
echo "Generated files:"
if ls -lh "${OUT_DIR}"/*.iso 2>/dev/null; then
  echo "✓ ISO build successful"
else
  echo "✗ Warning: No ISO files found in output directory"
  echo "Contents of ${OUT_DIR}:"
  ls -lh "${OUT_DIR}" || true
  exit 1
fi

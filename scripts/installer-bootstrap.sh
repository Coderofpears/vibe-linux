#!/usr/bin/env bash
set -euo pipefail

LOG_FILE="/var/log/vibe-installer-bootstrap.log"
INSTALLER="/usr/local/bin/vibe-installer"

exec > >(tee -a "${LOG_FILE}") 2>&1

echo "Starting Vibe-Linux live installer bootstrap..."

if [[ ! -x "${INSTALLER}" ]]; then
  echo "Installer not found at ${INSTALLER}." >&2
  exit 1
fi

if systemctl -q is-active NetworkManager; then
  echo "NetworkManager is active."
else
  echo "Starting NetworkManager..."
  systemctl start NetworkManager || true
fi

exec "${INSTALLER}"


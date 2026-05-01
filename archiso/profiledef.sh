#!/usr/bin/env bash
# shellcheck disable=SC2034

iso_name="vibe-linux"
iso_label="VIBE_LINUX_$(date +%Y%m)"
iso_publisher="Vibe-Linux OS <https://example.invalid/vibe-linux>"
iso_application="Vibe-Linux OS Installer"
iso_version="$(date +%Y.%m.%d)"
install_dir="arch"
buildmodes=("iso")
bootmodes=("bios.syslinux.mbr" "bios.syslinux.eltorito" "uefi-ia32.grub.esp" "uefi-x64.grub.esp")
arch="x86_64"
pacman_conf="pacman.conf"
airootfs_image_type="squashfs"
airootfs_image_tool_options=("-comp" "xz" "-Xbcj" "x86" "-b" "1M" "-Xdict-size" "1M")
file_permissions=(
  ["/etc/shadow"]="0:0:400"
  ["/root"]="0:0:750"
  ["/usr/local/bin/vibe-installer"]="0:0:755"
  ["/usr/local/bin/vibe-installer-bootstrap"]="0:0:755"
)


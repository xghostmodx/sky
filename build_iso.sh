#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ISO_ROOT="$SCRIPT_DIR/iso"
BOOT_DIR="$ISO_ROOT/boot"
GRUB_CFG="$BOOT_DIR/grub/grub.cfg"
ISO_OUTPUT="$SCRIPT_DIR/sky.iso"

function fail {
  echo "ERROR: $*" >&2
  exit 1
}

GRUB_MKRESCUE=""
if command -v grub-mkrescue >/dev/null 2>&1; then
  GRUB_MKRESCUE="grub-mkrescue"
elif command -v grub2-mkrescue >/dev/null 2>&1; then
  GRUB_MKRESCUE="grub2-mkrescue"
else
  fail "grub-mkrescue or grub2-mkrescue is required. Install grub2-common and xorriso."
fi

mkdir -p "$BOOT_DIR/grub"

if [ ! -f "$GRUB_CFG" ]; then
  cat > "$GRUB_CFG" <<'EOF'
set timeout=5
set default=0
menuentry "SKY OS (placeholder)" {
    echo "SKY OS ISO boots into GRUB."
    echo "Place vmlinuz and initrd.img into iso/boot to boot a real Linux kernel."
    sleep 5
}
EOF
fi

if [ ! -f "$BOOT_DIR/vmlinuz" ] || [ ! -f "$BOOT_DIR/initrd.img" ]; then
  cat <<'WARNING'
WARNING: No Linux kernel/initramfs files found in iso/boot.
This ISO will still be bootable into GRUB, but it cannot boot a full OS until you add:
  iso/boot/vmlinuz
  iso/boot/initrd.img

Copy a Linux kernel and initramfs from your system, then rerun ./build_iso.sh.
Example:
  cp /boot/vmlinuz-* iso/boot/vmlinuz
  cp /boot/initrd.img-* iso/boot/initrd.img
WARNING
fi

"$GRUB_MKRESCUE" -o "$ISO_OUTPUT" "$ISO_ROOT"

echo "Created bootable ISO: $ISO_OUTPUT"

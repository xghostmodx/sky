# Build a Bootable SKY OS ISO

This repository does not currently include a Linux kernel or initramfs image, so the ISO build scaffolding is provided here for a user-supplied kernel.

## Requirements

- `grub-mkrescue` or `grub2-mkrescue`
- `xorriso`
- A Linux kernel image (`vmlinuz`)
- A Linux initramfs (`initrd.img`)

## How to build

1. Copy your kernel and initramfs into `iso/boot/`:

```bash
mkdir -p iso/boot
cp /boot/vmlinuz-* iso/boot/vmlinuz
cp /boot/initrd.img-* iso/boot/initrd.img
```

2. Run the build script:

```bash
chmod +x ./build_iso.sh
./build_iso.sh
```

3. The resulting ISO will be written to `sky.iso`.

## Notes

- The current `grub.cfg` is a placeholder that boots GRUB and shows a menu entry.
- To make this a real bootable OS image, use a compatible Linux kernel and initramfs.
- You can customize `iso/boot/grub/grub.cfg` to add additional boot menu entries and kernel command-line options.

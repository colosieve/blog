+++
title = 'Framework 16 Keyboard HHKB Layout via VIA'
date = 2025-11-30T21:25:00Z
draft = false
tags = ['framework', 'keyboard', 'linux', 'via', 'hhkb']
author = 'colosieve'
+++

The Framework Laptop 16 keyboard supports remapping via [VIA](https://keyboard.frame.work), but Linux requires udev rules for browser access.

## Linux Permissions Fix

VIA communicates with the keyboard over USB HID. Without proper udev rules, you'll see:

```
NotAllowedError: Failed to open the device.
Received invalid protocol version from device
```

### Diagnosis

Check for existing rules:

```bash
cat /etc/udev/rules.d/*framework* 2>/dev/null
cat /etc/udev/rules.d/*qmk* 2>/dev/null
```

If empty, create the rules.

### Create udev Rules

```bash
sudo tee /etc/udev/rules.d/50-framework-keyboard.rules << 'EOF'
# Framework Laptop 16 Keyboard Module - ANSI
SUBSYSTEM=="hidraw", ATTRS{idVendor}=="32ac", ATTRS{idProduct}=="0012", MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="32ac", ATTRS{idProduct}=="0012", MODE="0666"
# Framework Laptop 16 Keyboard Module - Bootloader
SUBSYSTEM=="hidraw", ATTRS{idVendor}=="32ac", ATTRS{idProduct}=="0013", MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="32ac", ATTRS{idProduct}=="0013", MODE="0666"
EOF
```

Reload rules:

```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

## HHKB-Style Layout

The [Happy Hacking Keyboard](https://en.wikipedia.org/wiki/Happy_Hacking_Keyboard) layout optimizes for Unix users:

- **Control** on Caps Lock position (home row access)
- **Backspace** closer to home row
- **Fn layer** for navigation and F-keys

![Framework Keyboard HHKB Layout](/images/framework-keyboard-hhkb-layout.png)

Key remaps on Layer 0:

| Standard Key | HHKB Remap |
|--------------|------------|
| Caps Lock    | Left Ctrl  |
| Left Ctrl    | Caps Lock  |
| Left Win     | Left Alt   |
| Left Alt     | Left Win   |
| Backspace    | \\|        |
| \\|          | Backspace  |
| Right Alt    | Right Win  |
| Right Ctrl   | Right Alt  |
| ~`           | Esc        |
| Insert (Del) | ~`         |

Layer 1 provides F-keys, navigation (Home/End/PgUp/PgDn), and media controls.

## Import Configuration

This exact configuration is saved and directly importable:

1. Open [keyboard.frame.work](https://keyboard.frame.work)
2. Authorize the keyboard device
3. Go to **Settings** (gear icon) → **Load Saved Layout**
4. Import: [framework-keyboard-hhkb.json](/files/framework-keyboard-hhkb.json)

Changes save directly to keyboard EEPROM—no software needed after configuration.

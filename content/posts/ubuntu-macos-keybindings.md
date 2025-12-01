+++
title = "HHKB Layout and macOS-Style Keybindings on Ubuntu 24.04"
date = 2025-12-01T12:00:00-08:00
draft = false
toc = true
+++

If you're coming from macOS, the muscle memory for Cmd+C/V/X is hard to break. Or if you've used [Omarchy](https://omarchy.com/), you'll find how the remap makes total sense given today's terminal-focused trend reversal. This post shows how to set up macOS-style keybindings on Ubuntu 24.04 using a two-layer approach:

1. **keyd**  -  low-level keyboard remapping (remap internal laptop keyboard to HHKB layout)
2. **xremap**  -  application-aware Super→Ctrl shortcuts

## The Problem

The naive solution of swapping Alt and Super in GNOME settings doesn't work because:
- GNOME intercepts Super key presses for the Activities overview
- Terminals need Ctrl+C for SIGINT, not copy
- Some apps (like Chrome) don't respect GTK keybinding overrides

## Install keyd

keyd runs at the kernel level, remapping keys before they reach the desktop.

```bash
# Install dependencies
sudo apt install build-essential git

# Clone and build
cd ~/dev
git clone https://github.com/rvaiya/keyd
cd keyd
make
sudo make install

# Enable service
sudo systemctl enable keyd
sudo systemctl start keyd
```

## Configure keyd

Create `/etc/keyd/default.conf`:

```ini
[ids]
*

[main]
capslock = leftcontrol
leftcontrol = capslock
leftmeta = leftalt
leftalt = leftmeta
rightalt = rightmeta
rightcontrol = rightalt
```

This swaps:
- **Caps Lock ↔ Left Ctrl**  -  Caps Lock becomes a useful key
- **Left Meta ↔ Left Alt**  -  Super key moves next to spacebar (macOS position)
- **Right Alt → Right Meta**  -  Consistent right side
- **Right Ctrl → Right Alt**  -  Free up for compose/AltGr

Reload after changes:

```bash
sudo keyd reload
```

### Internal Keyboard Only

If you use an external keyboard with a different layout, target only the internal keyboard:

```bash
# Find your keyboard ID
sudo keyd -m
# Press keys on internal keyboard, note the ID (e.g., 0001:0001)
```

Create `/etc/keyd/internal.conf` with specific IDs:

```ini
[ids]
0001:0001

[main]
capslock = leftcontrol
leftcontrol = capslock
backslash = backspace
backspace = backslash
grave = esc
delete = grave
leftmeta = leftalt
leftalt = leftmeta
rightalt = rightmeta
rightcontrol = rightalt
```

Additional HHKB-style mappings:
- **Backslash ↔ Backspace**  -  Backspace moves to a more accessible position
- **Delete → Grave/tilde**  -  Grave moves to Delete key position
- **Grave/tilde → Escape**  -  Escape at top-left corner

## Install xremap

xremap provides application-aware key remapping. It can remap Super+C to Ctrl+C everywhere except terminals.

```bash
# Install Rust if needed
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env

# Install xremap with GNOME support
cargo install xremap --features gnome
```

### udev Rules

xremap needs access to input devices:

```bash
# Add user to input group
sudo usermod -aG input $USER

# Create udev rule
echo 'KERNEL=="uinput", GROUP="input", MODE="0660"' | \
  sudo tee /etc/udev/rules.d/99-uinput.rules

# Reload rules
sudo udevadm control --reload-rules
sudo udevadm trigger
```

Log out and back in for group changes to take effect.

### Create Config Directory

```bash
mkdir -p ~/.config/xremap
```

### GNOME Shell Extension

For app-specific remapping, xremap needs to know which app is focused. Install the GNOME extension:

```bash
# Clone extension
mkdir -p ~/.local/share/gnome-shell/extensions
cd ~/.local/share/gnome-shell/extensions
git clone https://github.com/xremap/xremap-gnome.git xremap@k0kubun.com

# Enable it
gnome-extensions enable xremap@k0kubun.com
```

You may need to restart GNOME Shell (log out/in or Alt+F2, type `r`, Enter on X11).

## Configure xremap

Create `~/.config/xremap/config.yml`:

```yaml
keymap:
  - name: Super clipboard for all apps except terminals
    application:
      not:
        - gnome-terminal
        - gnome-terminal-server
        - Gnome-terminal
        - ghostty
        - com.mitchellh.ghostty
        - kitty
        - alacritty
    remap:
      Super-c: C-c
      Super-v: C-v
      Super-x: C-x
      Super-a: C-a
      Super-z: C-z
      Super-Shift-z: C-Shift-z
```

This maps Super+C/V/X/A/Z to their Ctrl equivalents, except in terminal emulators where Ctrl+C means interrupt.

## Create xremap Service

Create `~/.config/systemd/user/xremap.service`:

```ini
[Unit]
Description=xremap key remapper
After=graphical-session.target

[Service]
ExecStart=%h/.cargo/bin/xremap %h/.config/xremap/config.yml
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
```

Enable and start:

```bash
systemctl --user daemon-reload
systemctl --user enable xremap
systemctl --user start xremap
```

## GNOME Settings

I moved away Super key mapping from GNOME - this should be optional, but who knows :-)

GNOME intercepts Super key by default. Disable these behaviors:

```bash
# Prevent Super from opening Activities
gsettings set org.gnome.mutter overlay-key ''

# Or remap to a different key
gsettings set org.gnome.mutter overlay-key 'Alt_R'

# Disable mouse-button-modifier (interferes with Super+click)
gsettings set org.gnome.desktop.wm.preferences mouse-button-modifier ''

# Disable message tray shortcut
gsettings set org.gnome.shell.keybindings toggle-message-tray '[]'
```

## Terminal Clipboard Shortcuts

Terminals excluded from xremap need native Super+C/V bindings:

**GNOME Terminal:** Edit → Preferences → Shortcuts

**Ghostty** (`~/.config/ghostty/config`):
```
keybind = super+c=copy_to_clipboard
keybind = super+v=paste_from_clipboard
```

**Kitty** (`~/.config/kitty/kitty.conf`):
```
map super+c copy_to_clipboard
map super+v paste_from_clipboard
```

## Troubleshooting

### xremap not detecting apps

Check if the GNOME extension is working:

```bash
gdbus call --session \
  --dest org.gnome.Shell \
  --object-path /com/k0kubun/Xremap \
  --method com.k0kubun.Xremap.ActiveWindow
```

Should return the current window's WM_CLASS.

### keyd not working

```bash
# Check service status
sudo systemctl status keyd

# Test interactively
sudo keyd -m
# Press keys and verify output
```

### Super key still opens Activities

```bash
# Verify setting
gsettings get org.gnome.mutter overlay-key
# Should be '' or your chosen alternative
```

## What Didn't Work

**GTK CSS keybindings**: GTK3's `-gtk-key-bindings` CSS property was removed in GTK4. Even for GTK3, Chrome ignores it.

**input-remapper**: GUI tool that works but lacks app-specific remapping. keyd + xremap is more flexible.

**GNOME Tweaks**: Can swap Alt/Super globally but doesn't help with the Super+C → Ctrl+C translation.

## Summary

| Layer | Tool | Purpose |
|-------|------|---------|
| Kernel | keyd | Physical key swaps (Caps↔Ctrl, Meta↔Alt), HHKB layout |
| User | xremap | Super→Ctrl translation, app-specific rules |
| App | Native config | Terminal Super+C/V bindings |
| Desktop | gsettings | Disable GNOME Super key interception |

After this setup, your muscle memory from macOS just works: Super+C copies, Super+V pastes, and terminals still get Ctrl+C for interrupt.

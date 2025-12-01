+++
title = 'Framework 16 LED Matrix Rain Effect'
date = 2025-12-01T00:00:00Z
draft = false
tags = ['framework', 'led', 'linux', 'python']
author = 'colosieve'
+++

The Framework 16 supports LED Matrix spacer modules that can be programmed via USB serial. This post covers the protocol and a Matrix-style digital rain effect.

## Hardware

- Two LED Matrix spacer modules (9x34 pixels each, 306 LEDs per module)
- Connected via USB serial at `/dev/ttyACM0` and `/dev/ttyACM1`
- Vendor ID: `0x32AC`, Product ID: `0x0020`

## Protocol

```
Magic header: [0x32, 0xAC]
Commands:
  0x00 - Set brightness
  0x06 - Draw binary frame (39 bytes, all 306 LEDs as bits)
  0x07 - Stage greyscale column (col_index + 34 brightness values)
  0x08 - Commit staged buffer to display
Baud rate: 115200
```

## Programming Examples

### Basic Connection

```python
import serial

device = "/dev/ttyACM0"
ser = serial.Serial(device, 115200, timeout=1)

FWK_MAGIC = bytes([0x32, 0xAC])
```

### Set Global Brightness (0-255)

```python
CMD_BRIGHTNESS = 0x00
ser.write(FWK_MAGIC + bytes([CMD_BRIGHTNESS, 128]))
```

### Stage a Column (greyscale)

```python
CMD_STAGE_GREY_COL = 0x07

col = 0  # Column index 0-8
brightness_values = [255] * 34  # 34 rows, all max brightness

ser.write(FWK_MAGIC + bytes([CMD_STAGE_GREY_COL, col] + brightness_values))
```

### Commit Staged Buffer to Display

```python
CMD_DRAW_GREY_COL_BUFFER = 0x08
ser.write(FWK_MAGIC + bytes([CMD_DRAW_GREY_COL_BUFFER, 0x00]))
```

### Full Frame Render

```python
def render_frame(ser, frame):
    """frame = 2D list [9 cols][34 rows] of brightness values 0-255"""
    for col in range(9):
        cmd = bytes([CMD_STAGE_GREY_COL, col] + frame[col])
        ser.write(FWK_MAGIC + cmd)
    ser.write(FWK_MAGIC + bytes([CMD_DRAW_GREY_COL_BUFFER, 0x00]))
    ser.flush()
```

### Clear Display

```python
frame = [[0] * 34 for _ in range(9)]
render_frame(ser, frame)
```

## How Matrix Rain Works

### Data Structures

```python
# Frame buffer: 9 columns x 34 rows of brightness values
frame = [[0] * 34 for _ in range(9)]

# Drops: list of [column, row, brightness, speed]
drops = [
    [3, 5.0, 255, 1.2],   # Drop in column 3, row 5, full bright, speed 1.2
    [7, 12.5, 255, 0.8],  # Drop in column 7, row 12.5, speed 0.8
]
```

### Algorithm (each frame)

```
1. FADE existing pixels
   └─ For each pixel: brightness = max(0, brightness - 15)

2. UPDATE drops
   └─ For each drop:
      ├─ Move down: row += speed
      ├─ Draw head: frame[col][row] = 255 (full bright)
      ├─ Draw trail: 5 pixels above head with decreasing brightness
      │   └─ trail_brightness = 255 - (i * 40) for i in 1..5
      └─ If row >= 34: respawn at top with random column/speed

3. SPAWN new drops
   └─ 10% chance each frame to add a new drop

4. RENDER frame to LED matrix
   └─ Stage all 9 columns, then commit buffer
```

### Trail Effect Visualization

```
Row:  Brightness:
 5    ████████ 255  ← Drop head (brightest)
 4    ██████   215  ← Trail
 3    ████     175
 2    ███      135
 1    ██        95
 0    █         55  ← Trail fades out
```

### Frame Timing

- Speed: 0.02 seconds between frames = 50 FPS
- Drop speed: 0.5 to 2.0 rows per frame (randomized per drop)

## Performance Optimization: DrawBW Mode

### Before (Greyscale mode - CMD 0x07/0x08)

- 10 serial writes per frame: 9 StageGreyCol (0x07) + 1 FlushCols (0x08)
- Each write requires USB round-trip latency (~5ms)
- Result: ~6 FPS

### After (Binary mode - CMD 0x06)

- 1 serial write per frame: single DrawBW (0x06) command
- All 306 LEDs packed as bits into 39 bytes
- Result: ~30+ FPS

### Code Change

```python
# Old: 10 writes per frame
for col in range(9):
    send(0x07, col, values[col])  # Stage column
send(0x08, 0x00)                  # Commit

# New: 1 write per frame
vals = [0] * 39
for x in range(9):
    for y in range(34):
        if frame[x][y] > threshold:
            i = x + 9 * y
            vals[i // 8] |= 1 << (i % 8)
send(0x06, vals)  # Single command
```

### Trade-off

- Lost: Variable brightness (greyscale)
- Gained: ~5x frame rate improvement
- No `flush()` needed with single-command writes
- For matrix rain effect, binary on/off still looks good

## Linux Setup

### Udev Rules

Grant access to the LED matrix devices:

```bash
sudo tee /etc/udev/rules.d/50-framework-ledmatrix.rules << 'EOF'
SUBSYSTEM=="tty", ATTRS{idVendor}=="32ac", ATTRS{idProduct}=="0020", MODE="0666"
EOF

sudo udevadm control --reload-rules && sudo udevadm trigger
```

### Install Dependencies

```bash
sudo pacman -S python-pyserial
```

### Install Script

Download: [fw16-led-matrix-rain.py](/files/fw16-led-matrix-rain.py)

```bash
sudo cp fw16-led-matrix-rain.py /usr/local/bin/fw16-led-matrix-rain
sudo chmod +x /usr/local/bin/fw16-led-matrix-rain
```

### Systemd Service

```bash
sudo tee /etc/systemd/system/fw16-led-matrix-rain.service << 'EOF'
[Unit]
Description=Framework 16 LED Matrix Rain Effect
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /usr/local/bin/fw16-led-matrix-rain --brightness 128 --speed 0.02
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable fw16-led-matrix-rain
sudo systemctl start fw16-led-matrix-rain
```

## Service Management

```bash
systemctl status fw16-led-matrix-rain       # Check status
sudo systemctl stop fw16-led-matrix-rain    # Stop
sudo systemctl start fw16-led-matrix-rain   # Start
sudo systemctl restart fw16-led-matrix-rain # Restart
sudo systemctl disable fw16-led-matrix-rain # Disable on boot
```

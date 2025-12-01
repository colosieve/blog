#!/usr/bin/env python3
"""
Framework 16 LED Matrix - Matrix Rain Effect
Displays a "digital rain" effect on both LED matrix spacers.

Usage: fw16-led-matrix-rain [--speed SPEED] [--brightness BRIGHTNESS] [--clear-interval SECONDS]

Requirements: pyserial (pip install pyserial)
"""

import serial
import time
import random
import argparse
from typing import List

# LED Matrix dimensions
COLS = 9
ROWS = 34

# Protocol constants
FWK_MAGIC = bytes([0x32, 0xAC])
CMD_BRIGHTNESS = 0x00
CMD_DRAW_BW = 0x06  # Single command for all 306 LEDs as bits

# Default serial devices for left and right LED matrices
DEFAULT_DEVICES = ["/dev/ttyACM0", "/dev/ttyACM1"]


class LEDMatrix:
    def __init__(self, device: str, brightness: int = 200, threshold: int = 64):
        self.device = device
        self.brightness = brightness
        self.threshold = threshold  # Brightness threshold for on/off
        self.serial = None

    def connect(self):
        try:
            self.serial = serial.Serial(self.device, 115200, timeout=1)
            self.set_brightness(self.brightness)
            return True
        except Exception as e:
            print(f"Failed to connect to {self.device}: {e}")
            return False

    def disconnect(self):
        if self.serial:
            self.serial.close()

    def send_command(self, cmd: bytes):
        if self.serial:
            self.serial.write(FWK_MAGIC + cmd)

    def set_brightness(self, level: int):
        """Set global brightness (0-255)"""
        self.send_command(bytes([CMD_BRIGHTNESS, level]))

    def render_frame(self, frame: List[List[int]]):
        """Render a full frame using DrawBW - single command for all 306 LEDs"""
        # Pack 306 LEDs into 39 bytes (306 bits)
        # Bit layout: LED[x,y] = bit (x + 9*y)
        vals = [0] * 39
        for x in range(COLS):
            for y in range(ROWS):
                if frame[x][y] > self.threshold:
                    i = x + COLS * y
                    vals[i // 8] |= 1 << (i % 8)
        self.send_command(bytes([CMD_DRAW_BW] + vals))

    def clear(self):
        """Clear the display"""
        self.send_command(bytes([CMD_DRAW_BW] + [0] * 39))


class MatrixRain:
    def __init__(self, max_brightness: int = 255):
        self.max_brightness = max_brightness
        self.drops = []
        self.frame = [[0] * ROWS for _ in range(COLS)]

        # Initialize random drops
        for _ in range(COLS * 2):
            self.spawn_drop()

    def spawn_drop(self):
        col = random.randint(0, COLS - 1)
        row = random.randint(-ROWS, 0)
        speed = random.uniform(0.5, 2.0)
        self.drops.append([col, float(row), self.max_brightness, speed])

    def reset(self):
        """Clear frame and reset drops"""
        self.frame = [[0] * ROWS for _ in range(COLS)]
        self.drops = []
        for _ in range(COLS * 2):
            self.spawn_drop()

    def update(self):
        # Fade existing pixels
        for col in range(COLS):
            for row in range(ROWS):
                if self.frame[col][row] > 0:
                    self.frame[col][row] = max(0, self.frame[col][row] - 15)

        # Update drops
        new_drops = []
        for drop in self.drops:
            col, row, brightness, speed = drop
            row += speed

            if row < ROWS:
                # Draw the drop head (bright)
                if 0 <= int(row) < ROWS:
                    self.frame[col][int(row)] = brightness

                # Draw trail (fading)
                for i in range(1, 6):
                    trail_row = int(row) - i
                    if 0 <= trail_row < ROWS:
                        trail_brightness = max(0, brightness - (i * 40))
                        self.frame[col][trail_row] = max(
                            self.frame[col][trail_row],
                            trail_brightness
                        )

                drop[1] = row
                new_drops.append(drop)
            else:
                # Respawn at top
                self.spawn_drop()

        self.drops = new_drops

        # Occasionally spawn new drops
        if random.random() < 0.1:
            self.spawn_drop()

        return self.frame


def main():
    parser = argparse.ArgumentParser(description="Matrix Rain effect for Framework 16 LED Matrix")
    parser.add_argument("--speed", type=float, default=0.02, help="Frame delay in seconds")
    parser.add_argument("--brightness", type=int, default=128, help="Max brightness (0-255)")
    parser.add_argument("--clear-interval", type=int, default=30, help="Clear and reset every N seconds (0 to disable)")
    parser.add_argument("--devices", nargs="+", default=DEFAULT_DEVICES, help="Serial devices")
    args = parser.parse_args()

    # Calculate clear interval in frames (DrawBW mode ~30+ FPS)
    clear_every_n_frames = int(args.clear_interval * 30) if args.clear_interval > 0 else 0

    # Connect to LED matrices
    matrices = []
    for device in args.devices:
        matrix = LEDMatrix(device, args.brightness)
        if matrix.connect():
            matrices.append(matrix)

    if not matrices:
        print("No LED matrices found!")
        return 1

    # Create rain effect for each matrix
    rains = [MatrixRain(args.brightness) for _ in matrices]

    frame_count = 0

    try:
        while True:
            frame_count += 1

            # Clear and reset periodically
            if clear_every_n_frames > 0 and frame_count >= clear_every_n_frames:
                frame_count = 0
                for matrix, rain in zip(matrices, rains):
                    rain.reset()
                    matrix.clear()

            # Render each matrix
            for matrix, rain in zip(matrices, rains):
                frame = rain.update()
                matrix.render_frame(frame)

            time.sleep(args.speed)
    except KeyboardInterrupt:
        pass
    finally:
        for matrix in matrices:
            matrix.clear()
            matrix.disconnect()

    return 0


if __name__ == "__main__":
    exit(main())

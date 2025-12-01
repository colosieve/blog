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
CMD_STAGE_GREY_COL = 0x07
CMD_DRAW_GREY_COL_BUFFER = 0x08
CMD_BRIGHTNESS = 0x00

# Default serial devices for left and right LED matrices
DEFAULT_DEVICES = ["/dev/ttyACM0", "/dev/ttyACM1"]


class LEDMatrix:
    def __init__(self, device: str, brightness: int = 200):
        self.device = device
        self.brightness = brightness
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
            self.serial.flush()

    def set_brightness(self, level: int):
        """Set global brightness (0-255)"""
        self.send_command(bytes([CMD_BRIGHTNESS, level]))

    def stage_column(self, col: int, values: List[int]):
        """Stage a single column of brightness values"""
        cmd = bytes([CMD_STAGE_GREY_COL, col] + values[:ROWS])
        self.send_command(cmd)

    def draw(self):
        """Commit staged columns to display"""
        self.send_command(bytes([CMD_DRAW_GREY_COL_BUFFER, 0x00]))

    def render_frame(self, frame: List[List[int]]):
        """Render a full frame (9 cols x 34 rows)"""
        for col in range(COLS):
            self.stage_column(col, frame[col])
        self.draw()

    def clear(self):
        """Clear the display"""
        frame = [[0] * ROWS for _ in range(COLS)]
        self.render_frame(frame)


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

    # Calculate clear interval in frames (assuming ~6 FPS actual)
    clear_every_n_frames = int(args.clear_interval * 6) if args.clear_interval > 0 else 0

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

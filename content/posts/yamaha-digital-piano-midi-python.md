+++
title = "Yamaha Digital Piano MIDI Monitor in Python"
date = 2026-01-03T00:00:00Z
author = "colosieve"
tags = ["python", "midi", "music", "yamaha"]
+++

Simple Python script to receive MIDI signals from a Yamaha Digital Piano (or any USB MIDI device) and print them to the console.

## Setup

Install the required packages:

```bash
pip3 install mido python-rtmidi
```

## The Script

```python
#!/usr/bin/env python3
"""Simple MIDI monitor - prints incoming MIDI messages to console."""

import mido

def list_ports():
    """List available MIDI input ports."""
    ports = mido.get_input_names()
    if not ports:
        print("No MIDI input ports found.")
        return None

    print("Available MIDI input ports:")
    for i, port in enumerate(ports):
        print(f"  [{i}] {port}")
    return ports

def monitor_midi(port_name=None):
    """Monitor MIDI input and print messages."""
    ports = list_ports()
    if not ports:
        print("\nPlug in your MIDI device and try again.")
        return

    # Auto-select Yamaha if found, otherwise use first port or specified
    if port_name is None:
        yamaha_ports = [p for p in ports if 'yamaha' in p.lower() or 'digital piano' in p.lower()]
        if yamaha_ports:
            port_name = yamaha_ports[0]
        else:
            port_name = ports[0]

    print(f"\nOpening: {port_name}")
    print("Listening for MIDI messages... (Ctrl+C to quit)\n")

    try:
        with mido.open_input(port_name) as inport:
            for msg in inport:
                print(msg)
    except KeyboardInterrupt:
        print("\nStopped.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    port = sys.argv[1] if len(sys.argv) > 1 else None
    monitor_midi(port)
```

## Usage

```bash
python3 midi_monitor.py
```

Or specify a port:

```bash
python3 midi_monitor.py "Digital Piano"
```

## Sample Output

When playing keys or using pedals:

```
note_on channel=0 note=60 velocity=64 time=0
note_off channel=0 note=60 velocity=0 time=0
control_change channel=0 control=64 value=127 time=0
```

## USB Detection

Check if the piano is connected:

```bash
lsusb | grep -i yamaha
# Bus 001 Device 013: ID 0499:1718 Yamaha Corp. Digital Piano
```

## Notes

- The Yamaha Digital Piano shows up as USB device ID `0499:1718`
- `mido` with `python-rtmidi` backend handles ALSA MIDI on Linux
- MIDI note 60 = Middle C
- Control 64 = sustain pedal

# Bungee Biker

A 1:1 clone of the classic game Elasto Mania - now with full macOS app support!

## Quick Start

### Run from Source

```bash
pip install -r requirements.txt
python main.py
```

### Build macOS Application

```bash
./build_macos.sh
```

This creates a standalone macOS app that you can double-click to run. See [BUILD_MACOS.md](BUILD_MACOS.md) for detailed instructions.

## Controls

- **Up Arrow**: Accelerate
- **Down Arrow**: Brake
- **Left Arrow**: Rotate counter-clockwise
- **Right Arrow**: Rotate clockwise
- **Space**: Turn around
- **R**: Restart level
- **1/2**: Switch test levels
- **ESC**: Quit

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Player quick start guide
- **[BUILD_MACOS.md](BUILD_MACOS.md)** - macOS app build instructions
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Developer documentation
- **[PRD_BUNGEE_BIKER.md](PRD_BUNGEE_BIKER.md)** - Complete product requirements

## Development Status

✅ **Phase 1: Core Engine - COMPLETE**

Working features:
- Elastic bike physics
- 2 test levels
- Apple collection
- Rotating killers
- Timer and UI
- macOS app packaging

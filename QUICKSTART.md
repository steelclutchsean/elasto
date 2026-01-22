# Bungee Biker - Quick Start Guide

## What is Bungee Biker?

Bungee Biker is a 1:1 recreation of the classic 2000 game **Elasto Mania**. It's a physics-based motorcycle platformer where you control an elastic bike through challenging levels, collecting apples and reaching the goal flower.

## Installation

### Quick Install

```bash
# 1. Make sure you have Python 3.8+ installed
python --version

# 2. Install dependencies
pip install pygame numpy

# 3. Run the game!
python main.py
```

### Using requirements.txt

```bash
pip install -r requirements.txt
python main.py
```

## How to Play

### Objective
- Collect all **apples** (red circles)
- Touch the **flower** (gold star) to complete the level
- Avoid hitting your **head** or **wheels** on obstacles
- Complete levels as fast as possible!

### Controls

```
Arrow Keys:
  ↑ UP    = Accelerate (rear-wheel drive)
  ↓ DOWN  = Brake
  ← LEFT  = Rotate counter-clockwise (lean back)
  → RIGHT = Rotate clockwise (lean forward)

Space     = Turn around (180° flip)
R         = Restart level
1 / 2     = Switch test levels
ESC       = Quit game
```

### Advanced Techniques

**Supervolt**: Press LEFT + RIGHT together for faster clockwise rotation (original Elma bug/feature)

**Balance**: The bike has realistic elastic physics - you must balance weight distribution

**Air Control**: Rotate in the air to prepare for landing angles

## Game Mechanics

### Death Conditions ☠️
You crash and restart if:
- Your **head** touches any wall or ground
- Your **head** or **wheels** touch a **killer** (spiky rotating ball)

### Safe Zones ✓
Your body can pass through walls safely - only head and wheels collide!

### Completion
- All apples must be collected before the flower unlocks
- Touch the flower to complete
- Your time is shown on completion

## Current Features ✅

- Authentic elastic bike physics
- 2 test levels (more coming soon!)
- Apple collection system
- Rotating killer obstacles
- Precise timer (minutes:seconds:hundredths)
- Smooth camera following
- Death and completion detection
- Instant restart

## Tips for New Players

1. **Start Slow**: The bike is very sensitive - small inputs are key
2. **Use Rotation**: Lean forward to accelerate downhill, lean back when climbing
3. **Watch Your Head**: Most deaths come from hitting your head on ceilings
4. **Landing Angle**: Try to land with both wheels touching simultaneously
5. **Practice**: The physics take time to master - that's the fun!

## Test Levels

### Level 1: Flat Track
Simple flat ground for learning basic controls and physics feel.
- Press `1` to load
- Good for: Testing acceleration, braking, basic jumping

### Level 2: Test Level
More complex terrain with obstacles, ramps, and a killer.
- Press `2` to load (default)
- Good for: Learning advanced techniques

## Troubleshooting

### Game won't start
```bash
# Install pygame
pip install pygame

# Or try
pip install pygame==2.5.2
```

### Low frame rate
- Close other applications
- The game targets 60 FPS but physics runs at 30 FPS internally

### Controls not responsive
- Make sure game window has focus
- Try pressing ESC and restarting

## What's Next?

This is an early prototype (Phase 1). Coming soon:
- All 54 original Elasto Mania levels
- Replay recording and playback
- Level editor
- Better graphics and sounds
- Multiplayer
- Online leaderboards

## Development Status

**Current Phase**: 1 - Core Engine ✅ COMPLETE

The physics engine, rendering system, and basic gameplay are fully functional!

**Next Phase**: 2 - Level Recreation (recreating all 54 original levels)

## Resources

- Full PRD: See `PRD_BUNGEE_BIKER.md`
- Development Guide: See `DEVELOPMENT.md`
- GitHub: [Your repo URL]

## Feedback

Found a bug? Have suggestions? Want to contribute?
- Open an issue
- Submit a pull request
- Join our community

---

**Have fun and enjoy the elastic physics!** 🏍️

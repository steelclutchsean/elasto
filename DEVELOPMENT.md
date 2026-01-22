# Bungee Biker - Development Guide

## Project Structure

```
elasto/
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── PRD_BUNGEE_BIKER.md    # Product Requirements Document
├── src/
│   ├── engine/            # Core engine components
│   │   ├── physics.py     # Physics engine (mass-spring-damper)
│   │   └── renderer.py    # Rendering system
│   └── game/              # Game logic
│       ├── game.py        # Main game class
│       ├── level.py       # Level management
│       └── objects.py     # Game objects (apple, flower, killer)
└── assets/                # Game assets (future)
    ├── sprites/
    ├── sounds/
    └── levels/
```

## Development Setup

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

## Architecture Overview

### Physics System

The physics engine (`src/engine/physics.py`) is the heart of the game:

- **Mass-Spring-Damper Model**: Wheels connected to bike center via springs
- **Fixed Timestep**: 30 FPS physics updates for deterministic replays
- **Collision Detection**: Sphere-to-line segment for wheels and head
- **Spring Forces**: Tunable constants for authentic Elma feel

Key classes:
- `Vec2`: 2D vector math
- `Line`: Terrain line segment with collision helpers
- `Wheel`: Individual wheel physics
- `Bike`: Complete bike physics model

### Rendering System

The renderer (`src/engine/renderer.py`) handles all visuals:

- **Camera**: Smooth following with configurable zoom
- **Coordinate Conversion**: World space ↔ Screen space
- **Drawing**: Terrain, bike, objects, UI

Key classes:
- `Camera`: View management
- `Renderer`: All drawing operations
- `Colors`: Centralized color palette

### Game Objects

Game objects (`src/game/objects.py`) are simple entities:

- `Apple`: Collectible items
- `Flower`: Goal/exit object
- `Killer`: Rotating spike obstacles

### Level System

Levels (`src/game/level.py`) contain:

- Terrain (list of Line segments)
- Objects (apples, flower, killers)
- Start position
- Level state (time, completion)

### Game Loop

The main game (`src/game/game.py`) manages:

- Input handling
- Fixed timestep physics updates
- State management (playing, dead, completed)
- Integration of all systems

## Physics Tuning

To match Elasto Mania's feel, tune these constants in `PhysicsConstants`:

```python
GRAVITY = 9.81 * 2.0           # Overall gravity strength
WHEEL_SPRING_K = 800.0         # Wheel suspension stiffness
WHEEL_DAMPING_C = 80.0         # Wheel suspension damping
ACCELERATION_FORCE = 35.0      # Acceleration power
ROTATION_TORQUE = 12.0         # Rotation speed
BRAKE_FRICTION = 0.95          # Braking power
```

**Testing Process:**
1. Load flat level (press `1`)
2. Test basic riding feel
3. Test jumping and landing
4. Test rotation responsiveness
5. Adjust constants and repeat

## Controls

### In-Game
- **Arrow Keys**: Accelerate, brake, rotate
- **Space**: Turn around (180° flip)
- **R**: Restart level
- **1/2**: Switch between test levels
- **ESC**: Quit

### Development
- Modify `create_test_level()` in `level.py` to test different scenarios
- Adjust camera zoom in `Camera.__init__()` for different views
- Change `PhysicsConstants` for physics experiments

## Adding New Levels

Create a new level function in `src/game/level.py`:

```python
def create_my_level() -> Level:
    level = Level("My Level Name")

    # Set start position
    level.start_position = Vec2(x, y)

    # Add terrain
    level.terrain.append(Line(Vec2(x1, y1), Vec2(x2, y2)))
    level.is_ground.append(True)  # or False for walls

    # Add objects
    level.apples.append(Apple(Vec2(x, y)))
    level.flower = Flower(Vec2(x, y))
    level.killers.append(Killer(Vec2(x, y)))

    return level
```

Then load it in `game.py` with a key binding.

## Next Steps (Phase 2+)

### Immediate Priorities
1. **Physics Tuning**: Match Elasto Mania feel exactly
2. **Level Recreation**: Start recreating original 54 levels
3. **LEV File Parser**: Load original .lev files
4. **Better Graphics**: Import or create proper sprites

### Future Features
- Replay recording (.rec files)
- Level editor UI
- Sound effects
- Multiplayer
- Leaderboards

## Debugging Tips

### Physics Issues
- Enable debug rendering: Draw spring connections, velocity vectors
- Log collision events
- Slow down physics with larger timestep visualization

### Collision Problems
- Draw collision circles for wheels/head
- Highlight terrain normals
- Log penetration depths

### Performance
- Profile with cProfile: `python -m cProfile main.py`
- Monitor frame times
- Check physics update count per frame

## Code Style

- Follow PEP 8
- Type hints for function signatures
- Docstrings for classes and complex functions
- Comments for non-obvious physics/math

## Testing

Currently manual testing only. Future:
- Unit tests for physics (determinism)
- Integration tests for levels
- Replay validation tests

## Resources

See `PRD_BUNGEE_BIKER.md` for complete specifications and reference links.

## Contributing

1. Create feature branch from `claude/elasto-mania-prd-3PdUP`
2. Implement feature
3. Test thoroughly
4. Commit with clear message
5. Push and create PR

## Known Issues

- Physics not yet perfectly tuned to Elasto Mania
- No proper sprites (using simple shapes)
- No sound effects
- Limited test levels
- No replay system yet

## License

TBD - See PRD for legal considerations regarding Elasto Mania IP

# Product Requirements Document: Bungee Biker
## A 1:1 Clone of Elasto Mania

**Version:** 1.0
**Date:** January 22, 2026
**Status:** Initial Draft

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Game Overview](#game-overview)
3. [Core Gameplay Mechanics](#core-gameplay-mechanics)
4. [Physics Engine](#physics-engine)
5. [Controls and Input](#controls-and-input)
6. [Level Design](#level-design)
7. [Graphics System](#graphics-system)
8. [Audio System](#audio-system)
9. [Game Objects](#game-objects)
10. [User Interface](#user-interface)
11. [Replay System](#replay-system)
12. [Multiplayer](#multiplayer)
13. [Level Editor](#level-editor)
14. [File Formats](#file-formats)
15. [Technical Specifications](#technical-specifications)
16. [Development Roadmap](#development-roadmap)

---

## Executive Summary

**Bungee Biker** is a 1:1 recreation of the classic 2000 indie motorbike simulation game Elasto Mania (also known as Elma). The game is a colorful 2D physics-based racing experience that emphasizes delicate balance, skill, and style. Players control an elastic motorcycle through 54 increasingly challenging levels, collecting apples and reaching the finish flower while avoiding deadly obstacles.

The core appeal lies in the emergent complexity that arises from the interaction between a brutally unforgiving physics engine and thoughtfully designed levels. The game has maintained an active competitive community for over two decades, with players continuously setting new world records measured to hundredths of a second.

---

## Game Overview

### Game Concept
Bungee Biker explores the notion of elastic motorcycles in a 2D platformer environment. The goal is to navigate through tricky terrain while controlling speed, balancing tilt, and collecting items. The game is fun to play yet challenging to master, with a steep difficulty curve that rewards precision and mastery.

### Target Audience
- Retro gaming enthusiasts
- Physics-based platformer fans
- Speedrunning community
- Players who enjoy skill-based challenges
- Competitive players focused on time trials

### Core Pillars
1. **Precision Physics** - Highly responsive, deterministic physics simulation
2. **Skill Mastery** - Deep mechanics that reward practice and precision
3. **Level Variety** - 54 hand-crafted levels ranging from simple to brutally difficult
4. **Competitive Play** - Time trial focus with replay sharing and world records
5. **Community Content** - Robust level editor for infinite replayability

---

## Core Gameplay Mechanics

### Primary Objective
Touch the flower object to complete each level. Some levels require collecting all apples before the flower becomes accessible.

### Win/Fail Conditions

**Win Condition:**
- Collect all apples in the level (if any)
- Touch the flower object

**Fail Conditions (Force Restart):**
- Player's head touches any solid structure (walls, ceiling, floor)
- Player's head OR bike wheels touch a rotating killer (spiky wheel)
- Player falls off map boundaries (if applicable)

**Important:** Only the rider's head and both wheels interact with collision geometry. The rider's body can overlap walls without penalty.

### Core Gameplay Loop
1. Start at spawn position on motorcycle
2. Navigate terrain using acceleration, braking, and rotation
3. Collect all apples (if level contains apples)
4. Reach and touch the flower
5. View completion time
6. Compare with personal best and world record times
7. Retry to improve time or progress to next level

### Difficulty Progression
- **Levels 1-17:** Tutorial and beginner levels (included in shareware demo)
- **Level 18:** Informational level (non-finishable in shareware)
- **Levels 19-54:** Advanced and expert levels (full version only)
- **Level 55:** Download information level (non-finishable)

---

## Physics Engine

### Core Physics Model
The physics system is the heart of Elasto Mania's gameplay. It must be replicated precisely for authentic feel.

#### Fundamental Components

**1. Collision System**
- Sphere-based collision detection only
- Three collision spheres: Front wheel, rear wheel, rider's head
- Static geometry only (no moving platforms in original Elma)
- Line segment collision for polygon edges
- Point-to-line distance calculations for wheel positioning

**2. Mass-Spring-Damper System**
- Center of mass (bike body) connected to wheels via spring-damper
- Wheels connected to center via mass-spring-damper physics
- Creates the characteristic "elastic" motorcycle behavior
- Spring stiffness and damping values critical for authentic feel

**3. Collision Response**
- Basic projection-based response
- Wheels projected out of intersecting geometry
- No complex friction models - simplified ground interaction
- Head collision = instant failure (no bounce/slide)

**4. Wheel Physics**
- Rear-wheel drive only
- Front wheel is passive (no power)
- Both wheels have independent suspension
- Wheels must maintain contact with ground for traction

**5. Braking Mechanics**
- Temporary stiff spring created between wheel and ground contact point
- Simulates wheel lockup behavior
- Different brake behavior for front vs rear wheel
- Can cause dramatic rotation changes

**6. Rotation Physics**
- Rider can actively rotate the bike (lean forward/backward)
- Rotation affects weight distribution
- Critical for maintaining balance and air control
- "Volt" system allows faster rotation in specific direction

**7. Gravity**
- Standard downward gravity (adjustable value to match original)
- Some levels feature gravity-changing apples
- Gravity apples change direction: floor becomes ceiling, etc.
- Unpopular feature but must be implemented for authenticity

#### Physics Constants (To Be Tuned)
These values must be reverse-engineered or tuned to match original Elma:
- Gravity strength
- Wheel spring stiffness
- Wheel damping coefficient
- Body spring stiffness
- Body damping coefficient
- Brake spring stiffness
- Acceleration force magnitude
- Rotation angular velocity
- Air resistance/drag coefficients
- Ground friction coefficient

#### Determinism Requirements
- Physics must be 100% deterministic for replay system
- Same inputs must always produce identical results
- Fixed timestep simulation required
- Floating-point consistency across platforms critical

---

## Controls and Input

### Default Control Scheme

#### Player 1 (Keyboard - Arrow Keys)
- **Up Arrow** - Accelerate (rear wheel drive)
- **Down Arrow** - Brake (both wheels)
- **Left Arrow** - Rotate counter-clockwise (lean backward)
- **Right Arrow** - Rotate clockwise (lean forward)
- **Space** - Turn around / Change direction (180° flip)

#### Player 2 (Keyboard - Numpad)
- **Numpad 5** - Accelerate
- **Numpad 2** - Brake
- **Numpad 1** - Rotate counter-clockwise
- **Numpad 3** - Rotate clockwise
- **Numpad 0** - Turn around

#### Global Controls
- **V Key** - Toggle navigator/map view
- **T Key** - Toggle timer display
- **I Key** - Screenshot
- **ESC** - Pause/Menu

### Advanced Techniques

#### Supervolt
- Pressing both rotation keys simultaneously causes faster clockwise rotation
- Originally a bug, now an accepted competitive technique
- Normally requires precise simultaneous key press
- Later versions (1.11h+) allow binding to single key

#### Alovolt
- Immediate supervolt without prior rotation
- Requires perfectly simultaneous button press (frame-perfect)
- Timing varies by system/frame rate
- Gives maximum clockwise spin instantly

#### Brutal Volt
- Advanced rotation technique for extreme angular velocity
- Specific timing sequence of rotation inputs
- Community-discovered technique

### Configuration Requirements
- All controls must be fully rebindable
- Support for game controller input (modern feature)
- Force feedback support (modern feature)
- Keyboard/controller hybrid support
- Multiple control profiles savable

### Input Handling
- 5 binary input states: Accelerate, Brake, Left, Right, Turn
- Inputs recorded at 30 FPS for replay system
- Input buffering for responsive feel
- No analog input in original (digital only)

---

## Level Design

### Complete Level List (54 Internal Levels)

All levels must be recreated exactly as in the original game:

1. **Warm Up** - Tutorial/beginner level
2. **Flat Track** - Simple flat terrain
3. **Twin Peaks** - Two hills to navigate
4. **Over and Under** - Mixed terrain elevation
5. **Uphill Battle** - Climbing focus
6. **Long Haul** - Extended level, endurance
7. **Hi Flyer** - Jumping and air control
8. **Tag** - Precision navigation
9. **Tunnel Terror** - Enclosed spaces
10. **The Steppes** - Stepped terrain
11. **Gravity Ride** - Gravity mechanics introduction
12. **Islands in the Sky** - Platform jumping
13. **Hill Legend** - Complex hillwork
14. **Loop-de-Loop** - Circular terrain
15. **Serpents Tale** - Winding paths
16. **New Wave** - Wave-pattern terrain
17. **Labyrinth** - Maze-like structure
18. **Spiral** - Circular/spiral layout
19. **Turnaround** - Direction changes
20. **Upside Down** - Ceiling riding
21. **Hangman** - Precision hanging sections
22. **Slalom** - Weaving through obstacles
23. **Quick Round** - Speed emphasis
24. **Ramp Frenzy** - Multiple jumps
25. **Precarious** - Dangerous positioning
26. **Circuitous** - Complex routing
27. **Shelf Life** - Shelf/ledge navigation
28. **Bounce Back** - Elastic physics showcase
29. **Headbanger** - Low ceiling challenges
30. **Pipe** - Pipe/tunnel navigation
31. **Animal Farm** - Thematic level
32. **Steep Corner** - Sharp angle navigation
33. **Zig-Zag** - Angular terrain
34. **Bumpy Journey** - Rough terrain
35. **Labyrinth Pro** - Advanced maze
36. **Fruit in the Den** - Apple collection focus
37. **Jaws** - Dangerous tight spaces
38. **Curvaceous** - Curved terrain mastery
39. **Haircut** - Very tight clearances
40. **Double Trouble** - Dual challenges
41. **Framework** - Structural navigation
42. **Enduro** - Endurance challenge
43. **He He** - Trick/joke level
44. **Freefall** - Falling/dropping sections
45. **Sink** - Descending level
46. **Bowling** - Rolling/momentum focus
47. **Enigma** - Puzzle-like routing
48. **Downhill** - Descending focus
49. **What the Heck** - Confusing/difficult
50. **Expert System** - Expert difficulty
51. **Tricks Abound** - Advanced techniques required
52. **Hang Tight** - Precision timing
53. **Hooked** - Hooking/curved paths
54. **Apple Harvest** - Final challenge level

### Level Structure Requirements

Each level must contain:
- **Spawn Point** - Single starting position for player
- **Terrain Polygons** - Ground/obstacle geometry (max 300 polygons, 1000 vertices per level)
- **Apples** - 0-20+ collectible objects, varies by level
- **Flower** - Single exit/goal object
- **Killers** - 0-20+ rotating spike obstacles
- **Gravity Apples** - Optional gravity-changing collectibles (rare)
- **Textures/Pictures** - Background and foreground decorative elements

### Level Design Principles
- Levels teach mechanics through design, not tutorials
- Difficulty curves within individual levels
- Multiple route options in advanced levels (optimal vs. safe)
- Precision required increases with level number
- Visual clarity despite simple graphics
- Memorable/iconic level layouts

### Polygon System
- Vector-based terrain (not tile-based)
- Polygons define ground, walls, ceilings
- Polygons can be "ground" (grassy texture) or "solid" (sky texture edge)
- Each polygon composed of connected line segments
- Vertex coordinates stored as floating-point
- Polygon rendering order matters for visual appearance

---

## Graphics System

### Visual Style
- **Colorful 2D** with retro aesthetic
- Simple, clean graphics prioritizing gameplay clarity
- Bright, saturated color palette
- Cartoony/playful art style
- Minimal particle effects (original had very few)

### Native Resolution
- **640x480** pixels (original)
- 4:3 aspect ratio
- Modern versions should support scaling and widescreen

### Graphics Architecture

#### LGR File System (Level Graphics Resource)
Graphics are stored separately from levels in .lgr files.

**Technical Specifications:**
- PCX format images (256-color palette)
- Palette limited to 256 colors from q1bike.pcx
- Maximum single picture size: 600,000 pixels (width × height)
- Individual object files limited to 255×255 pixels
- All graphics use shared color palette for consistency

**Graphics Categories:**

1. **Textures**
   - Ground/terrain textures
   - Masked textures for bushes, trees, objects
   - Normal pictures vs. masked pictures

2. **Bike and Rider**
   - q1bike.pcx - Player 1 bike and rider
   - q2bike.pcx - Player 2 bike and rider
   - Decorative parts auto-transparent
   - Special handling for bike graphics

3. **Animation Frames**
   - Object width must be multiple of 40 pixels
   - Each 40-pixel segment = 1 animation frame
   - Sequential frame playback for animations
   - Used for rotating killers, animated objects

4. **Background Elements**
   - Sky/background pictures
   - Non-interactive decorative elements
   - Parallax scrolling (if implemented)

**LGR Development Kit:**
- Tool: make_lgr.exe (command-line)
- Import custom pictures into game
- Palette conversion from PCX files
- Texture and sprite compilation

#### Default Graphics Set
Must include recreation of original graphics:
- Default grass texture
- Default bike sprite (two wheel positions + rider)
- Default killer sprite (rotating spikes)
- Default apple sprite
- Default flower sprite
- Default background sky
- UI elements (timer, menus, etc.)

### Rendering Requirements
- 2D sprite rendering
- Polygon fill rendering for terrain
- Texture mapping on polygons
- Sprite rotation (for killers, bike)
- Alpha/transparency support (for masked graphics)
- Layering: Background → Terrain → Objects → Foreground → UI
- Smooth camera following player position
- Screen shake effects (optional, for modern feel)

### Camera System
- Center on player bike
- Smooth following with slight lag
- Zoom level adjustable
- Navigator/map view (toggle with V key)
- Must keep player visible at all times
- Boundary clamping if level has edges

---

## Audio System

### Sound Requirements

The original game used sound effects stored in the ELMA.RES resource file. Modern recreation should include:

#### Sound Effects (SFX)
- **Engine Sound** - Continuous loop when accelerating, pitch varies with speed
- **Brake Sound** - Screeching when braking
- **Crash Sound** - When player dies (head/wheel collision)
- **Apple Collect** - Short pickup sound
- **Flower Touch** - Level complete sound
- **Turn Sound** - Direction change (spacebar)
- **Menu Sounds** - Selection, confirmation, back

#### Music
- Original game had minimal/no music during gameplay
- Menu music (if any)
- Victory jingle (optional)
- Modern version could add optional background music toggle

### Audio Format
- Original used PCM WAV files embedded in resources
- Modern version: .ogg or .wav for compatibility
- Low file size for retro authenticity

### Audio Implementation
- Positional audio for 3D spatial effects (modern enhancement)
- Volume controls: Master, SFX, Music (separate sliders)
- Audio mixing for overlapping sounds
- Engine sound pitch modulation based on acceleration

---

## Game Objects

### 1. Apples (Collectibles)

**Behavior:**
- Static position in level
- Disappear on contact with any part of bike or rider
- Must collect ALL apples before flower is accessible
- No physics interaction (pass-through until collected)

**Visuals:**
- Small red apple sprite
- Possible subtle animation (rotation, bobbing)
- Particle effect on collection (optional)

**Types:**
- **Normal Apple** - Standard collectible
- **Gravity Apple** - Changes gravity direction on collection
  - Floor becomes ceiling (or vice versa)
  - Walls become ground
  - Considered unpopular/disliked feature
  - No visual indicator before collection (design flaw from original)
  - Must be implemented for authenticity in relevant levels

**Count:** Varies by level, typically 0-20+

### 2. Flower (Goal/Exit)

**Behavior:**
- Single flower per level
- Static position
- Initially locked if level contains apples
- Unlocks when all apples collected
- Touch to complete level
- Triggers end-of-level sequence

**Visuals:**
- Flower sprite (sunflower-style in original)
- Subtle animation/sway
- Visual indicator when unlocked vs. locked (glow, color change)

**Collision:**
- Touch detection with any part of bike/rider
- Pass-through object (no physics collision)

### 3. Killers (Rotating Spikes)

**Behavior:**
- Rotating spiked ball/wheel
- Constant rotation speed
- Collision with head OR wheels = death
- Can pass through rider body safely (only head/wheels collide)

**Visuals:**
- Circular spike ball sprite
- Continuous rotation animation
- Clear visual danger indicator

**Physics:**
- Static position (no movement in original Elma)
- No physics interaction beyond collision detection
- Hit detection on wheel/head spheres only

**Count:** Varies by level, 0-20+

### 4. Starting Position

**Behavior:**
- Defined spawn point for player
- Always same position on restart
- Player spawns stationary on bike

**Technical:**
- Single point coordinate (x, y)
- Initial rotation angle (typically 0° = upright)

### 5. Terrain/Polygons

**Behavior:**
- Static collision geometry
- Can be "ground" type or "solid" type
- Different visual rendering based on type

**Collision:**
- Head collision = death
- Wheel collision = traction/surface contact
- Body passes through (no collision)

---

## User Interface

### Main Menu
- **Single Player** - Start level selection
- **Multiplayer** - Local 2-player mode
- **Level Editor** - Launch editor
- **Options** - Settings menu
- **Records** - View best times
- **Replays** - Watch saved replays
- **Exit** - Quit game

### Level Selection Screen
- Grid or list of all 54 levels
- Display for each level:
  - Level number and name
  - Personal best time (if completed)
  - World record time (optional, if online features)
  - Lock indicator for uncompleted levels
  - Apple count indicator
- Preview/thumbnail of level (optional)
- **Demo version:** Only levels 1-18 accessible

### In-Game HUD

**Minimal HUD approach:**
- **Timer** - Current run time (MM:SS:HH format)
  - Toggleable with T key
  - Top-right or top-center position
  - Hundredths of seconds precision
- **Apple Counter** - "Apples: X/Y" (collected/total)
  - Only visible if level has apples
  - Top-left position
- **Navigator** - Mini-map view
  - Toggleable with V key
  - Shows full level layout
  - Player position indicator
  - Apple/flower positions

**No other HUD elements** - Clean screen for gameplay focus

### End-of-Level Screen
- **Completion Time** - Large display of final time
- **Personal Best** - Show if new record
- **World Record** - Show comparison (if online)
- **Options:**
  - Retry Level
  - Next Level
  - Save Replay
  - Main Menu

### Pause Menu
- **Resume**
- **Restart Level**
- **Options**
- **Main Menu**
- **Quit**

### Options Menu
- **Graphics:**
  - Resolution selection
  - Fullscreen/Windowed toggle
  - VSync on/off
  - Graphics quality (if modern enhancements)
- **Audio:**
  - Master volume
  - SFX volume
  - Music volume
- **Controls:**
  - Key rebinding interface
  - Controller configuration
  - Supervolt binding option
- **Gameplay:**
  - Show timer (default on)
  - Show navigator (default off)
  - Auto-save replays
  - Physics settings (for accessibility/practice mode)

### Records/Statistics Screen
- Table of all 54 levels
- Personal best time for each
- Total time across all levels
- Completion percentage
- Death counter (optional)
- Attempt counter (optional)

### Replay Browser
- List of saved replays
- Sort by: Date, Level, Time
- Replay info: Level, Time, Date
- Options: Watch, Delete, Export
- Ghost replay feature (overlay on live attempt)

---

## Replay System

### Core Functionality
The replay system is critical for competitive play and community sharing.

### Recording

**What is Recorded:**
- All player inputs at 30 FPS
  - Accelerate (on/off)
  - Brake (on/off)
  - Rotate Left (on/off)
  - Rotate Right (on/off)
  - Turn (on/off)
- Level identifier
- Starting random seed (if any randomness in physics)
- Replay metadata: Player name, date, time

**What is NOT Recorded:**
- Actual physics state (position, velocity, rotation)
- Replay reconstructs physics from inputs + deterministic engine

**Recording Format:**
- Binary file format (.rec extension)
- Compact size (inputs only)
- Maximum replay length: 5 minutes (300 seconds)

### Playback

**Deterministic Replay:**
- Same inputs + same physics = identical result
- Must perfectly reproduce original run
- Proves time legitimacy for world records

**Playback Features:**
- Watch full replay
- Pause/resume
- Speed control (0.5x, 1x, 2x, 4x)
- Frame advance (for analysis)
- Ghost replay (semi-transparent bike overlay during live play)

**Camera Control During Playback:**
- Follow bike (default)
- Free camera (optional)
- Zoom in/out

### Replay Validation

**For World Record Submission:**
- Replay file (.rec)
- State.dat file (player profile, prevents certain hacks)
- Files sent to record authority (Moposite equivalent)
- Automated validation of file integrity
- Manual review for suspicious times

**Integrity Checks:**
- File checksum/hash
- Time stamp verification
- Physics engine version matching
- No impossible inputs (simultaneous conflicting inputs)

### Auto-Save
- Option to automatically save replays on:
  - Level completion
  - New personal record
  - All attempts (for practice review)
- Configurable in options

---

## Multiplayer

### Local Multiplayer (Split-Screen)

**Mode: Simultaneous 2-Player**
- Both players play same level at same time
- Split-screen view (horizontal or vertical split)
- Independent completion times
- First to finish or both finish separately

**Controls:**
- Player 1: Arrow keys + Space
- Player 2: Numpad controls
- Each player has independent input handling

**Features:**
- Same as single-player per player
- Independent death/restart
- Can watch each other's replays afterward
- Shared level progression unlocking (modern version)
- Level skip option if stuck (modern version)

**Technical:**
- Two independent physics simulations
- Two independent collision checks
- Synchronized rendering
- Equal screen real estate per player

### Online Multiplayer (Modern Feature - Not in Original)

**Leaderboards:**
- Global best times per level
- Total time leaderboards (all 54 levels)
- Regional leaderboards
- Friends leaderboards

**Ghost Downloads:**
- Download world record replays
- Download friend replays
- Race against ghost

**Online Features:**
- Replay sharing
- Custom level sharing
- Profile/statistics tracking

**NOT INCLUDED:**
- Real-time online racing (too latency-sensitive for physics)
- Stick to async leaderboards and ghost racing

---

## Level Editor

### Core Functionality
Robust level editor for community content creation.

### Editor Features

**Terrain Editing:**
- Draw polygons by placing vertices
- Click-and-drag vertex movement
- Polygon deletion
- Polygon properties: Ground vs. Solid type
- Visual grid for alignment
- Snap-to-grid option
- Coordinate display

**Object Placement:**
- Place start position (1 required)
- Place flower (1 required)
- Place apples (0-unlimited)
- Place killers (0-unlimited)
- Drag to reposition
- Rotation for killers (starting angle)

**Graphics/Textures:**
- Select LGR file for level
- Texture selection for polygons
- Background picture placement
- Foreground picture placement
- Picture scaling/rotation

**View Controls:**
- Pan camera (click-drag or arrow keys)
- Zoom in/out (mousewheel)
- Full level view
- Grid toggle
- Coordinate system display

**Testing:**
- "Test Level" button launches playable preview
- Return to editor from test
- Iterate rapidly

**File Operations:**
- New level
- Open level (.lev file)
- Save level
- Save As
- Export for sharing

### Editor UI

**Layout:**
- Large central canvas (level view)
- Tool palette (left sidebar)
  - Select tool
  - Vertex tool
  - Polygon tool
  - Object tool
- Properties panel (right sidebar)
  - Selected object properties
  - Level properties
  - LGR selection
- Top menu bar
  - File, Edit, View, Tools, Help
- Bottom status bar
  - Cursor coordinates
  - Polygon count / vertex count
  - Zoom level

### Level Validation

**Requirements Check:**
- Must have exactly 1 start position
- Must have exactly 1 flower
- Polygon count ≤ 300
- Vertex count ≤ 1000
- All polygons must be valid (≥3 vertices)
- No self-intersecting polygons (optional check)

**Warnings (Non-Fatal):**
- Level has no apples
- Very large/small polygons
- Objects outside reasonable bounds
- Potential soft-lock situations

---

## File Formats

### LEV File (Level Format)

**Purpose:** Stores level topology, objects, and metadata

**File Structure:**
- **Header:**
  - Magic bytes: "MAGLEV" (POT14 format variant)
  - Version number
  - Level name (string, max 51 characters)
  - LGR filename (graphics resource to use)

- **Polygon Data:**
  - Polygon count (max 300)
  - For each polygon:
    - Grass/ground flag (boolean)
    - Vertex count
    - Vertex coordinates (x, y pairs as floats)
    - Texture index (optional)

- **Object Data:**
  - Object count (apples + killers + flowers + start)
  - For each object:
    - Object type (apple, killer, flower, start)
    - Position (x, y)
    - Animation number (for apples/killers)
    - Gravity direction (for gravity apples)

- **Pictures:**
  - Picture count
  - For each picture:
    - Texture/picture name
    - Position (x, y)
    - Distance value (parallax depth)
    - Clipping (clip/unclip)

**Format:** Binary file, little-endian

**Limits:**
- Max 300 polygons
- Max 1000 vertices total
- Max ~250 objects (estimate based on community levels)
- File size typically <100KB

### LGR File (Level Graphics Resource)

**Purpose:** Stores all graphics for a level/mod

**Contents:**
- Compressed PCX images
- 256-color palette
- Textures, sprites, objects
- Picture data organized by type

**Creation:**
- Use make_lgr.exe tool (or modern equivalent)
- Import PCX files with correct palette
- Compile into single LGR file

**Format:** Custom binary format
- Header with file count
- Image data blocks
- Palette data

### REC File (Replay)

**Purpose:** Stores input recording for replay playback

**File Structure:**
- **Header:**
  - Magic bytes/version
  - Level filename
  - Player name
  - Time in hundredths (completion time)
  - Date/timestamp

- **Frame Data:**
  - Recorded at 30 FPS
  - Each frame: 5 binary flags (up, down, left, right, turn)
  - Bitpacked for compression
  - Max 9000 frames (300 seconds × 30 FPS)

**Format:** Binary file, highly compressed
**Size:** Typically 1-10 KB per replay

### STATE.DAT File (Player Profile)

**Purpose:** Stores player progress, best times, unlocked levels

**Contents:**
- Player name
- Best time for each of 54 levels
- Level unlock status
- Statistics (deaths, attempts, playtime)
- Configuration settings

**Validation:**
- Used with replay files to verify legitimacy
- Prevents certain types of cheating
- Checksum for integrity

**Format:** Binary file
**Location:** Game root directory

### Configuration Files

**ELMACONF.TXT / config.ini:**
- Graphics settings (resolution, fullscreen)
- Audio settings (volumes)
- Control bindings
- Gameplay options

**Format:** Plain text INI-style or custom format

---

## Technical Specifications

### Minimum System Requirements

**Original (Year 2000):**
- Windows 95/NT/98/ME/2000/XP
- DirectX 5.0
- Pentium 133 MHz
- 16 MB RAM
- 4 MB hard disk space

**Modern Recreation (2026):**
- Windows 10/11, macOS 10.14+, Linux (Ubuntu 20.04+)
- 64-bit processor
- 512 MB RAM
- 100 MB hard disk space
- OpenGL 3.3+ or DirectX 11+ compatible GPU
- Keyboard or game controller

### Performance Targets
- **Frame Rate:** 60 FPS minimum (display), 30 FPS physics tick (for replay compatibility)
- **Input Latency:** <16ms (1 frame at 60 FPS)
- **Load Times:** <2 seconds per level
- **Memory Usage:** <200 MB RAM

### Platform Support
**Priority 1 (Must Have):**
- Windows 10/11 (64-bit)

**Priority 2 (Should Have):**
- macOS (Intel + Apple Silicon)
- Linux (Ubuntu, Debian, Arch)

**Priority 3 (Nice to Have):**
- Steam Deck compatibility
- Web version (WebGL/WASM)
- Mobile (iOS/Android) with touch controls

### Technology Stack Recommendations

**Game Engine Options:**
- **Custom Engine** - Maximum control, better for physics accuracy
- **Godot** - Open source, 2D focused, good physics
- **Unity** - Widely used, extensive tools, replay may need custom physics
- **MonoGame/FNA** - C#, close to original's DirectX approach
- **Raylib** - Lightweight, C-based, full control

**Language:**
- C# (Unity, MonoGame) - Good balance of performance and productivity
- C++ (Custom, Raylib) - Maximum performance, complex
- Rust - Memory safe, excellent performance, modern
- Go - Simple, good enough performance, easy distribution

**Physics:**
- Custom 2D physics (recommended for determinism)
- Box2D (modify for Elma-style physics)
- Fully custom implementation for 100% accuracy

**Networking (for online features):**
- REST API for leaderboards
- WebSocket for real-time features
- Cloud storage for replays (AWS S3, Google Cloud Storage)

### Version Control
- Git repository
- GitHub/GitLab for hosting
- Branching strategy for features/releases

### Build System
- Automated builds for all platforms
- CI/CD pipeline (GitHub Actions, GitLab CI)
- Automated testing for physics determinism

---

## Development Roadmap

### Phase 1: Core Engine (Months 1-3)

**Goal:** Functional physics and basic gameplay

**Deliverables:**
- ✅ Physics engine implementation
  - Collision detection (spheres + line segments)
  - Mass-spring-damper system
  - Gravity simulation
  - Wheel-ground interaction
  - Rotation mechanics
- ✅ Input system
  - Keyboard controls
  - 5 input states handling
  - Configurable bindings
- ✅ Basic rendering
  - 2D sprite rendering
  - Polygon rendering
  - Camera system
- ✅ Simple test level (not original levels yet)
- ✅ Bike and rider sprites
- ✅ Basic collision (head, wheels)

**Success Criteria:**
- Player can ride bike with authentic "feel"
- Physics behaves like original Elma
- Can complete simple custom test level

### Phase 2: Level Support (Months 4-5)

**Goal:** Load and play original levels

**Deliverables:**
- ✅ LEV file parser
  - Read polygon data
  - Read object data
  - Read picture data
- ✅ LGR file support
  - Load PCX images
  - Palette handling
  - Texture system
- ✅ All game objects implemented
  - Apples (normal + gravity)
  - Flower
  - Killers
  - Start position
- ✅ Recreate first 5 internal levels
  - Warm Up
  - Flat Track
  - Twin Peaks
  - Over and Under
  - Uphill Battle
- ✅ Level completion logic
- ✅ Basic UI for level selection

**Success Criteria:**
- Can load and complete original levels 1-5
- All objects behave correctly
- Graphics match original aesthetic

### Phase 3: Full Level Set (Months 6-7)

**Goal:** All 54 original levels playable

**Deliverables:**
- ✅ Recreate ALL 54 internal levels
  - Exact geometry matching original
  - All apples/killers placed correctly
  - Textures and graphics faithful
- ✅ Level progression system
  - Unlock levels sequentially
  - Track completion status
- ✅ Difficulty balancing review
- ✅ Polish level-specific graphics

**Success Criteria:**
- All 54 levels completable
- Geometry accurate to original (within 1%)
- Community playtest confirms authenticity

### Phase 4: Replay System (Month 8)

**Goal:** Recording and playback of runs

**Deliverables:**
- ✅ Replay recording
  - Input capture at 30 FPS
  - REC file writing
  - Metadata (name, time, date)
- ✅ Replay playback
  - REC file reading
  - Deterministic physics reproduction
  - Playback controls (pause, speed)
- ✅ Replay browser UI
- ✅ Auto-save options
- ✅ Ghost replay feature

**Success Criteria:**
- Replays reproduce runs perfectly (100% accuracy)
- Can save and load replays reliably
- Ghost racing works smoothly

### Phase 5: UI & Polish (Months 9-10)

**Goal:** Complete user experience

**Deliverables:**
- ✅ Main menu implementation
- ✅ Level selection screen
- ✅ In-game HUD (timer, apple counter, navigator)
- ✅ End-of-level screen
- ✅ Options menu (graphics, audio, controls)
- ✅ Records/statistics screen
- ✅ Audio implementation
  - Engine sounds
  - SFX (crash, apple, flower)
  - UI sounds
- ✅ Graphics polish
  - Particle effects
  - Screen transitions
  - Visual feedback

**Success Criteria:**
- Intuitive, polished menus
- All UI functional and bug-free
- Audio enhances experience without distraction

### Phase 6: Level Editor (Months 11-12)

**Goal:** Community content creation

**Deliverables:**
- ✅ Terrain editing tools
  - Polygon creation/editing
  - Vertex manipulation
- ✅ Object placement tools
- ✅ Graphics/texture tools
- ✅ Level testing from editor
- ✅ File save/load
- ✅ Level validation
- ✅ Documentation/tutorial

**Success Criteria:**
- Users can create complex levels
- Editor is intuitive for beginners
- Can recreate original levels using editor
- Export/import levels easily

### Phase 7: Multiplayer (Months 13-14)

**Goal:** Local and online competition

**Deliverables:**
- ✅ Local split-screen multiplayer
  - Dual physics simulation
  - Independent controls
  - Split-screen rendering
- ✅ Online leaderboards
  - Level-specific boards
  - Total time boards
  - Regional/friends filtering
- ✅ Replay sharing
  - Upload replays to server
  - Download community replays
  - Ghost racing vs. online players
- ✅ Profile system
  - Online accounts
  - Statistics tracking

**Success Criteria:**
- Local multiplayer is fun and functional
- Leaderboards are accurate and cheat-resistant
- Replay sharing works seamlessly

### Phase 8: Testing & Optimization (Months 15-16)

**Goal:** Bug-free, performant release

**Deliverables:**
- ✅ Comprehensive bug testing
  - Physics edge cases
  - Level geometry issues
  - UI bugs
  - Replay desync issues
- ✅ Performance optimization
  - Maintain 60 FPS on target hardware
  - Reduce load times
  - Memory optimization
- ✅ Platform-specific testing
  - Windows builds
  - macOS builds
  - Linux builds
- ✅ Community beta testing
  - Gather feedback
  - Fix critical issues
  - Balance tweaks
- ✅ Accessibility features
  - Colorblind modes
  - Control customization
  - Practice mode (optional)

**Success Criteria:**
- Zero critical bugs
- Consistent 60 FPS performance
- Positive community feedback
- Passes certification (if console release)

### Phase 9: Launch (Month 17)

**Goal:** Public release

**Deliverables:**
- ✅ Final build for all platforms
- ✅ Store pages (Steam, itch.io, etc.)
- ✅ Marketing materials
  - Trailer video
  - Screenshots
  - Press kit
- ✅ Documentation
  - Player manual
  - Level editor guide
  - FAQ
- ✅ Community setup
  - Discord server
  - Subreddit/forum
  - Social media
- ✅ Launch day support plan

**Success Criteria:**
- Smooth launch with minimal issues
- Positive reviews from players and press
- Active community engagement
- Stable servers (if online features)

### Post-Launch Support

**Ongoing (Months 18+):**
- Bug fixes and patches
- Balance adjustments
- Additional levels (DLC or free)
- Community level spotlight
- Seasonal events/challenges
- Quality-of-life improvements
- New features based on feedback

---

## Success Metrics

### Player Engagement
- **Retention:** 40% of players return after 1 week
- **Completion:** 60% of players complete at least level 10
- **Mastery:** 20% of players complete all 54 levels

### Community
- **Level Sharing:** 1000+ custom levels created in first 3 months
- **Replays:** 10,000+ replays shared in first month
- **Leaderboards:** 5,000+ players on leaderboards

### Performance
- **Frame Rate:** 95% of players achieve 60 FPS
- **Load Time:** Average level load <1 second
- **Crashes:** <0.5% crash rate

### Business (if commercial)
- **Sales:** 10,000 copies in first month
- **Revenue:** $50,000+ in first quarter
- **Reviews:** 4.5+ stars average (Steam, metacritic)

---

## Risk Assessment

### Technical Risks

**Risk: Physics Accuracy**
- **Impact:** High - Inaccurate physics ruins gameplay
- **Likelihood:** Medium
- **Mitigation:**
  - Extensive playtesting by original Elma veterans
  - Side-by-side comparison with original
  - Open source physics code for community review
  - Replay validation against original game

**Risk: Replay Determinism**
- **Impact:** High - Replays must be perfect for competitive play
- **Likelihood:** Medium
- **Mitigation:**
  - Fixed timestep physics
  - Careful floating-point handling
  - Cross-platform testing
  - Regression tests for physics changes

**Risk: Performance Issues**
- **Impact:** Medium - Game must run smoothly
- **Likelihood:** Low
- **Mitigation:**
  - Simple 2D graphics keep requirements low
  - Profile and optimize early
  - Target modest hardware

### Legal Risks

**Risk: Copyright/Trademark Issues**
- **Impact:** High - Could force takedown or rebrand
- **Likelihood:** Low-Medium
- **Mitigation:**
  - Different name ("Bungee Biker" not "Elasto Mania")
  - Original artwork (not copied sprites)
  - Clean-room implementation (no decompiled code)
  - Legal review before launch
  - Consider open source to reduce commercial risk

**Risk: Level Design Copyright**
- **Impact:** Medium - Original levels might be protected
- **Likelihood:** Low
- **Mitigation:**
  - Game mechanics not copyrightable
  - Level geometry is functional, arguable fair use
  - Could create new levels inspired by originals
  - Consult IP lawyer

### Market Risks

**Risk: Limited Audience**
- **Impact:** Medium - Niche game, small market
- **Likelihood:** Medium
- **Mitigation:**
  - Keep development costs low
  - Target passionate existing community
  - Price accessibly ($5-15)
  - Free demo version (first 18 levels)

**Risk: Original Game Competition**
- **Impact:** Low - Original still available
- **Likelihood:** High
- **Mitigation:**
  - Offer modern features (online leaderboards, HD graphics option)
  - Better onboarding for new players
  - Cross-platform support
  - Active development and community

---

## Appendix A: Physics Tuning Parameters

These values must be determined through reverse engineering or iterative tuning:

```
GRAVITY = 9.81 (or tuned value)
WHEEL_RADIUS = 0.4 (meters, estimate)
BIKE_CENTER_HEIGHT = 1.0 (meters, estimate)
WHEEL_SPRING_K = 500.0 (spring constant)
WHEEL_DAMPING_C = 50.0 (damping coefficient)
BIKE_SPRING_K = 100.0
BIKE_DAMPING_C = 20.0
BRAKE_SPRING_K = 1000.0
ACCELERATION_FORCE = 30.0 (Newtons)
ROTATION_TORQUE = 10.0 (Newton-meters)
FRICTION_GROUND = 0.8 (coefficient)
AIR_RESISTANCE = 0.01 (drag coefficient)
MAX_SPEED = 20.0 (meters/second, approximate)
```

These are estimates and must be fine-tuned through testing.

---

## Appendix B: Control Bindings Reference

### Default Keyboard Scheme
| Action | Player 1 | Player 2 |
|--------|----------|----------|
| Accelerate | Up Arrow | Numpad 5 |
| Brake | Down Arrow | Numpad 2 |
| Rotate CCW | Left Arrow | Numpad 1 |
| Rotate CW | Right Arrow | Numpad 3 |
| Turn Around | Space | Numpad 0 |
| Navigator | V | V |
| Timer | T | T |
| Screenshot | I | I |
| Pause | ESC | ESC |

### Suggested Gamepad Scheme
| Action | Binding |
|--------|---------|
| Accelerate | Right Trigger |
| Brake | Left Trigger |
| Rotate | Left Stick (X-axis) |
| Turn Around | A Button |
| Navigator | Y Button |
| Pause | Start Button |

---

## Appendix C: Level Design Guidelines

For creating new levels (beyond the 54 internal levels):

### Beginner Levels (Like 1-10)
- Wide, forgiving terrain
- Few obstacles
- Short length (20-40 seconds completion time)
- Teach one concept per level
- No gravity apples
- Few or no killers

### Intermediate Levels (Like 11-35)
- Tighter corridors
- Multiple route options
- Moderate length (40-90 seconds)
- Combine multiple concepts
- Occasional killer placement
- Require some precision

### Advanced Levels (Like 36-54)
- Pixel-perfect precision required
- Complex routing puzzles
- Long length possible (90-180+ seconds)
- All techniques required
- Dense killer placement
- Gravity apples (if absolutely necessary)
- Punishing but fair

### General Principles
- **Visibility:** Player should see upcoming challenges
- **Checkpointing:** (via level design) Difficult sections followed by easier recovery
- **Flow:** Smooth transitions between sections
- **Fairness:** Deaths should feel earned, not cheap
- **Clarity:** Distinguish background from collision geometry
- **Testability:** Play your level 20+ times before releasing

---

## Appendix D: Reference Materials

### Primary Sources
- [Elasto Mania Official Site](https://elastomania.com/)
- [Elasto Mania on Steam](https://store.steampowered.com/app/1290220/Elasto_Mania_Remastered/)
- [Wikipedia - Elasto Mania](https://en.wikipedia.org/wiki/Elasto_Mania)
- [Moposite - Elma Community Hub](https://moposite.com/)
- [Elma Wiki](https://wiki.elmaonline.net/)
- [Speedrun.com - Elasto Mania](https://www.speedrun.com/elma)

### Technical Resources
- [elma-rust - Level/Replay Parser](https://github.com/elmadev/elma-rust)
- [elmajs - NPM Package](https://github.com/elmadev/elmajs)
- [recplay - JS Replay Renderer](https://github.com/Maxdamantus/recplay)
- [Elmanager - Replay/Level Manager](https://github.com/Smibu/elmanager)

### Community Resources
- [GameDev.net Physics Discussion](https://gamedev.net/forums/topic/397791-elasto-mania/)
- [PCGamingWiki - Technical Info](https://www.pcgamingwiki.com/wiki/Elasto_Mania)
- [Steam Community Guides](https://steamcommunity.com/app/1290220/guides/)

### Gameplay Videos
- Search "Elasto Mania gameplay" on YouTube
- Search "Elasto Mania speedrun" on YouTube
- Search "Elasto Mania world record" on YouTube

---

## Conclusion

**Bungee Biker** aims to faithfully recreate the beloved Elasto Mania experience while modernizing aspects like graphics options, online features, and cross-platform support. The core physics, level design, and gameplay loop must remain authentic to honor the original while making the game accessible to a new generation of players.

Success depends on:
1. **Physics Accuracy** - The game must *feel* like Elasto Mania
2. **Level Faithfulness** - All 54 levels recreated precisely
3. **Replay System** - Deterministic, reliable, competitive-ready
4. **Community Tools** - Level editor and sharing features
5. **Polish** - Modern UI/UX without sacrificing simplicity

With careful execution across the 17-month roadmap, Bungee Biker can become the definitive modern version of this classic physics platformer.

---

**Document Version:** 1.0
**Last Updated:** January 22, 2026
**Next Review:** February 2026 (after Phase 1 completion)

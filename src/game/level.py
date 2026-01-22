"""
Level class for Bungee Biker
Manages terrain, objects, and level state
"""

from typing import List
from ..engine.physics import Vec2, Line, Bike, PhysicsConstants
from .objects import Apple, Flower, Killer


class Level:
    """Represents a game level"""

    def __init__(self, name: str):
        self.name = name
        self.terrain: List[Line] = []
        self.is_ground: List[bool] = []  # Track which lines are ground vs solid
        self.start_position = Vec2(0, 0)
        self.apples: List[Apple] = []
        self.flower: Flower = None
        self.killers: List[Killer] = []

        # Level state
        self.time = 0.0
        self.completed = False
        self.completion_time = 0.0

    def update(self, dt: float, bike: Bike):
        """Update level objects and check win/lose conditions"""
        if self.completed or not bike.alive:
            return

        self.time += dt

        # Update animated objects
        if self.flower:
            self.flower.update(dt)

        for killer in self.killers:
            killer.update(dt)

        # Check apple collection
        for apple in self.apples:
            if not apple.collected:
                apple.check_collision(bike.position, bike.rotation)

        # Check killer collisions
        for killer in self.killers:
            # Check head collision
            if killer.check_collision(bike.get_head_position(), PhysicsConstants.HEAD_RADIUS):
                bike.alive = False
                return

            # Check wheel collisions
            if killer.check_collision(bike.rear_wheel.position, PhysicsConstants.WHEEL_RADIUS):
                bike.alive = False
                return

            if killer.check_collision(bike.front_wheel.position, PhysicsConstants.WHEEL_RADIUS):
                bike.alive = False
                return

        # Check if flower is unlocked (all apples collected)
        flower_unlocked = all(apple.collected for apple in self.apples)

        # Check level completion
        if flower_unlocked and self.flower:
            if self.flower.check_collision(bike.position):
                self.completed = True
                self.completion_time = self.time

    def get_collected_apples(self) -> int:
        """Get number of collected apples"""
        return sum(1 for apple in self.apples if apple.collected)

    def get_total_apples(self) -> int:
        """Get total number of apples"""
        return len(self.apples)

    def is_flower_unlocked(self) -> bool:
        """Check if flower is accessible"""
        return all(apple.collected for apple in self.apples)

    def reset(self):
        """Reset level state"""
        self.time = 0.0
        self.completed = False
        self.completion_time = 0.0

        for apple in self.apples:
            apple.collected = False


def create_test_level() -> Level:
    """Create a simple test level for development"""
    level = Level("Test Level - Warm Up")

    # Starting position
    level.start_position = Vec2(2, 0)

    # Create simple ground terrain
    ground_points = [
        Vec2(0, 5),
        Vec2(5, 5),
        Vec2(7, 6),
        Vec2(10, 6),
        Vec2(12, 7),
        Vec2(15, 7),
        Vec2(17, 6),
        Vec2(20, 6),
        Vec2(25, 5),
        Vec2(30, 5),
    ]

    # Convert to line segments
    for i in range(len(ground_points) - 1):
        level.terrain.append(Line(ground_points[i], ground_points[i + 1]))
        level.is_ground.append(True)

    # Add some walls
    # Left wall
    level.terrain.append(Line(Vec2(0, 5), Vec2(0, -5)))
    level.is_ground.append(False)

    # Right wall
    level.terrain.append(Line(Vec2(30, 5), Vec2(30, -5)))
    level.is_ground.append(False)

    # Ceiling obstacle
    level.terrain.append(Line(Vec2(10, 2), Vec2(15, 2)))
    level.is_ground.append(False)

    # Small platform/ramp
    level.terrain.append(Line(Vec2(18, 4), Vec2(20, 3)))
    level.is_ground.append(True)

    # Add apples
    level.apples.append(Apple(Vec2(8, 4)))
    level.apples.append(Apple(Vec2(13, 5)))
    level.apples.append(Apple(Vec2(22, 4)))

    # Add flower at end
    level.flower = Flower(Vec2(28, 3))

    # Add a killer obstacle
    level.killers.append(Killer(Vec2(16, 4.5), rotation_speed=2.0))

    return level


def create_flat_track() -> Level:
    """Create a very simple flat level for testing physics"""
    level = Level("Flat Track")

    level.start_position = Vec2(2, 0)

    # Simple flat ground
    level.terrain.append(Line(Vec2(0, 5), Vec2(50, 5)))
    level.is_ground.append(True)

    # Left wall
    level.terrain.append(Line(Vec2(0, 5), Vec2(0, -5)))
    level.is_ground.append(False)

    # Right wall
    level.terrain.append(Line(Vec2(50, 5), Vec2(50, -5)))
    level.is_ground.append(False)

    # Few apples
    level.apples.append(Apple(Vec2(10, 3)))
    level.apples.append(Apple(Vec2(20, 3)))
    level.apples.append(Apple(Vec2(30, 3)))

    # Flower at end
    level.flower = Flower(Vec2(45, 3))

    return level

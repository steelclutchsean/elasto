"""
Game objects for Bungee Biker
"""

import math
from ..engine.physics import Vec2


class Apple:
    """Collectible apple object"""

    def __init__(self, position: Vec2):
        self.position = position
        self.collected = False
        self.radius = 0.25

    def check_collision(self, bike_position: Vec2, bike_rotation: float) -> bool:
        """Check if bike touched this apple"""
        if self.collected:
            return False

        # Check collision with bike center and head area
        distance = (self.position - bike_position).length()
        if distance < 1.0:  # Close enough to collect
            self.collected = True
            return True

        return False


class Flower:
    """Goal/exit flower object"""

    def __init__(self, position: Vec2):
        self.position = position
        self.radius = 0.4
        self.rotation = 0.0

    def update(self, dt: float):
        """Animate the flower"""
        self.rotation += dt * 0.5

    def check_collision(self, bike_position: Vec2) -> bool:
        """Check if bike touched the flower"""
        distance = (self.position - bike_position).length()
        return distance < 1.0


class Killer:
    """Rotating spike obstacle"""

    def __init__(self, position: Vec2, rotation_speed: float = 1.0):
        self.position = position
        self.rotation = 0.0
        self.rotation_speed = rotation_speed
        self.radius = 0.5

    def update(self, dt: float):
        """Rotate the killer"""
        self.rotation += dt * self.rotation_speed
        if self.rotation > 2 * math.pi:
            self.rotation -= 2 * math.pi

    def check_collision(self, point: Vec2, point_radius: float) -> bool:
        """Check if a point (wheel or head) touches this killer"""
        distance = (self.position - point).length()
        return distance < (self.radius + point_radius)

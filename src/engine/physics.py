"""
Core physics engine for Bungee Biker
Implements the mass-spring-damper system that gives Elasto Mania its characteristic feel
"""

import math
from typing import Tuple, List, Optional


class Vec2:
    """2D Vector class for physics calculations"""

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    def __add__(self, other: 'Vec2') -> 'Vec2':
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vec2') -> 'Vec2':
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> 'Vec2':
        return Vec2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> 'Vec2':
        return Vec2(self.x / scalar, self.y / scalar)

    def dot(self, other: 'Vec2') -> float:
        return self.x * other.x + self.y * other.y

    def length(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)

    def length_squared(self) -> float:
        return self.x * self.x + self.y * self.y

    def normalize(self) -> 'Vec2':
        length = self.length()
        if length > 0.0001:
            return Vec2(self.x / length, self.y / length)
        return Vec2(0, 0)

    def rotate(self, angle: float) -> 'Vec2':
        """Rotate vector by angle in radians"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Vec2(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a
        )

    def to_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)

    def copy(self) -> 'Vec2':
        return Vec2(self.x, self.y)


class PhysicsConstants:
    """Physics constants tuned to match Elasto Mania feel"""

    # Gravity
    GRAVITY = 9.81 * 2.0  # Stronger gravity for game feel

    # Bike dimensions
    WHEEL_RADIUS = 0.4
    BIKE_WIDTH = 1.2
    HEAD_RADIUS = 0.3

    # Spring-damper system
    WHEEL_SPRING_K = 800.0  # Spring stiffness for wheels
    WHEEL_DAMPING_C = 80.0  # Damping for wheels

    # Forces
    ACCELERATION_FORCE = 35.0
    ROTATION_TORQUE = 12.0
    BRAKE_FRICTION = 0.95  # Multiplier for braking
    GROUND_FRICTION = 0.98  # Natural friction
    AIR_RESISTANCE = 0.995  # Slight air drag

    # Collision
    COLLISION_ELASTICITY = 0.1  # Bounce factor
    MIN_GROUND_NORMAL_Y = 0.3  # Minimum Y component to be considered ground

    # Physics timestep
    FIXED_DT = 1.0 / 30.0  # 30 FPS physics for replay compatibility


class Line:
    """Line segment for terrain collision"""

    def __init__(self, p1: Vec2, p2: Vec2):
        self.p1 = p1
        self.p2 = p2

    def closest_point_on_line(self, point: Vec2) -> Tuple[Vec2, float]:
        """
        Find closest point on line segment to given point
        Returns (closest_point, distance)
        """
        line_vec = self.p2 - self.p1
        point_vec = point - self.p1
        line_len_sq = line_vec.length_squared()

        if line_len_sq < 0.0001:
            return self.p1.copy(), (point - self.p1).length()

        # Project point onto line
        t = max(0.0, min(1.0, point_vec.dot(line_vec) / line_len_sq))
        projection = self.p1 + line_vec * t

        distance = (point - projection).length()
        return projection, distance

    def normal(self) -> Vec2:
        """Get normal vector to line (perpendicular, pointing 'up')"""
        line_vec = self.p2 - self.p1
        # Rotate 90 degrees counter-clockwise
        normal = Vec2(-line_vec.y, line_vec.x)
        return normal.normalize()


class Wheel:
    """Represents a single wheel of the bike"""

    def __init__(self, offset: Vec2):
        self.offset = offset  # Offset from bike center when at rest
        self.position = Vec2()
        self.velocity = Vec2()
        self.touching_ground = False
        self.ground_point = Vec2()
        self.ground_normal = Vec2(0, -1)

    def update_spring_force(self, bike_pos: Vec2, bike_vel: Vec2,
                           bike_rotation: float) -> Vec2:
        """Calculate spring force connecting wheel to bike center"""
        # Target position relative to bike (rotated offset)
        target_offset = self.offset.rotate(bike_rotation)
        target_pos = bike_pos + target_offset

        # Spring force
        displacement = target_pos - self.position
        spring_force = displacement * PhysicsConstants.WHEEL_SPRING_K

        # Damping force
        relative_vel = bike_vel - self.velocity
        damping_force = relative_vel * PhysicsConstants.WHEEL_DAMPING_C

        return spring_force + damping_force


class Bike:
    """
    The bike physics model using mass-spring-damper system
    This is the heart of the Elasto Mania physics
    """

    def __init__(self, start_pos: Vec2):
        # Center of mass
        self.position = start_pos.copy()
        self.velocity = Vec2()
        self.rotation = 0.0  # Angle in radians
        self.angular_velocity = 0.0

        # Wheels (front and rear)
        self.rear_wheel = Wheel(Vec2(-PhysicsConstants.BIKE_WIDTH / 2, 0))
        self.front_wheel = Wheel(Vec2(PhysicsConstants.BIKE_WIDTH / 2, 0))

        # Head position (relative to center)
        self.head_offset = Vec2(0, -0.8)

        # Input state
        self.input_accelerate = False
        self.input_brake = False
        self.input_rotate_left = False
        self.input_rotate_right = False

        # State
        self.alive = True
        self.on_ground = False

        # Initialize wheel positions
        self._update_wheel_positions()

    def _update_wheel_positions(self):
        """Update wheel positions to match bike position (initialization)"""
        rear_offset = self.rear_wheel.offset.rotate(self.rotation)
        front_offset = self.front_wheel.offset.rotate(self.rotation)
        self.rear_wheel.position = self.position + rear_offset
        self.front_wheel.position = self.position + front_offset

    def get_head_position(self) -> Vec2:
        """Get current head position in world space"""
        rotated_offset = self.head_offset.rotate(self.rotation)
        return self.position + rotated_offset

    def apply_gravity(self, dt: float):
        """Apply gravity to all components"""
        gravity_force = Vec2(0, PhysicsConstants.GRAVITY)
        self.velocity = self.velocity + gravity_force * dt
        self.rear_wheel.velocity = self.rear_wheel.velocity + gravity_force * dt
        self.front_wheel.velocity = self.front_wheel.velocity + gravity_force * dt

    def apply_rotation_input(self, dt: float):
        """Apply rotation torque based on player input"""
        rotation_input = 0.0

        if self.input_rotate_right:
            rotation_input += 1.0
        if self.input_rotate_left:
            rotation_input -= 1.0

        # Supervolt: both keys pressed = faster clockwise rotation
        if self.input_rotate_left and self.input_rotate_right:
            rotation_input = 1.5  # Faster clockwise

        self.angular_velocity += rotation_input * PhysicsConstants.ROTATION_TORQUE * dt

        # Apply damping to angular velocity
        self.angular_velocity *= 0.95

    def apply_acceleration(self, dt: float):
        """Apply acceleration force to rear wheel (rear-wheel drive)"""
        if self.input_accelerate and self.rear_wheel.touching_ground:
            # Direction along the ground
            accel_dir = Vec2(math.cos(self.rotation), math.sin(self.rotation))
            accel_force = accel_dir * PhysicsConstants.ACCELERATION_FORCE
            self.rear_wheel.velocity = self.rear_wheel.velocity + accel_force * dt

    def apply_brake(self, dt: float):
        """Apply braking force to both wheels"""
        if self.input_brake:
            # Brake reduces velocity significantly
            self.rear_wheel.velocity = self.rear_wheel.velocity * PhysicsConstants.BRAKE_FRICTION
            self.front_wheel.velocity = self.front_wheel.velocity * PhysicsConstants.BRAKE_FRICTION

    def apply_spring_forces(self, dt: float):
        """Apply spring-damper forces between wheels and bike center"""
        # Force from rear wheel
        rear_force = self.rear_wheel.update_spring_force(
            self.position, self.velocity, self.rotation
        )

        # Force from front wheel
        front_force = self.front_wheel.update_spring_force(
            self.position, self.velocity, self.rotation
        )

        # Total force on bike center
        total_force = rear_force + front_force

        # Apply to bike center (using simplified mass model)
        self.velocity = self.velocity + total_force * dt * 0.1

        # Apply opposite force to wheels
        self.rear_wheel.velocity = self.rear_wheel.velocity - rear_force * dt * 0.5
        self.front_wheel.velocity = self.front_wheel.velocity - front_force * dt * 0.5

    def apply_friction(self):
        """Apply ground and air friction"""
        # Ground friction for wheels
        if self.rear_wheel.touching_ground:
            self.rear_wheel.velocity = self.rear_wheel.velocity * PhysicsConstants.GROUND_FRICTION
        if self.front_wheel.touching_ground:
            self.front_wheel.velocity = self.front_wheel.velocity * PhysicsConstants.GROUND_FRICTION

        # Air resistance for everything
        self.velocity = self.velocity * PhysicsConstants.AIR_RESISTANCE
        self.rear_wheel.velocity = self.rear_wheel.velocity * PhysicsConstants.AIR_RESISTANCE
        self.front_wheel.velocity = self.front_wheel.velocity * PhysicsConstants.AIR_RESISTANCE

    def integrate(self, dt: float):
        """Integrate velocities to update positions"""
        # Update positions
        self.position = self.position + self.velocity * dt
        self.rear_wheel.position = self.rear_wheel.position + self.rear_wheel.velocity * dt
        self.front_wheel.position = self.front_wheel.position + self.front_wheel.velocity * dt

        # Update rotation
        self.rotation += self.angular_velocity * dt

        # Keep rotation in reasonable range
        if self.rotation > math.pi:
            self.rotation -= 2 * math.pi
        elif self.rotation < -math.pi:
            self.rotation += 2 * math.pi

    def check_wheel_collision(self, wheel: Wheel, terrain: List[Line]) -> bool:
        """
        Check and resolve collision for a wheel against terrain
        Returns True if collision occurred
        """
        wheel.touching_ground = False
        min_penetration = float('inf')
        best_contact_point = None
        best_normal = None

        for line in terrain:
            contact_point, distance = line.closest_point_on_line(wheel.position)
            penetration = PhysicsConstants.WHEEL_RADIUS - distance

            if penetration > 0 and penetration < min_penetration:
                min_penetration = penetration
                best_contact_point = contact_point
                best_normal = line.normal()

        if best_contact_point is not None:
            # Project wheel out of terrain
            wheel.position = best_contact_point + best_normal * PhysicsConstants.WHEEL_RADIUS

            # Mark as touching ground
            wheel.touching_ground = True
            wheel.ground_point = best_contact_point
            wheel.ground_normal = best_normal

            # Apply collision response (reduce velocity in normal direction)
            velocity_along_normal = wheel.velocity.dot(best_normal)
            if velocity_along_normal > 0:  # Moving into ground
                # Remove normal component and apply elasticity
                normal_vel = best_normal * velocity_along_normal
                wheel.velocity = wheel.velocity - normal_vel * (1 + PhysicsConstants.COLLISION_ELASTICITY)

            return True

        return False

    def check_head_collision(self, terrain: List[Line]) -> bool:
        """
        Check if head collides with terrain (instant death)
        Returns True if collision occurred
        """
        head_pos = self.get_head_position()

        for line in terrain:
            contact_point, distance = line.closest_point_on_line(head_pos)
            if distance < PhysicsConstants.HEAD_RADIUS:
                return True

        return False

    def update(self, dt: float, terrain: List[Line]):
        """Main physics update loop"""
        if not self.alive:
            return

        # Apply forces
        self.apply_gravity(dt)
        self.apply_rotation_input(dt)
        self.apply_acceleration(dt)
        self.apply_brake(dt)
        self.apply_spring_forces(dt)
        self.apply_friction()

        # Integrate
        self.integrate(dt)

        # Collision detection and response
        self.check_wheel_collision(self.rear_wheel, terrain)
        self.check_wheel_collision(self.front_wheel, terrain)

        # Check if head hit anything (death)
        if self.check_head_collision(terrain):
            self.alive = False

        # Update ground status
        self.on_ground = self.rear_wheel.touching_ground or self.front_wheel.touching_ground

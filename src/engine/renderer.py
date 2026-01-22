"""
Rendering system for Bungee Biker
Handles all 2D graphics rendering
"""

import pygame
import math
from typing import List, Tuple
from .physics import Vec2, Line, Bike


class Camera:
    """Camera that follows the player"""

    def __init__(self, screen_width: int, screen_height: int):
        self.position = Vec2(0, 0)
        self.target_position = Vec2(0, 0)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.zoom = 30.0  # Pixels per meter
        self.smooth_factor = 0.1

    def update(self, target: Vec2):
        """Smoothly follow target position"""
        self.target_position = target
        # Smooth camera movement
        diff = self.target_position - self.position
        self.position = self.position + diff * self.smooth_factor

    def world_to_screen(self, world_pos: Vec2) -> Tuple[int, int]:
        """Convert world coordinates to screen coordinates"""
        screen_x = int((world_pos.x - self.position.x) * self.zoom + self.screen_width / 2)
        screen_y = int((world_pos.y - self.position.y) * self.zoom + self.screen_height / 2)
        return (screen_x, screen_y)

    def world_to_screen_scale(self, world_size: float) -> int:
        """Convert world size to screen pixels"""
        return int(world_size * self.zoom)


class Colors:
    """Color palette"""
    SKY = (135, 206, 235)  # Light blue sky
    GROUND = (34, 139, 34)  # Green grass
    TERRAIN_OUTLINE = (20, 80, 20)  # Dark green
    BIKE_BODY = (200, 0, 0)  # Red
    BIKE_WHEEL = (50, 50, 50)  # Dark gray
    HEAD = (255, 200, 150)  # Skin tone
    APPLE = (255, 0, 0)  # Red
    FLOWER = (255, 215, 0)  # Gold
    KILLER = (128, 128, 128)  # Gray
    KILLER_SPIKES = (255, 0, 0)  # Red spikes
    UI_TEXT = (255, 255, 255)  # White
    UI_SHADOW = (0, 0, 0)  # Black


class Renderer:
    """Main rendering class"""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.camera = Camera(screen.get_width(), screen.get_height())
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

    def clear(self):
        """Clear screen with sky color"""
        self.screen.fill(Colors.SKY)

    def draw_terrain(self, terrain: List[Line], is_ground: List[bool]):
        """Draw terrain polygons"""
        for i, line in enumerate(terrain):
            p1_screen = self.camera.world_to_screen(line.p1)
            p2_screen = self.camera.world_to_screen(line.p2)

            # Draw ground lines thicker and green
            color = Colors.GROUND if (i < len(is_ground) and is_ground[i]) else Colors.TERRAIN_OUTLINE
            width = 3 if (i < len(is_ground) and is_ground[i]) else 2

            pygame.draw.line(self.screen, color, p1_screen, p2_screen, width)

    def draw_bike(self, bike: Bike):
        """Draw the bike with wheels and rider"""
        # Draw connection lines (bike frame)
        center_screen = self.camera.world_to_screen(bike.position)
        rear_screen = self.camera.world_to_screen(bike.rear_wheel.position)
        front_screen = self.camera.world_to_screen(bike.front_wheel.position)
        head_screen = self.camera.world_to_screen(bike.get_head_position())

        # Frame
        pygame.draw.line(self.screen, Colors.BIKE_BODY, center_screen, rear_screen, 2)
        pygame.draw.line(self.screen, Colors.BIKE_BODY, center_screen, front_screen, 2)
        pygame.draw.line(self.screen, Colors.BIKE_BODY, center_screen, head_screen, 2)

        # Wheels
        wheel_radius = self.camera.world_to_screen_scale(0.4)
        pygame.draw.circle(self.screen, Colors.BIKE_WHEEL, rear_screen, wheel_radius, 2)
        pygame.draw.circle(self.screen, Colors.BIKE_WHEEL, front_screen, wheel_radius, 2)

        # Wheel spokes (for rotation visualization)
        spoke_angle = bike.rotation
        for wheel_pos in [rear_screen, front_screen]:
            spoke_end_x = wheel_pos[0] + int(wheel_radius * math.cos(spoke_angle))
            spoke_end_y = wheel_pos[1] + int(wheel_radius * math.sin(spoke_angle))
            pygame.draw.line(self.screen, Colors.BIKE_WHEEL, wheel_pos, (spoke_end_x, spoke_end_y), 1)

        # Head
        head_radius = self.camera.world_to_screen_scale(0.3)
        pygame.draw.circle(self.screen, Colors.HEAD, head_screen, head_radius)
        pygame.draw.circle(self.screen, Colors.TERRAIN_OUTLINE, head_screen, head_radius, 1)

        # Center dot (for debugging)
        pygame.draw.circle(self.screen, Colors.BIKE_BODY, center_screen, 3)

    def draw_apple(self, position: Vec2, collected: bool = False):
        """Draw an apple collectible"""
        if collected:
            return

        screen_pos = self.camera.world_to_screen(position)
        radius = self.camera.world_to_screen_scale(0.25)

        # Draw apple as red circle
        pygame.draw.circle(self.screen, Colors.APPLE, screen_pos, radius)
        pygame.draw.circle(self.screen, (150, 0, 0), screen_pos, radius, 2)

        # Small highlight
        highlight_pos = (screen_pos[0] - radius // 3, screen_pos[1] - radius // 3)
        pygame.draw.circle(self.screen, (255, 150, 150), highlight_pos, radius // 3)

    def draw_flower(self, position: Vec2, unlocked: bool = True):
        """Draw the goal flower"""
        screen_pos = self.camera.world_to_screen(position)
        radius = self.camera.world_to_screen_scale(0.4)

        # Color based on locked/unlocked
        color = Colors.FLOWER if unlocked else (128, 128, 128)

        # Draw flower as star shape
        points = []
        for i in range(8):
            angle = i * math.pi / 4
            r = radius if i % 2 == 0 else radius // 2
            x = screen_pos[0] + int(r * math.cos(angle))
            y = screen_pos[1] + int(r * math.sin(angle))
            points.append((x, y))

        pygame.draw.polygon(self.screen, color, points)
        pygame.draw.polygon(self.screen, (200, 150, 0), points, 2)

        # Center
        pygame.draw.circle(self.screen, (255, 100, 0), screen_pos, radius // 3)

    def draw_killer(self, position: Vec2, rotation: float):
        """Draw a rotating killer spike"""
        screen_pos = self.camera.world_to_screen(position)
        radius = self.camera.world_to_screen_scale(0.5)

        # Draw base circle
        pygame.draw.circle(self.screen, Colors.KILLER, screen_pos, radius)

        # Draw spikes
        num_spikes = 8
        for i in range(num_spikes):
            angle = rotation + i * 2 * math.pi / num_spikes
            spike_length = radius * 1.5
            spike_end_x = screen_pos[0] + int(spike_length * math.cos(angle))
            spike_end_y = screen_pos[1] + int(spike_length * math.sin(angle))

            # Draw spike as triangle
            side_angle1 = angle - math.pi / 16
            side_angle2 = angle + math.pi / 16
            base_len = radius * 0.8

            p1 = (screen_pos[0] + int(base_len * math.cos(side_angle1)),
                  screen_pos[1] + int(base_len * math.sin(side_angle1)))
            p2 = (screen_pos[0] + int(base_len * math.cos(side_angle2)),
                  screen_pos[1] + int(base_len * math.sin(side_angle2)))
            p3 = (spike_end_x, spike_end_y)

            pygame.draw.polygon(self.screen, Colors.KILLER_SPIKES, [p1, p2, p3])
            pygame.draw.polygon(self.screen, (100, 0, 0), [p1, p2, p3], 1)

    def draw_text(self, text: str, position: Tuple[int, int], color=Colors.UI_TEXT, shadow=True):
        """Draw text with optional shadow"""
        if shadow:
            shadow_surf = self.font.render(text, True, Colors.UI_SHADOW)
            self.screen.blit(shadow_surf, (position[0] + 2, position[1] + 2))

        text_surf = self.font.render(text, True, color)
        self.screen.blit(text_surf, position)

    def draw_small_text(self, text: str, position: Tuple[int, int], color=Colors.UI_TEXT):
        """Draw smaller text"""
        text_surf = self.small_font.render(text, True, color)
        self.screen.blit(text_surf, position)

    def draw_timer(self, time: float):
        """Draw game timer"""
        minutes = int(time // 60)
        seconds = int(time % 60)
        hundredths = int((time % 1) * 100)
        time_str = f"{minutes:02d}:{seconds:02d}:{hundredths:02d}"

        self.draw_text(time_str, (self.screen.get_width() - 200, 20))

    def draw_apple_counter(self, collected: int, total: int):
        """Draw apple collection counter"""
        if total == 0:
            return

        counter_str = f"Apples: {collected}/{total}"
        self.draw_text(counter_str, (20, 20))

    def draw_death_message(self):
        """Draw death message"""
        msg = "CRASHED! Press R to restart"
        text_surf = self.font.render(msg, True, Colors.UI_TEXT)
        rect = text_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        # Background
        bg_rect = pygame.Rect(rect.left - 20, rect.top - 10, rect.width + 40, rect.height + 20)
        pygame.draw.rect(self.screen, (0, 0, 0, 128), bg_rect)
        pygame.draw.rect(self.screen, Colors.UI_TEXT, bg_rect, 2)

        self.screen.blit(text_surf, rect)

    def draw_completion_message(self, time: float):
        """Draw level completion message"""
        minutes = int(time // 60)
        seconds = int(time % 60)
        hundredths = int((time % 1) * 100)
        time_str = f"{minutes:02d}:{seconds:02d}:{hundredths:02d}"

        msg1 = "Level Complete!"
        msg2 = f"Time: {time_str}"
        msg3 = "Press R to restart or N for next level"

        y_offset = self.screen.get_height() // 2 - 60

        for i, msg in enumerate([msg1, msg2, msg3]):
            font = self.font if i < 2 else self.small_font
            text_surf = font.render(msg, True, Colors.UI_TEXT)
            rect = text_surf.get_rect(center=(self.screen.get_width() // 2, y_offset + i * 40))

            # Background
            bg_rect = pygame.Rect(rect.left - 20, rect.top - 10, rect.width + 40, rect.height + 20)
            pygame.draw.rect(self.screen, (0, 0, 0, 128), bg_rect)

            self.screen.blit(text_surf, rect)

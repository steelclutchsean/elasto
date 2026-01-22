"""
Main game class for Bungee Biker
Manages game state, input, and updates
"""

import pygame
from ..engine.physics import Bike, PhysicsConstants
from ..engine.renderer import Renderer
from .level import Level, create_test_level, create_flat_track


class GameState:
    """Game state enum"""
    MENU = 0
    PLAYING = 1
    PAUSED = 2
    LEVEL_COMPLETE = 3
    DEAD = 4


class Game:
    """Main game class"""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.renderer = Renderer(screen)
        self.clock = pygame.time.Clock()

        # Game state
        self.state = GameState.PLAYING
        self.running = True

        # Physics accumulator for fixed timestep
        self.accumulator = 0.0
        self.fixed_dt = PhysicsConstants.FIXED_DT

        # Current level
        self.current_level = create_test_level()
        self.bike = Bike(self.current_level.start_position)

        # Input state
        self.keys = {
            'up': False,
            'down': False,
            'left': False,
            'right': False,
            'space': False,
        }

    def handle_input(self):
        """Process input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)

            elif event.type == pygame.KEYUP:
                self._handle_keyup(event.key)

    def _handle_keydown(self, key):
        """Handle key press"""
        # Movement keys
        if key == pygame.K_UP:
            self.keys['up'] = True
        elif key == pygame.K_DOWN:
            self.keys['down'] = True
        elif key == pygame.K_LEFT:
            self.keys['left'] = True
        elif key == pygame.K_RIGHT:
            self.keys['right'] = True
        elif key == pygame.K_SPACE:
            self.turn_bike()

        # Game control keys
        elif key == pygame.K_ESCAPE:
            self.running = False
        elif key == pygame.K_r:
            self.restart_level()
        elif key == pygame.K_n:
            if self.state == GameState.LEVEL_COMPLETE:
                self.next_level()
        elif key == pygame.K_1:
            self.load_level(create_flat_track())
        elif key == pygame.K_2:
            self.load_level(create_test_level())

    def _handle_keyup(self, key):
        """Handle key release"""
        if key == pygame.K_UP:
            self.keys['up'] = False
        elif key == pygame.K_DOWN:
            self.keys['down'] = False
        elif key == pygame.K_LEFT:
            self.keys['left'] = False
        elif key == pygame.K_RIGHT:
            self.keys['right'] = False

    def turn_bike(self):
        """Flip bike direction 180 degrees"""
        import math
        self.bike.rotation += math.pi
        self.bike.velocity.x *= -1

    def restart_level(self):
        """Restart current level"""
        self.current_level.reset()
        self.bike = Bike(self.current_level.start_position)
        self.state = GameState.PLAYING

    def load_level(self, level: Level):
        """Load a new level"""
        self.current_level = level
        self.bike = Bike(self.current_level.start_position)
        self.state = GameState.PLAYING

    def next_level(self):
        """Load next level (placeholder)"""
        # For now, just restart current level
        self.restart_level()

    def update_input(self):
        """Update bike input state from key state"""
        self.bike.input_accelerate = self.keys['up']
        self.bike.input_brake = self.keys['down']
        self.bike.input_rotate_left = self.keys['left']
        self.bike.input_rotate_right = self.keys['right']

    def update(self, dt: float):
        """Update game state"""
        if self.state != GameState.PLAYING:
            return

        # Update input
        self.update_input()

        # Fixed timestep physics updates
        self.accumulator += dt

        # Prevent spiral of death (cap accumulator)
        if self.accumulator > 0.2:
            self.accumulator = 0.2

        # Run physics updates at fixed rate
        while self.accumulator >= self.fixed_dt:
            self.bike.update(self.fixed_dt, self.current_level.terrain)
            self.current_level.update(self.fixed_dt, self.bike)
            self.accumulator -= self.fixed_dt

        # Update camera to follow bike
        self.renderer.camera.update(self.bike.position)

        # Check game state changes
        if self.current_level.completed:
            self.state = GameState.LEVEL_COMPLETE
        elif not self.bike.alive:
            self.state = GameState.DEAD

    def render(self):
        """Render game"""
        self.renderer.clear()

        # Draw terrain
        self.renderer.draw_terrain(self.current_level.terrain, self.current_level.is_ground)

        # Draw objects
        for apple in self.current_level.apples:
            self.renderer.draw_apple(apple.position, apple.collected)

        for killer in self.current_level.killers:
            self.renderer.draw_killer(killer.position, killer.rotation)

        if self.current_level.flower:
            flower_unlocked = self.current_level.is_flower_unlocked()
            self.renderer.draw_flower(self.current_level.flower.position, flower_unlocked)

        # Draw bike
        self.renderer.draw_bike(self.bike)

        # Draw UI
        self.renderer.draw_timer(self.current_level.time)
        self.renderer.draw_apple_counter(
            self.current_level.get_collected_apples(),
            self.current_level.get_total_apples()
        )

        # Draw state-specific overlays
        if self.state == GameState.DEAD:
            self.renderer.draw_death_message()
        elif self.state == GameState.LEVEL_COMPLETE:
            self.renderer.draw_completion_message(self.current_level.completion_time)

        # Draw controls help
        help_text = "Controls: Arrows=Move, Space=Turn, R=Restart, 1/2=Change Level, ESC=Quit"
        self.renderer.draw_small_text(help_text, (10, self.screen.get_height() - 30))

        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while self.running:
            # Calculate delta time
            dt = self.clock.tick(60) / 1000.0  # 60 FPS target, dt in seconds

            # Handle input
            self.handle_input()

            # Update game
            self.update(dt)

            # Render
            self.render()

        pygame.quit()

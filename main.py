#!/usr/bin/env python3
"""
Bungee Biker - Main Entry Point
A 1:1 clone of Elasto Mania
"""

import pygame
import sys

from src.game.game import Game


def main():
    """Main entry point"""
    # Initialize Pygame
    pygame.init()

    # Set up display
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Bungee Biker - Alpha v0.1")

    # Create and run game
    game = Game(screen)
    game.run()


if __name__ == "__main__":
    main()

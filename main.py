#!/usr/bin/env python3
"""
Snake Game v2 - PyGame Implementation
Entry point for the game.
"""
import pygame
from src.game import Game


def main():
    """Main entry point for the Snake game."""
    # Initialize pygame
    pygame.init()
    
    # Set up display
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Snake Game v2")
    
    # Create and run the game
    game = Game(screen)
    game.run()


if __name__ == '__main__':
    main()

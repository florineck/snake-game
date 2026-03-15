"""Input handler for the Snake game."""
import pygame
from src.snake import Direction


class InputHandler:
    """Handles keyboard input for the game."""
    
    def __init__(self):
        """Initialize the input handler."""
        self.quit_requested = False
        self.restart_requested = False
        self.pause_toggle_requested = False
    
    def process_events(self) -> dict:
        """
        Process pygame events and return action flags.
        
        Returns:
            Dictionary with action flags:
            - 'direction': New direction or None
            - 'quit': True if quit requested
            - 'restart': True if restart requested
            - 'pause': True if pause toggle requested
        """
        direction = None
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_requested = True
                return {'quit': True}
            
            if event.type == pygame.KEYDOWN:
                # Quit
                if event.key == pygame.K_ESCAPE:
                    self.quit_requested = True
                    return {'quit': True}
                
                # Restart
                if event.key == pygame.K_r:
                    self.restart_requested = True
                    return {'restart': True}
                
                # Pause
                if event.key == pygame.K_SPACE:
                    self.pause_toggle_requested = True
                    return {'pause': True}
                
                # Direction controls
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    direction = Direction.UP
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    direction = Direction.DOWN
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    direction = Direction.RIGHT
        
        return {
            'direction': direction,
            'quit': False,
            'restart': False,
            'pause': False,
        }
    
    def reset_flags(self) -> None:
        """Reset the one-time action flags."""
        self.restart_requested = False
        self.pause_toggle_requested = False

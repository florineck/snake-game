"""Food entity for the Snake game."""
import random
from typing import Set, Tuple


class Food:
    """Represents food that the snake can eat."""
    
    def __init__(self, grid):
        """
        Initialize the food.
        
        Args:
            grid: The Grid instance for position calculations
        """
        self.grid = grid
        self.position = (0, 0)
        self.spawn()
    
    def spawn(self, occupied_positions: Set[Tuple[int, int]] = None) -> None:
        """
        Spawn food at a random position.
        
        Args:
            occupied_positions: Set of (x, y) positions that are occupied by the snake
        """
        if occupied_positions is None:
            occupied_positions = set()
        
        # Try to find an empty position
        max_attempts = 100
        for _ in range(max_attempts):
            x, y = self.grid.get_random_position()
            if (x, y) not in occupied_positions:
                self.position = (x, y)
                return
        
        # Fallback: just pick any random position if grid is almost full
        self.position = self.grid.get_random_position()
    
    @property
    def x(self) -> int:
        """Get the x coordinate of the food."""
        return self.position[0]
    
    @property
    def y(self) -> int:
        """Get the y coordinate of the food."""
        return self.position[1]
    
    def collides_with(self, x: int, y: int) -> bool:
        """
        Check if food collides with the given position.
        
        Args:
            x: X coordinate to check
            y: Y coordinate to check
            
        Returns:
            True if position matches food position
        """
        return self.position == (x, y)
    
    def get_pixel_position(self) -> Tuple[int, int]:
        """
        Get the pixel position for rendering.
        
        Returns:
            Tuple of (pixel_x, pixel_y) for the center of the food
        """
        pixel_x, pixel_y = self.grid.tile_to_pixel(self.x, self.y)
        # Center the food in the tile
        offset = self.grid.tile_size // 2
        return pixel_x + offset, pixel_y + offset

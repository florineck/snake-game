"""Snake entity for the Snake game."""
from enum import Enum
from typing import List, Tuple, Set


class Direction(Enum):
    """Possible directions for the snake."""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Snake:
    """Represents the snake in the game."""
    
    def __init__(self, grid, start_x: int = None, start_y: int = None):
        """
        Initialize the snake.
        
        Args:
            grid: The Grid instance for boundary checking
            start_x: Starting x position (defaults to center)
            start_y: Starting y position (defaults to center)
        """
        self.grid = grid
        
        # Default to center of grid
        if start_x is None:
            start_x = grid.width // 2
        if start_y is None:
            start_y = grid.height // 2
        
        # Snake body as list of (x, y) positions (head is first)
        self.body: List[Tuple[int, int]] = [
            (start_x, start_y),
            (start_x, start_y + 1),  # Body segment
            (start_x, start_y + 2),  # Tail
        ]
        
        self.direction = Direction.UP
        self.next_direction = Direction.UP
        self.grow_pending = 0
    
    @property
    def head(self) -> Tuple[int, int]:
        """Get the head position."""
        return self.body[0]
    
    @property
    def positions(self) -> List[Tuple[int, int]]:
        """Get all snake positions."""
        return self.body
    
    @property
    def position_set(self) -> Set[Tuple[int, int]]:
        """Get all snake positions as a set for O(1) lookups."""
        return set(self.body)
    
    def set_direction(self, direction: Direction) -> None:
        """
        Set the next direction (prevents 180° turns).
        
        Args:
            direction: The new direction
        """
        # Prevent 180° reversal
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }
        
        if direction != opposite_directions.get(self.direction):
            self.next_direction = direction
    
    def update_direction(self) -> None:
        """Apply the queued direction change."""
        self.direction = self.next_direction
    
    def move(self) -> None:
        """Move the snake one step in the current direction."""
        self.update_direction()
        
        head_x, head_y = self.head
        dx, dy = self.direction.value
        
        new_head = (head_x + dx, head_y + dy)
        
        # Add new head
        self.body.insert(0, new_head)
        
        # Remove tail unless growing
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()
    
    def grow(self, amount: int = 1) -> None:
        """
        Make the snake grow after eating food.
        
        Args:
            amount: Number of segments to grow
        """
        self.grow_pending += amount
    
    def check_collision(self) -> bool:
        """
        Check if the snake has collided with itself.
        
        Returns:
            True if head collides with body
        """
        head = self.head
        # Check if head is in any body segment (excluding head itself)
        return head in self.body[1:]
    
    def check_wall_collision(self) -> bool:
        """
        Check if the snake has collided with the wall.
        
        Returns:
            True if head is outside grid bounds
        """
        head_x, head_y = self.head
        return not self.grid.is_valid_position(head_x, head_y)
    
    def reset(self, start_x: int = None, start_y: int = None) -> None:
        """
        Reset the snake to starting position.
        
        Args:
            start_x: Starting x position
            start_y: Starting y position
        """
        if start_x is None:
            start_x = self.grid.width // 2
        if start_y is None:
            start_y = self.grid.height // 2
        
        self.body = [
            (start_x, start_y),
            (start_x, start_y + 1),
            (start_x, start_y + 2),
        ]
        self.direction = Direction.UP
        self.next_direction = Direction.UP
        self.grow_pending = 0
    
    def get_pixel_positions(self) -> List[Tuple[int, int]]:
        """
        Get pixel positions for all body segments.
        
        Returns:
            List of (pixel_x, pixel_y) tuples for each segment
        """
        positions = []
        for x, y in self.body:
            px, py = self.grid.tile_to_pixel(x, y)
            # Center in tile
            offset = self.grid.tile_size // 2
            positions.append((px + offset, py + offset))
        return positions

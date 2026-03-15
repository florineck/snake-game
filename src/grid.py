"""Grid coordinate system for the Snake game."""


class Grid:
    """Represents the game grid and handles coordinate conversions."""
    
    def __init__(self, width: int = 40, height: int = 30, tile_size: int = 20):
        """
        Initialize the grid.
        
        Args:
            width: Number of tiles horizontally
            height: Number of tiles vertically
            tile_size: Size of each tile in pixels
        """
        self.width = width
        self.height = height
        self.tile_size = tile_size
    
    @property
    def pixel_width(self) -> int:
        """Get the total width in pixels."""
        return self.width * self.tile_size
    
    @property
    def pixel_height(self) -> int:
        """Get the total height in pixels."""
        return self.height * self.tile_size
    
    def tile_to_pixel(self, x: int, y: int) -> tuple[int, int]:
        """
        Convert tile coordinates to pixel coordinates.
        
        Args:
            x: Tile x coordinate
            y: Tile y coordinate
            
        Returns:
            Tuple of (pixel_x, pixel_y) for the top-left corner of the tile
        """
        return x * self.tile_size, y * self.tile_size
    
    def pixel_to_tile(self, pixel_x: int, pixel_y: int) -> tuple[int, int]:
        """
        Convert pixel coordinates to tile coordinates.
        
        Args:
            pixel_x: Pixel x coordinate
            pixel_y: Pixel y coordinate
            
        Returns:
            Tuple of (tile_x, tile_y)
        """
        return pixel_x // self.tile_size, pixel_y // self.tile_size
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """
        Check if a tile position is within the grid bounds.
        
        Args:
            x: Tile x coordinate
            y: Tile y coordinate
            
        Returns:
            True if position is valid, False otherwise
        """
        return 0 <= x < self.width and 0 <= y < self.height
    
    def get_random_position(self) -> tuple[int, int]:
        """
        Get a random valid grid position.
        
        Returns:
            Tuple of (x, y) random grid coordinates
        """
        import random
        return random.randint(0, self.width - 1), random.randint(0, self.height - 1)
    
    def get_random_empty_position(self, occupied_positions: set[tuple[int, int]]) -> tuple[int, int]:
        """
        Get a random position that is not occupied.
        
        Args:
            occupied_positions: Set of (x, y) positions that are occupied
            
        Returns:
            Tuple of (x, y) random grid coordinates that are not occupied
        """
        import random
        while True:
            x, y = self.get_random_position()
            if (x, y) not in occupied_positions:
                return x, y

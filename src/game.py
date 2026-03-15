"""Main game class for the Snake game."""
from enum import Enum

from src.grid import Grid
from src.snake import Snake
from src.food import Food
from src.score_manager import ScoreManager
from src.input_handler import InputHandler
from src.renderer import Renderer


class GameState(Enum):
    """Game states."""
    READY = 'ready'
    PLAYING = 'playing'
    PAUSED = 'paused'
    GAMEOVER = 'gameover'


class Game:
    """Main game controller - coordinates all systems."""
    
    # Game settings
    TILE_SIZE = 20
    GRID_WIDTH = 40
    GRID_HEIGHT = 30
    FPS = 15  # Game speed (frames per second)
    
    def __init__(self, screen):
        """
        Initialize the game.
        
        Args:
            screen: PyGame display surface
        """
        self.screen = screen
        
        # Initialize grid
        self.grid = Grid(
            width=self.GRID_WIDTH,
            height=self.GRID_HEIGHT,
            tile_size=self.TILE_SIZE
        )
        
        # Initialize game components
        self.snake = Snake(self.grid)
        self.food = Food(self.grid)
        self.score_manager = ScoreManager()
        self.input_handler = InputHandler()
        self.renderer = Renderer(screen, self.grid)
        
        # Game state
        self.state = GameState.READY
        
        # Timing
        self.clock = pygame.time.Clock()
        self.move_timer = 0
        self.move_interval = 1000 // self.FPS  # Milliseconds between moves
    
    def handle_input(self) -> bool:
        """
        Process input events.
        
        Returns:
            False if quit requested, True otherwise
        """
        events = self.input_handler.process_events()
        
        # Handle quit
        if events.get('quit'):
            return False
        
        # Handle restart
        if events.get('restart'):
            self.reset()
            return True
        
        # Handle pause toggle
        if events.get('pause'):
            if self.state == GameState.PLAYING:
                self.state = GameState.PAUSED
            elif self.state == GameState.PAUSED:
                self.state = GameState.PLAYING
            return True
        
        # Handle direction changes
        direction = events.get('direction')
        if direction:
            # First direction input starts the game
            if self.state == GameState.READY:
                self.state = GameState.PLAYING
            
            if self.state == GameState.PLAYING:
                self.snake.set_direction(direction)
        
        return True
    
    def update(self) -> None:
        """Update game state."""
        if self.state != GameState.PLAYING:
            return
        
        # Move snake
        self.snake.move()
        
        # Check food collision
        if self.snake.head == self.food.position:
            self.snake.grow()
            self.score_manager.add_points()
            # Spawn new food at empty position
            self.food.spawn(self.snake.position_set)
        
        # Check wall collision
        if self.snake.check_wall_collision():
            self.state = GameState.GAMEOVER
            return
        
        # Check self collision
        if self.snake.check_collision():
            self.state = GameState.GAMEOVER
            return
    
    def reset(self) -> None:
        """Reset the game to initial state."""
        self.snake.reset()
        self.food.spawn(self.snake.position_set)
        self.score_manager.reset()
        self.state = GameState.READY
    
    def run(self) -> None:
        """Main game loop."""
        running = True
        
        while running:
            # Handle input
            running = self.handle_input()
            
            # Update game state
            self.update()
            
            # Render
            self.renderer.render(self)
            
            # Control frame rate
            self.clock.tick(self.FPS)
        
        # Clean up
        pygame.quit()


# Import pygame at module level for clock
import pygame

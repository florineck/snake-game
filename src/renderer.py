"""Renderer for the Snake game."""
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.game import Game


class Renderer:
    """Handles all visual rendering for the game."""
    
    # Color palette (matching the original)
    COLORS = {
        'background': (13, 17, 23),       # #0d1117
        'grid_lines': (74, 222, 128, 25), # rgba(74, 222, 128, 0.1) - converted to pygame
        'snake_head': (74, 222, 128),     # #4ade80
        'snake_body': (34, 197, 94),     # #22c55e
        'food': (239, 68, 68),            # #ef4444
        'ui_text': (232, 232, 232),      # #e8e8e8
        'score': (251, 191, 36),         # #fbbf24
        'paused': (100, 100, 100),
        'game_over': (239, 68, 68),
    }
    
    def __init__(self, screen: pygame.Surface, grid):
        """
        Initialize the renderer.
        
        Args:
            screen: PyGame display surface
            grid: The Grid instance
        """
        self.screen = screen
        self.grid = grid
        
        # Initialize fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 48)
        self.score_font = pygame.font.Font(None, 36)
        self.info_font = pygame.font.Font(None, 24)
    
    def render(self, game: 'Game') -> None:
        """
        Render the entire game.
        
        Args:
            game: The Game instance to render
        """
        # Clear screen
        self.screen.fill(self.COLORS['background'])
        
        # Draw grid
        self._draw_grid()
        
        # Draw food
        self._draw_food(game.food)
        
        # Draw snake
        self._draw_snake(game.snake)
        
        # Draw UI
        self._draw_score(game.score_manager)
        
        # Draw game state overlays
        if game.state == 'ready':
            self._draw_ready_screen()
        elif game.state == 'paused':
            self._draw_paused_screen()
        elif game.state == 'gameover':
            self._draw_game_over_screen(game.score_manager)
        
        # Update display
        pygame.display.flip()
    
    def _draw_grid(self) -> None:
        """Draw the grid lines."""
        # Create a surface for grid lines with alpha
        grid_surface = pygame.Surface(
            (self.grid.pixel_width, self.grid.pixel_height),
            pygame.SRCALPHA
        )
        
        # Vertical lines
        for x in range(self.grid.width + 1):
            pixel_x = x * self.grid.tile_size
            pygame.draw.line(
                grid_surface,
                self.COLORS['grid_lines'],
                (pixel_x, 0),
                (pixel_x, self.grid.pixel_height)
            )
        
        # Horizontal lines
        for y in range(self.grid.height + 1):
            pixel_y = y * self.grid.tile_size
            pygame.draw.line(
                grid_surface,
                self.COLORS['grid_lines'],
                (0, pixel_y),
                (self.grid.pixel_width, pixel_y)
            )
        
        self.screen.blit(grid_surface, (0, 0))
    
    def _draw_food(self, food) -> None:
        """Draw the food."""
        pixel_x, pixel_y = food.get_pixel_position()
        
        # Draw glow effect (larger, semi-transparent circle)
        glow_radius = self.grid.tile_size // 2 + 4
        glow_surface = pygame.Surface(
            (glow_radius * 2, glow_radius * 2),
            pygame.SRCALPHA
        )
        pygame.draw.circle(
            glow_surface,
            (*self.COLORS['food'][:3], 80),
            (glow_radius, glow_radius),
            glow_radius
        )
        self.screen.blit(
            glow_surface,
            (pixel_x - glow_radius, pixel_y - glow_radius)
        )
        
        # Draw food circle
        radius = self.grid.tile_size // 2 - 2
        pygame.draw.circle(
            self.screen,
            self.COLORS['food'],
            (pixel_x, pixel_y),
            radius
        )
    
    def _draw_snake(self, snake) -> None:
        """Draw the snake."""
        positions = snake.get_pixel_positions()
        
        # Draw body segments (from tail to head for proper layering)
        for i in range(len(positions) - 1, 0, -1):
            x, y = positions[i]
            radius = self.grid.tile_size // 2 - 1
            
            pygame.draw.circle(
                self.screen,
                self.COLORS['snake_body'],
                (x, y),
                radius
            )
        
        # Draw head
        if positions:
            head_x, head_y = positions[0]
            radius = self.grid.tile_size // 2 - 1
            
            # Head is slightly larger and brighter
            pygame.draw.circle(
                self.screen,
                self.COLORS['snake_head'],
                (head_x, head_y),
                radius
            )
    
    def _draw_score(self, score_manager) -> None:
        """Draw the score display."""
        # Current score
        score_text = f"Score: {score_manager.score}"
        score_surface = self.score_font.render(
            score_text,
            True,
            self.COLORS['score']
        )
        self.screen.blit(score_surface, (20, 10))
        
        # High score
        high_score_text = f"High Score: {score_manager.high_score}"
        high_score_surface = self.info_font.render(
            high_score_text,
            True,
            self.COLORS['ui_text']
        )
        self.screen.blit(
            high_score_surface,
            (20, 50)
        )
    
    def _draw_ready_screen(self) -> None:
        """Draw the ready/start screen overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface(
            (self.grid.pixel_width, self.grid.pixel_height),
            pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Title
        title = self.title_font.render("Snake Game", True, self.COLORS['snake_head'])
        title_rect = title.get_rect(
            center=(self.grid.pixel_width // 2, self.grid.pixel_height // 2 - 40)
        )
        self.screen.blit(title, title_rect)
        
        # Instructions
        instructions = [
            "Press any arrow key to start",
            "Arrow Keys or WASD to move",
            "Space to pause",
            "R to restart",
            "ESC to quit",
        ]
        
        y_offset = self.grid.pixel_height // 2 + 20
        for line in instructions:
            text = self.info_font.render(line, True, self.COLORS['ui_text'])
            rect = text.get_rect(center=(self.grid.pixel_width // 2, y_offset))
            self.screen.blit(text, rect)
            y_offset += 30
    
    def _draw_paused_screen(self) -> None:
        """Draw the paused screen overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface(
            (self.grid.pixel_width, self.grid.pixel_height),
            pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Paused text
        paused_text = self.title_font.render("PAUSED", True, self.COLORS['ui_text'])
        rect = paused_text.get_rect(
            center=(self.grid.pixel_width // 2, self.grid.pixel_height // 2)
        )
        self.screen.blit(paused_text, rect)
        
        # Resume instruction
        resume_text = self.info_font.render("Press Space to resume", True, self.COLORS['ui_text'])
        resume_rect = resume_text.get_rect(
            center=(self.grid.pixel_width // 2, self.grid.pixel_height // 2 + 40)
        )
        self.screen.blit(resume_text, resume_rect)
    
    def _draw_game_over_screen(self, score_manager) -> None:
        """Draw the game over screen overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface(
            (self.grid.pixel_width, self.grid.pixel_height),
            pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = self.title_font.render("GAME OVER", True, self.COLORS['game_over'])
        rect = game_over_text.get_rect(
            center=(self.grid.pixel_width // 2, self.grid.pixel_height // 2 - 40)
        )
        self.screen.blit(game_over_text, rect)
        
        # Final score
        score_text = self.score_font.render(
            f"Final Score: {score_manager.score}",
            True,
            self.COLORS['score']
        )
        score_rect = score_text.get_rect(
            center=(self.grid.pixel_width // 2, self.grid.pixel_height // 2 + 20)
        )
        self.screen.blit(score_text, score_rect)
        
        # High score
        if score_manager.score >= score_manager.high_score:
            new_high_text = self.info_font.render(
                "New High Score!",
                True,
                self.COLORS['snake_head']
            )
            new_high_rect = new_high_text.get_rect(
                center=(self.grid.pixel_width // 2, self.grid.pixel_height // 2 + 60)
            )
            self.screen.blit(new_high_text, new_high_rect)
            y_offset = 100
        else:
            y_offset = 60
        
        # Restart instruction
        restart_text = self.info_font.render(
            "Press R to restart",
            True,
            self.COLORS['ui_text']
        )
        restart_rect = restart_text.get_rect(
            center=(self.grid.pixel_width // 2, self.grid.pixel_height // 2 + y_offset)
        )
        self.screen.blit(restart_text, restart_rect)

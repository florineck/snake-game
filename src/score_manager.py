"""Score manager for the Snake game."""
import json
import os
from pathlib import Path


class ScoreManager:
    """Manages current score and high score persistence."""
    
    def __init__(self):
        """Initialize the score manager."""
        self.score = 0
        self.high_score = 0
        self.high_score_file = self._get_high_score_path()
        self.load_high_score()
    
    def _get_high_score_path(self) -> Path:
        """
        Get the path to the high score file.
        
        Returns:
            Path to the high score JSON file
        """
        # Use ~/.snake_game/highscore.json
        home_dir = Path.home()
        game_dir = home_dir / ".snake_game"
        game_dir.mkdir(exist_ok=True)
        return game_dir / "highscore.json"
    
    def load_high_score(self) -> None:
        """Load high score from file."""
        try:
            if self.high_score_file.exists():
                with open(self.high_score_file, 'r') as f:
                    data = json.load(f)
                    self.high_score = data.get('high_score', 0)
        except (json.JSONDecodeError, IOError):
            self.high_score = 0
    
    def save_high_score(self) -> None:
        """Save high score to file."""
        try:
            with open(self.high_score_file, 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except IOError:
            pass  # Silently fail if we can't save
    
    def add_points(self, points: int = 1) -> None:
        """
        Add points to the current score.
        
        Args:
            points: Number of points to add
        """
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
    
    def reset(self) -> None:
        """Reset the current score (high score persists)."""
        self.score = 0
    
    def reset_all(self) -> None:
        """Reset both current score and high score."""
        self.score = 0
        self.high_score = 0
        self.save_high_score()

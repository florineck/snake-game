# Snake Game v2 - PyGame Architecture Plan

## Project Overview
Refactor the existing JavaScript Snake game to Python using PyGame, maintaining feature parity while leveraging PyGame's capabilities.

## File Structure

```
snake-game-v2/
├── requirements.txt        # PyGame dependency
├── main.py                 # Entry point, game loop
├── src/
│   ├── __init__.py
│   ├── game.py             # Main game class
│   ├── snake.py            # Snake entity class
│   ├── food.py             # Food entity class
│   ├── grid.py             # Grid system
│   ├── input_handler.py    # Keyboard input
│   ├── score_manager.py    # Score/high score persistence
│   └── renderer.py         # Drawing/rendering logic
└── .gitignore
```

## Core Classes Design

### 1. Game (src/game.py)
Main game controller - coordinates all systems.
- Game state management, game loop, collision detection, score tracking

### 2. Snake (src/snake.py)
Represents the snake entity.
- Movement, growth, direction management, self-collision detection

### 3. Food (src/food.py)
Food entity with random spawning.
- Random position generation, collision with snake

### 4. Grid (src/grid.py)
Grid coordinate system.
- Define game boundaries, tile-to-pixel conversion

### 5. Input Handler (src/input_handler.py)
Keyboard input processing.
- Map keys to directions, prevent 180° reversals

### 6. Score Manager (src/score_manager.py)
Score persistence using JSON.
- Track current score, persist high score to file

### 7. Renderer (src/renderer.py)
PyGame drawing operations.
- All visual rendering, colors, fonts, glow effects

## Color Palette (Matching Original)

| Element | Color |
|---------|-------|
| Background | #0d1117 |
| Grid lines | rgba(74, 222, 128, 0.1) |
| Snake Head | #4ade80 |
| Snake Body | #22c55e |
| Food | #ef4444 |
| UI Text | #e8e8e8 |
| Score | #fbbf24 |

## Game States
- **Ready**: Initial state, waiting for input
- **Playing**: Active gameplay
- **Paused**: Game paused (Space)
- **GameOver**: Collision occurred

## Key Mappings
- Arrow Keys / WASD: Direction
- Space: Pause/Resume
- R: Restart
- Escape: Quit

## Dependencies
```
pygame>=2.5.0
```

## High Score Storage
- Location: ~/.snake_game/highscore.json
- Format: {"high_score": 0}

## Implementation Order
1. Create project structure
2. Grid class
3. Food class  
4. Snake class
5. ScoreManager
6. InputHandler
7. Renderer
8. Game class (main controller)
9. main.py entry point
10. Test and verify

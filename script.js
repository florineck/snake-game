// Snake Game JavaScript

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreElement = document.getElementById('score');
const highScoreElement = document.getElementById('highScore');
const statusElement = document.getElementById('status');

// Game constants
const GRID_SIZE = 20;
const TILE_COUNT = canvas.width / GRID_SIZE;
const GAME_SPEED = 100;

// Game state
let snake = [];
let food = { x: 0, y: 0 };
let direction = { x: 0, y: 0 };
let nextDirection = { x: 0, y: 0 };
let score = 0;
let highScore = parseInt(localStorage.getItem('snakeHighScore')) || 0;
let gameLoop = null;
let isPaused = false;
let isGameOver = false;
let hasStarted = false;

// Initialize high score display
highScoreElement.textContent = highScore;

// Initialize game
function initGame() {
  snake = [
    { x: 10, y: 10 },
    { x: 10, y: 11 },
    { x: 10, y: 12 }
  ];
  direction = { x: 0, y: -1 };
  nextDirection = { x: 0, y: -1 };
  score = 0;
  isPaused = false;
  isGameOver = false;
  hasStarted = false;
  scoreElement.textContent = score;
  statusElement.textContent = 'Press any direction key to start.';
  statusElement.className = 'status';
  spawnFood();
  draw();
}

// Spawn food at random position
function spawnFood() {
  let validPosition = false;
  while (!validPosition) {
    food.x = Math.floor(Math.random() * TILE_COUNT);
    food.y = Math.floor(Math.random() * TILE_COUNT);
    
    validPosition = !snake.some(segment => 
      segment.x === food.x && segment.y === food.y
    );
  }
}

// Draw game elements
function draw() {
  // Clear canvas
  ctx.fillStyle = '#0d1117';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Draw grid (subtle)
  ctx.strokeStyle = 'rgba(74, 222, 128, 0.1)';
  ctx.lineWidth = 1;
  for (let i = 0; i <= TILE_COUNT; i++) {
    ctx.beginPath();
    ctx.moveTo(i * GRID_SIZE, 0);
    ctx.lineTo(i * GRID_SIZE, canvas.height);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(0, i * GRID_SIZE);
    ctx.lineTo(canvas.width, i * GRID_SIZE);
    ctx.stroke();
  }

  // Draw food
  ctx.fillStyle = '#ef4444';
  ctx.shadowColor = '#ef4444';
  ctx.shadowBlur = 10;
  ctx.beginPath();
  ctx.arc(
    food.x * GRID_SIZE + GRID_SIZE / 2,
    food.y * GRID_SIZE + GRID_SIZE / 2,
    GRID_SIZE / 2 - 2,
    0,
    Math.PI * 2
  );
  ctx.fill();
  ctx.shadowBlur = 0;

  // Draw snake
  snake.forEach((segment, index) => {
    const isHead = index === 0;
    ctx.fillStyle = isHead ? '#4ade80' : '#22c55e';
    
    if (isHead) {
      ctx.shadowColor = '#4ade80';
      ctx.shadowBlur = 15;
    }
    
    ctx.beginPath();
    ctx.roundRect(
      segment.x * GRID_SIZE + 1,
      segment.y * GRID_SIZE + 1,
      GRID_SIZE - 2,
      GRID_SIZE - 2,
      4
    );
    ctx.fill();
    ctx.shadowBlur = 0;
  });
}

// Update game state
function update() {
  if (!hasStarted || isPaused || isGameOver) return;

  direction = { ...nextDirection };

  // Calculate new head position
  const newHead = {
    x: snake[0].x + direction.x,
    y: snake[0].y + direction.y
  };

  // Check wall collision
  if (newHead.x < 0 || newHead.x >= TILE_COUNT || 
      newHead.y < 0 || newHead.y >= TILE_COUNT) {
    gameOver();
    return;
  }

  // Check self collision
  if (snake.some(segment => segment.x === newHead.x && segment.y === newHead.y)) {
    gameOver();
    return;
  }

  // Add new head
  snake.unshift(newHead);

  // Check food collision
  if (newHead.x === food.x && newHead.y === food.y) {
    score += 10;
    scoreElement.textContent = score;
    spawnFood();
  } else {
    // Remove tail
    snake.pop();
  }

  draw();
}

// Game over handler
function gameOver() {
  isGameOver = true;
  clearInterval(gameLoop);
  gameLoop = null;
  
  statusElement.textContent = 'Game Over! Press R to restart.';
  statusElement.className = 'status game-over';

  // Update high score
  if (score > highScore) {
    highScore = score;
    highScoreElement.textContent = highScore;
    localStorage.setItem('snakeHighScore', highScore);
  }
}

// Toggle pause
function togglePause() {
  if (!hasStarted || isGameOver) return;
  
  isPaused = !isPaused;
  statusElement.textContent = isPaused ? 'Paused - Press Space to resume' : 'Playing...';
  statusElement.className = isPaused ? 'status paused' : 'status';
}

// Handle keyboard input
function handleKeyDown(event) {
  const key = event.key.toLowerCase();
  
  // Restart game
  if (key === 'r') {
    clearInterval(gameLoop);
    gameLoop = null;
    initGame();
    return;
  }

  // Pause game
  if (key === ' ') {
    event.preventDefault();
    togglePause();
    return;
  }

  // Direction controls
  if (!hasStarted && ['arrowup', 'arrowdown', 'arrowleft', 'arrowright', 'w', 'a', 's', 'd'].includes(key)) {
    hasStarted = true;
    statusElement.textContent = 'Playing...';
    gameLoop = setInterval(update, GAME_SPEED);
  }

  // Prevent reversing direction
  switch (key) {
    case 'arrowup':
    case 'w':
      if (direction.y !== 1) nextDirection = { x: 0, y: -1 };
      break;
    case 'arrowdown':
    case 's':
      if (direction.y !== -1) nextDirection = { x: 0, y: 1 };
      break;
    case 'arrowleft':
    case 'a':
      if (direction.x !== 1) nextDirection = { x: -1, y: 0 };
      break;
    case 'arrowright':
    case 'd':
      if (direction.x !== -1) nextDirection = { x: 1, y: 0 };
      break;
  }
}

// Event listeners
document.addEventListener('keydown', handleKeyDown);

// Start the game
initGame();

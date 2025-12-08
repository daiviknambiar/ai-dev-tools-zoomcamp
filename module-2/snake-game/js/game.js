/**
 * Snake Game Engine
 * Handles game logic for both pass-through and walls modes
 */

export const DIRECTIONS = {
    UP: { x: 0, y: -1 },
    DOWN: { x: 0, y: 1 },
    LEFT: { x: -1, y: 0 },
    RIGHT: { x: 1, y: 0 }
};

export const GAME_MODES = {
    PASS_THROUGH: 'pass-through',
    WALLS: 'walls'
};

export class SnakeGame {
    constructor(gridSize = 30, mode = GAME_MODES.PASS_THROUGH) {
        this.gridSize = gridSize;
        this.mode = mode;
        this.reset();
    }

    reset() {
        const centerX = Math.floor(this.gridSize / 2);
        const centerY = Math.floor(this.gridSize / 2);

        this.snake = [
            { x: centerX, y: centerY },
            { x: centerX - 1, y: centerY },
            { x: centerX - 2, y: centerY }
        ];

        this.direction = DIRECTIONS.RIGHT;
        this.nextDirection = DIRECTIONS.RIGHT;
        this.food = this.generateFood();
        this.score = 0;
        this.isGameOver = false;
        this.isPaused = false;
    }

    setMode(mode) {
        this.mode = mode;
        this.reset();
    }

    generateFood() {
        let food;
        let attempts = 0;
        const maxAttempts = 100;

        do {
            food = {
                x: Math.floor(Math.random() * this.gridSize),
                y: Math.floor(Math.random() * this.gridSize)
            };
            attempts++;
        } while (this.isPositionOnSnake(food.x, food.y) && attempts < maxAttempts);

        return food;
    }

    isPositionOnSnake(x, y) {
        return this.snake.some(segment => segment.x === x && segment.y === y);
    }

    changeDirection(newDirection) {
        // Prevent reversing into itself
        const oppositeDirections = {
            [JSON.stringify(DIRECTIONS.UP)]: JSON.stringify(DIRECTIONS.DOWN),
            [JSON.stringify(DIRECTIONS.DOWN)]: JSON.stringify(DIRECTIONS.UP),
            [JSON.stringify(DIRECTIONS.LEFT)]: JSON.stringify(DIRECTIONS.RIGHT),
            [JSON.stringify(DIRECTIONS.RIGHT)]: JSON.stringify(DIRECTIONS.LEFT)
        };

        const currentDirStr = JSON.stringify(this.direction);
        const newDirStr = JSON.stringify(newDirection);

        if (oppositeDirections[currentDirStr] !== newDirStr) {
            this.nextDirection = newDirection;
        }
    }

    togglePause() {
        this.isPaused = !this.isPaused;
        return this.isPaused;
    }

    update() {
        if (this.isGameOver || this.isPaused) {
            return false;
        }

        // Update direction
        this.direction = this.nextDirection;

        // Calculate new head position
        const head = this.snake[0];
        let newHead = {
            x: head.x + this.direction.x,
            y: head.y + this.direction.y
        };

        // Handle wall collision based on mode
        if (this.mode === GAME_MODES.PASS_THROUGH) {
            // Wrap around walls
            if (newHead.x < 0) newHead.x = this.gridSize - 1;
            if (newHead.x >= this.gridSize) newHead.x = 0;
            if (newHead.y < 0) newHead.y = this.gridSize - 1;
            if (newHead.y >= this.gridSize) newHead.y = 0;
        } else if (this.mode === GAME_MODES.WALLS) {
            // Check wall collision
            if (newHead.x < 0 || newHead.x >= this.gridSize ||
                newHead.y < 0 || newHead.y >= this.gridSize) {
                this.isGameOver = true;
                return false;
            }
        }

        // Check self collision
        if (this.isPositionOnSnake(newHead.x, newHead.y)) {
            this.isGameOver = true;
            return false;
        }

        // Add new head
        this.snake.unshift(newHead);

        // Check if food eaten
        if (newHead.x === this.food.x && newHead.y === this.food.y) {
            this.score += 10;
            this.food = this.generateFood();
        } else {
            // Remove tail if no food eaten
            this.snake.pop();
        }

        return true;
    }

    getState() {
        return {
            snake: this.snake.map(segment => ({ ...segment })),
            food: { ...this.food },
            score: this.score,
            isGameOver: this.isGameOver,
            isPaused: this.isPaused,
            mode: this.mode,
            gridSize: this.gridSize
        };
    }

    // Method for simulating AI/bot gameplay
    static simulateMove(gameState) {
        const { snake, food, gridSize, mode } = gameState;
        const head = snake[0];

        // Simple AI: try to move towards food
        let dx = food.x - head.x;
        let dy = food.y - head.y;

        // Handle wrapping in pass-through mode for shortest path
        if (mode === GAME_MODES.PASS_THROUGH) {
            if (Math.abs(dx) > gridSize / 2) {
                dx = dx > 0 ? dx - gridSize : dx + gridSize;
            }
            if (Math.abs(dy) > gridSize / 2) {
                dy = dy > 0 ? dy - gridSize : dy + gridSize;
            }
        }

        // Prioritize the larger delta
        if (Math.abs(dx) > Math.abs(dy)) {
            return dx > 0 ? DIRECTIONS.RIGHT : DIRECTIONS.LEFT;
        } else if (Math.abs(dy) > 0) {
            return dy > 0 ? DIRECTIONS.DOWN : DIRECTIONS.UP;
        } else {
            // Random move if at food position (shouldn't happen)
            const dirs = [DIRECTIONS.UP, DIRECTIONS.DOWN, DIRECTIONS.LEFT, DIRECTIONS.RIGHT];
            return dirs[Math.floor(Math.random() * dirs.length)];
        }
    }
}

export class GameRenderer {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.cellSize = 0;
    }

    render(gameState) {
        const { snake, food, gridSize } = gameState;

        // Calculate cell size
        this.cellSize = this.canvas.width / gridSize;

        // Clear canvas
        this.ctx.fillStyle = '#1a1a1a';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw grid
        this.drawGrid(gridSize);

        // Draw food
        this.drawFood(food);

        // Draw snake
        this.drawSnake(snake);
    }

    drawGrid(gridSize) {
        this.ctx.strokeStyle = '#2a2a2a';
        this.ctx.lineWidth = 1;

        for (let i = 0; i <= gridSize; i++) {
            // Vertical lines
            this.ctx.beginPath();
            this.ctx.moveTo(i * this.cellSize, 0);
            this.ctx.lineTo(i * this.cellSize, this.canvas.height);
            this.ctx.stroke();

            // Horizontal lines
            this.ctx.beginPath();
            this.ctx.moveTo(0, i * this.cellSize);
            this.ctx.lineTo(this.canvas.width, i * this.cellSize);
            this.ctx.stroke();
        }
    }

    drawSnake(snake) {
        snake.forEach((segment, index) => {
            const x = segment.x * this.cellSize;
            const y = segment.y * this.cellSize;

            if (index === 0) {
                // Head - brighter green
                this.ctx.fillStyle = '#4ade80';
            } else {
                // Body - gradient green
                const alpha = 1 - (index / snake.length) * 0.4;
                this.ctx.fillStyle = `rgba(34, 197, 94, ${alpha})`;
            }

            this.ctx.fillRect(
                x + 1,
                y + 1,
                this.cellSize - 2,
                this.cellSize - 2
            );

            // Add eyes to head
            if (index === 0) {
                this.ctx.fillStyle = '#1a1a1a';
                const eyeSize = this.cellSize / 6;
                this.ctx.fillRect(x + eyeSize, y + eyeSize, eyeSize, eyeSize);
                this.ctx.fillRect(x + this.cellSize - 2 * eyeSize, y + eyeSize, eyeSize, eyeSize);
            }
        });
    }

    drawFood(food) {
        const x = food.x * this.cellSize;
        const y = food.y * this.cellSize;

        this.ctx.fillStyle = '#ef4444';
        this.ctx.beginPath();
        this.ctx.arc(
            x + this.cellSize / 2,
            y + this.cellSize / 2,
            this.cellSize / 2 - 2,
            0,
            Math.PI * 2
        );
        this.ctx.fill();
    }
}

/**
 * Tests for Snake Game Logic
 */

import { describe, test, expect, beforeEach } from '@jest/globals';
import { SnakeGame, DIRECTIONS, GAME_MODES } from '../js/game.js';

describe('SnakeGame', () => {
    let game;

    beforeEach(() => {
        game = new SnakeGame(30, GAME_MODES.PASS_THROUGH);
    });

    describe('Initialization', () => {
        test('should initialize with correct default values', () => {
            expect(game.gridSize).toBe(30);
            expect(game.mode).toBe(GAME_MODES.PASS_THROUGH);
            expect(game.score).toBe(0);
            expect(game.isGameOver).toBe(false);
            expect(game.isPaused).toBe(false);
        });

        test('should initialize snake at center with length 3', () => {
            expect(game.snake.length).toBe(3);
            expect(game.snake[0].x).toBe(15); // Head at center
            expect(game.snake[0].y).toBe(15);
        });

        test('should initialize with food not on snake', () => {
            const food = game.food;
            const foodOnSnake = game.isPositionOnSnake(food.x, food.y);
            expect(foodOnSnake).toBe(false);
        });

        test('should initialize with RIGHT direction', () => {
            expect(game.direction).toEqual(DIRECTIONS.RIGHT);
        });
    });

    describe('Mode Setting', () => {
        test('should change mode and reset game', () => {
            game.score = 100;
            game.setMode(GAME_MODES.WALLS);

            expect(game.mode).toBe(GAME_MODES.WALLS);
            expect(game.score).toBe(0); // Reset
        });
    });

    describe('Direction Change', () => {
        test('should change direction when valid', () => {
            game.changeDirection(DIRECTIONS.UP);
            expect(game.nextDirection).toEqual(DIRECTIONS.UP);
        });

        test('should not allow reversing direction', () => {
            game.direction = DIRECTIONS.RIGHT;
            game.changeDirection(DIRECTIONS.LEFT); // Opposite of RIGHT

            expect(game.nextDirection).toEqual(DIRECTIONS.RIGHT); // Should not change
        });

        test('should allow perpendicular direction changes', () => {
            game.direction = DIRECTIONS.RIGHT;
            game.changeDirection(DIRECTIONS.UP);

            expect(game.nextDirection).toEqual(DIRECTIONS.UP);
        });
    });

    describe('Pause Functionality', () => {
        test('should toggle pause state', () => {
            expect(game.isPaused).toBe(false);

            game.togglePause();
            expect(game.isPaused).toBe(true);

            game.togglePause();
            expect(game.isPaused).toBe(false);
        });

        test('should return current pause state when toggled', () => {
            const isPaused = game.togglePause();
            expect(isPaused).toBe(true);
        });
    });

    describe('Movement - Pass-Through Mode', () => {
        beforeEach(() => {
            game.setMode(GAME_MODES.PASS_THROUGH);
        });

        test('should move snake forward', () => {
            const initialHead = { ...game.snake[0] };
            game.update();

            expect(game.snake[0].x).toBe(initialHead.x + 1); // Moved right
        });

        test('should wrap around right wall', () => {
            game.snake = [{ x: 29, y: 15 }]; // At right edge
            game.direction = DIRECTIONS.RIGHT;
            game.nextDirection = DIRECTIONS.RIGHT;

            game.update();

            expect(game.snake[0].x).toBe(0); // Wrapped to left
        });

        test('should wrap around left wall', () => {
            game.snake = [{ x: 0, y: 15 }];
            game.direction = DIRECTIONS.LEFT;
            game.nextDirection = DIRECTIONS.LEFT;

            game.update();

            expect(game.snake[0].x).toBe(29); // Wrapped to right
        });

        test('should wrap around top wall', () => {
            game.snake = [{ x: 15, y: 0 }];
            game.direction = DIRECTIONS.UP;
            game.nextDirection = DIRECTIONS.UP;

            game.update();

            expect(game.snake[0].y).toBe(29); // Wrapped to bottom
        });

        test('should wrap around bottom wall', () => {
            game.snake = [{ x: 15, y: 29 }];
            game.direction = DIRECTIONS.DOWN;
            game.nextDirection = DIRECTIONS.DOWN;

            game.update();

            expect(game.snake[0].y).toBe(0); // Wrapped to top
        });
    });

    describe('Movement - Walls Mode', () => {
        beforeEach(() => {
            game.setMode(GAME_MODES.WALLS);
        });

        test('should end game when hitting right wall', () => {
            game.snake = [{ x: 29, y: 15 }];
            game.direction = DIRECTIONS.RIGHT;
            game.nextDirection = DIRECTIONS.RIGHT;

            game.update();

            expect(game.isGameOver).toBe(true);
        });

        test('should end game when hitting left wall', () => {
            game.snake = [{ x: 0, y: 15 }];
            game.direction = DIRECTIONS.LEFT;
            game.nextDirection = DIRECTIONS.LEFT;

            game.update();

            expect(game.isGameOver).toBe(true);
        });

        test('should end game when hitting top wall', () => {
            game.snake = [{ x: 15, y: 0 }];
            game.direction = DIRECTIONS.UP;
            game.nextDirection = DIRECTIONS.UP;

            game.update();

            expect(game.isGameOver).toBe(true);
        });

        test('should end game when hitting bottom wall', () => {
            game.snake = [{ x: 15, y: 29 }];
            game.direction = DIRECTIONS.DOWN;
            game.nextDirection = DIRECTIONS.DOWN;

            game.update();

            expect(game.isGameOver).toBe(true);
        });
    });

    describe('Self Collision', () => {
        test('should end game when snake hits itself', () => {
            // Create a snake that will collide with itself
            game.snake = [
                { x: 10, y: 10 },
                { x: 9, y: 10 },
                { x: 9, y: 11 },
                { x: 10, y: 11 }
            ];
            game.direction = DIRECTIONS.DOWN;
            game.nextDirection = DIRECTIONS.DOWN;

            game.update();

            expect(game.isGameOver).toBe(true);
        });
    });

    describe('Food Consumption', () => {
        test('should increase score when eating food', () => {
            game.snake = [{ x: 10, y: 10 }];
            game.food = { x: 11, y: 10 };
            game.direction = DIRECTIONS.RIGHT;
            game.nextDirection = DIRECTIONS.RIGHT;

            const initialScore = game.score;
            game.update();

            expect(game.score).toBe(initialScore + 10);
        });

        test('should grow snake when eating food', () => {
            game.snake = [{ x: 10, y: 10 }];
            game.food = { x: 11, y: 10 };
            game.direction = DIRECTIONS.RIGHT;
            game.nextDirection = DIRECTIONS.RIGHT;

            const initialLength = game.snake.length;
            game.update();

            expect(game.snake.length).toBe(initialLength + 1);
        });

        test('should generate new food after eating', () => {
            game.snake = [{ x: 10, y: 10 }];
            const oldFood = { x: 11, y: 10 };
            game.food = oldFood;
            game.direction = DIRECTIONS.RIGHT;
            game.nextDirection = DIRECTIONS.RIGHT;

            game.update();

            expect(game.food).not.toEqual(oldFood);
        });

        test('should not grow snake when not eating food', () => {
            game.snake = [{ x: 10, y: 10 }, { x: 9, y: 10 }];
            game.food = { x: 20, y: 20 };
            game.direction = DIRECTIONS.RIGHT;
            game.nextDirection = DIRECTIONS.RIGHT;

            const initialLength = game.snake.length;
            game.update();

            expect(game.snake.length).toBe(initialLength);
        });
    });

    describe('Pause Behavior', () => {
        test('should not update when paused', () => {
            const initialState = game.getState();
            game.togglePause();

            game.update();

            const currentState = game.getState();
            expect(currentState.snake).toEqual(initialState.snake);
            expect(currentState.score).toBe(initialState.score);
        });
    });

    describe('Game State', () => {
        test('should return complete game state', () => {
            const state = game.getState();

            expect(state).toHaveProperty('snake');
            expect(state).toHaveProperty('food');
            expect(state).toHaveProperty('score');
            expect(state).toHaveProperty('isGameOver');
            expect(state).toHaveProperty('isPaused');
            expect(state).toHaveProperty('mode');
            expect(state).toHaveProperty('gridSize');
        });

        test('should return deep copy of snake array', () => {
            const state = game.getState();

            // Modify returned state
            state.snake[0].x = 999;

            // Original should be unchanged
            expect(game.snake[0].x).not.toBe(999);
        });
    });

    describe('AI Simulation', () => {
        test('should return a valid direction', () => {
            const state = game.getState();
            const direction = SnakeGame.simulateMove(state);

            const validDirections = [
                DIRECTIONS.UP,
                DIRECTIONS.DOWN,
                DIRECTIONS.LEFT,
                DIRECTIONS.RIGHT
            ];

            const isValid = validDirections.some(
                d => d.x === direction.x && d.y === direction.y
            );

            expect(isValid).toBe(true);
        });

        test('should move towards food', () => {
            const gameState = {
                snake: [{ x: 10, y: 10 }],
                food: { x: 15, y: 10 },
                gridSize: 30,
                mode: GAME_MODES.PASS_THROUGH
            };

            const direction = SnakeGame.simulateMove(gameState);

            // Should move right towards food
            expect(direction).toEqual(DIRECTIONS.RIGHT);
        });
    });

    describe('Reset Functionality', () => {
        test('should reset all game properties', () => {
            // Modify game state
            game.score = 100;
            game.isGameOver = true;
            game.isPaused = true;

            game.reset();

            expect(game.score).toBe(0);
            expect(game.isGameOver).toBe(false);
            expect(game.isPaused).toBe(false);
            expect(game.snake.length).toBe(3);
        });
    });
});

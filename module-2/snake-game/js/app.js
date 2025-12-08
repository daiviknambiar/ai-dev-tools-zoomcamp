/**
 * Main Application Controller
 * Coordinates all components and manages navigation
 */

import { AuthController } from './auth.js';
import { LeaderboardController } from './leaderboard.js';
import { WatchController } from './watch.js';
import { SnakeGame, GameRenderer, DIRECTIONS, GAME_MODES } from './game.js';
import { api } from './api.js';

class App {
    constructor() {
        this.authController = new AuthController();
        this.leaderboardController = new LeaderboardController();
        this.watchController = new WatchController();

        this.game = null;
        this.renderer = null;
        this.gameLoop = null;
        this.currentMode = GAME_MODES.PASS_THROUGH;
        this.isPlaying = false;

        this.setupGame();
        this.setupNavigation();
        this.setupGameControls();
        this.loadHighScore();
    }

    setupGame() {
        const canvas = document.getElementById('game-canvas');
        this.renderer = new GameRenderer(canvas);
        this.game = new SnakeGame(30, this.currentMode);
    }

    setupNavigation() {
        const sections = {
            'nav-play': 'play-section',
            'nav-leaderboard': 'leaderboard-section',
            'nav-watch': 'watch-section'
        };

        Object.keys(sections).forEach(navId => {
            const btn = document.getElementById(navId);
            btn.addEventListener('click', () => {
                this.navigateTo(navId, sections[navId]);
            });
        });
    }

    navigateTo(navId, sectionId) {
        // Update active nav button
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.getElementById(navId).classList.add('active');

        // Update visible section
        document.querySelectorAll('.section').forEach(section => {
            section.classList.add('hidden');
        });
        document.getElementById(sectionId).classList.remove('hidden');

        // Handle section-specific logic
        if (sectionId === 'leaderboard-section') {
            this.leaderboardController.show();
        } else if (sectionId === 'watch-section') {
            this.watchController.show();
        } else if (sectionId === 'play-section') {
            this.watchController.hide();
        }
    }

    setupGameControls() {
        // Mode selector
        const modeRadios = document.querySelectorAll('input[name="game-mode"]');
        modeRadios.forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.currentMode = e.target.value === 'pass-through'
                    ? GAME_MODES.PASS_THROUGH
                    : GAME_MODES.WALLS;

                document.getElementById('current-mode').textContent =
                    this.currentMode === GAME_MODES.PASS_THROUGH ? 'Pass-Through' : 'Walls';

                // Reset game if not playing
                if (!this.isPlaying) {
                    this.game.setMode(this.currentMode);
                    this.renderer.render(this.game.getState());
                }
            });
        });

        // Start button
        document.getElementById('start-btn').addEventListener('click', () => {
            this.startGame();
        });

        // Pause button
        document.getElementById('pause-btn').addEventListener('click', () => {
            this.togglePause();
        });

        // Restart button
        document.getElementById('restart-btn').addEventListener('click', () => {
            this.hideGameOver();
            this.startGame();
        });

        // Keyboard controls
        document.addEventListener('keydown', (e) => {
            if (!this.isPlaying || !this.game) return;

            switch (e.key) {
                case 'ArrowUp':
                case 'w':
                case 'W':
                    e.preventDefault();
                    this.game.changeDirection(DIRECTIONS.UP);
                    break;
                case 'ArrowDown':
                case 's':
                case 'S':
                    e.preventDefault();
                    this.game.changeDirection(DIRECTIONS.DOWN);
                    break;
                case 'ArrowLeft':
                case 'a':
                case 'A':
                    e.preventDefault();
                    this.game.changeDirection(DIRECTIONS.LEFT);
                    break;
                case 'ArrowRight':
                case 'd':
                case 'D':
                    e.preventDefault();
                    this.game.changeDirection(DIRECTIONS.RIGHT);
                    break;
                case ' ':
                case 'p':
                case 'P':
                    e.preventDefault();
                    this.togglePause();
                    break;
            }
        });
    }

    startGame() {
        // Reset game
        this.game.setMode(this.currentMode);
        this.game.reset();
        this.isPlaying = true;

        // Update UI
        document.getElementById('start-btn').classList.add('hidden');
        document.getElementById('pause-btn').classList.remove('hidden');
        this.hideGameOver();

        // Disable mode selection during game
        document.querySelectorAll('input[name="game-mode"]').forEach(radio => {
            radio.disabled = true;
        });

        // Start game loop
        this.runGameLoop();
    }

    runGameLoop() {
        let lastUpdate = Date.now();
        const updateSpeed = 100; // 100ms between updates

        const loop = () => {
            const now = Date.now();

            if (now - lastUpdate >= updateSpeed) {
                const continued = this.game.update();

                // Update score display
                document.getElementById('score').textContent = this.game.score;

                // Render game
                this.renderer.render(this.game.getState());

                if (!continued) {
                    this.endGame();
                    return;
                }

                lastUpdate = now;
            }

            if (this.isPlaying) {
                this.gameLoop = requestAnimationFrame(loop);
            }
        };

        loop();
    }

    togglePause() {
        if (!this.isPlaying) return;

        const isPaused = this.game.togglePause();
        const pauseBtn = document.getElementById('pause-btn');

        if (isPaused) {
            pauseBtn.textContent = 'Resume';
            if (this.gameLoop) {
                cancelAnimationFrame(this.gameLoop);
                this.gameLoop = null;
            }
        } else {
            pauseBtn.textContent = 'Pause';
            this.runGameLoop();
        }
    }

    async endGame() {
        this.isPlaying = false;

        if (this.gameLoop) {
            cancelAnimationFrame(this.gameLoop);
            this.gameLoop = null;
        }

        const finalScore = this.game.score;

        // Update UI
        document.getElementById('final-score').textContent = finalScore;
        document.getElementById('game-over').classList.remove('hidden');
        document.getElementById('pause-btn').classList.add('hidden');
        document.getElementById('start-btn').classList.remove('hidden');

        // Re-enable mode selection
        document.querySelectorAll('input[name="game-mode"]').forEach(radio => {
            radio.disabled = false;
        });

        // Submit score
        await this.leaderboardController.submitScore(finalScore, this.currentMode);

        // Update high score
        await this.loadHighScore();
    }

    hideGameOver() {
        document.getElementById('game-over').classList.add('hidden');
        document.getElementById('score').textContent = '0';
    }

    async loadHighScore() {
        try {
            const result = await api.getUserHighScore('all');
            if (result.success) {
                document.getElementById('high-score').textContent = result.highScore;
            }
        } catch (error) {
            console.error('Error loading high score:', error);
        }
    }
}

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new App();
    });
} else {
    new App();
}

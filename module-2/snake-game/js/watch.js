/**
 * Watch Controller
 * Handles watching other players' games with simulated gameplay
 */

import { api } from './api.js';
import { SnakeGame, GameRenderer, GAME_MODES } from './game.js';

export class WatchController {
    constructor() {
        this.canvas = document.getElementById('watch-canvas');
        this.renderer = new GameRenderer(this.canvas);
        this.activeGames = [];
        this.currentWatchedGame = null;
        this.simulatedGame = null;
        this.animationId = null;
        this.updateInterval = null;
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Event listeners will be added dynamically when player cards are created
    }

    async loadActivePlayers() {
        try {
            const result = await api.getActiveGames();

            if (result.success) {
                this.activeGames = result.games;
                this.renderPlayersList();
            }
        } catch (error) {
            console.error('Error loading active games:', error);
        }
    }

    renderPlayersList() {
        const playersList = document.getElementById('players-list');
        playersList.innerHTML = '';

        if (this.activeGames.length === 0) {
            playersList.innerHTML = '<p style="padding: 20px; text-align: center; color: #666;">No active games at the moment</p>';
            return;
        }

        this.activeGames.forEach(game => {
            const card = document.createElement('div');
            card.className = 'player-card';
            card.dataset.gameId = game.id;

            const timePlaying = this.getTimePlaying(game.gameStartTime);

            card.innerHTML = `
                <div class="player-name">${this.escapeHtml(game.username)}</div>
                <div class="player-stats">
                    Score: ${game.currentScore} | Mode: ${this.formatMode(game.mode)}<br>
                    Playing for: ${timePlaying}
                </div>
            `;

            card.addEventListener('click', () => {
                this.watchGame(game);
            });

            playersList.appendChild(card);
        });
    }

    watchGame(gameInfo) {
        // Stop any current watched game
        this.stopWatching();

        // Update UI
        document.querySelectorAll('.player-card').forEach(card => {
            card.classList.remove('watching');
        });

        const selectedCard = document.querySelector(`[data-game-id="${gameInfo.id}"]`);
        if (selectedCard) {
            selectedCard.classList.add('watching');
        }

        // Update watch info
        const watchInfo = document.getElementById('watch-info');
        watchInfo.innerHTML = `
            <h3>Watching: ${this.escapeHtml(gameInfo.username)}</h3>
            <p>Mode: ${this.formatMode(gameInfo.mode)} | Current Score: <strong id="watch-score">${gameInfo.currentScore}</strong></p>
        `;

        // Create simulated game
        this.currentWatchedGame = gameInfo;
        this.simulatedGame = new SnakeGame(
            30,
            gameInfo.mode === 'walls' ? GAME_MODES.WALLS : GAME_MODES.PASS_THROUGH
        );

        // Set initial score to match
        this.simulatedGame.score = gameInfo.currentScore;

        // Start simulation
        this.startSimulation();
    }

    startSimulation() {
        let lastUpdate = Date.now();
        const updateSpeed = 150; // Update every 150ms

        const gameLoop = () => {
            const now = Date.now();

            if (now - lastUpdate >= updateSpeed) {
                // Simulate AI move
                const state = this.simulatedGame.getState();
                const aiDirection = SnakeGame.simulateMove(state);
                this.simulatedGame.changeDirection(aiDirection);

                // Update game
                const continued = this.simulatedGame.update();

                // Update score display
                const scoreElement = document.getElementById('watch-score');
                if (scoreElement) {
                    scoreElement.textContent = this.simulatedGame.score;
                }

                // Render
                this.renderer.render(this.simulatedGame.getState());

                // Check if game over
                if (!continued) {
                    // Wait a bit then start new game
                    setTimeout(() => {
                        if (this.currentWatchedGame) {
                            this.simulatedGame.reset();
                            this.simulatedGame.score = Math.floor(Math.random() * 100) + 20;
                        }
                    }, 2000);
                }

                lastUpdate = now;
            }

            if (this.currentWatchedGame) {
                this.animationId = requestAnimationFrame(gameLoop);
            }
        };

        gameLoop();

        // Periodically update player info
        this.updateInterval = setInterval(() => {
            if (this.currentWatchedGame) {
                // Simulate score changes
                const watchInfo = document.getElementById('watch-info');
                if (watchInfo) {
                    const newScore = this.simulatedGame.score + Math.floor(Math.random() * 10);
                    watchInfo.querySelector('strong').textContent = newScore;
                }
            }
        }, 5000);
    }

    stopWatching() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }

        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }

        this.currentWatchedGame = null;
        this.simulatedGame = null;

        // Clear canvas
        const ctx = this.canvas.getContext('2d');
        ctx.fillStyle = '#1a1a1a';
        ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // Clear watch info
        const watchInfo = document.getElementById('watch-info');
        watchInfo.innerHTML = '<p>Select a player to watch their game</p>';

        // Remove watching class from cards
        document.querySelectorAll('.player-card').forEach(card => {
            card.classList.remove('watching');
        });
    }

    formatMode(mode) {
        return mode === 'pass-through' ? 'Pass-Through' : 'Walls';
    }

    getTimePlaying(startTime) {
        const start = new Date(startTime);
        const now = new Date();
        const diffMs = now - start;
        const diffMins = Math.floor(diffMs / (1000 * 60));
        const diffSecs = Math.floor((diffMs % (1000 * 60)) / 1000);

        if (diffMins > 0) {
            return `${diffMins}m ${diffSecs}s`;
        }
        return `${diffSecs}s`;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    show() {
        this.loadActivePlayers();
    }

    hide() {
        this.stopWatching();
    }
}

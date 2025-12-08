/**
 * Centralized Mock Backend API Service
 * All backend calls should go through this module
 */

class MockAPI {
    constructor() {
        this.STORAGE_KEYS = {
            USERS: 'snake_users',
            CURRENT_USER: 'snake_current_user',
            LEADERBOARD: 'snake_leaderboard',
            ACTIVE_GAMES: 'snake_active_games'
        };
        this.initializeStorage();
    }

    /**
     * Initialize storage with default data if empty
     */
    initializeStorage() {
        if (!localStorage.getItem(this.STORAGE_KEYS.USERS)) {
            const defaultUsers = [
                { id: 1, username: 'player1', email: 'player1@test.com', password: 'pass123' },
                { id: 2, username: 'player2', email: 'player2@test.com', password: 'pass123' },
                { id: 3, username: 'speedmaster', email: 'speed@test.com', password: 'pass123' }
            ];
            localStorage.setItem(this.STORAGE_KEYS.USERS, JSON.stringify(defaultUsers));
        }

        if (!localStorage.getItem(this.STORAGE_KEYS.LEADERBOARD)) {
            const defaultLeaderboard = [
                { id: 1, userId: 1, username: 'player1', score: 150, mode: 'walls', date: new Date(Date.now() - 86400000).toISOString() },
                { id: 2, userId: 2, username: 'player2', score: 230, mode: 'pass-through', date: new Date(Date.now() - 172800000).toISOString() },
                { id: 3, userId: 3, username: 'speedmaster', score: 180, mode: 'walls', date: new Date(Date.now() - 259200000).toISOString() },
                { id: 4, userId: 1, username: 'player1', score: 200, mode: 'pass-through', date: new Date(Date.now() - 345600000).toISOString() },
                { id: 5, userId: 2, username: 'player2', score: 120, mode: 'walls', date: new Date(Date.now() - 432000000).toISOString() }
            ];
            localStorage.setItem(this.STORAGE_KEYS.LEADERBOARD, JSON.stringify(defaultLeaderboard));
        }

        if (!localStorage.getItem(this.STORAGE_KEYS.ACTIVE_GAMES)) {
            localStorage.setItem(this.STORAGE_KEYS.ACTIVE_GAMES, JSON.stringify([]));
        }
    }

    /**
     * Simulate network delay
     */
    async delay(ms = 300) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Authentication Methods
     */

    async login(username, password) {
        await this.delay();

        const users = JSON.parse(localStorage.getItem(this.STORAGE_KEYS.USERS) || '[]');
        const user = users.find(u => u.username === username && u.password === password);

        if (user) {
            const userSession = {
                id: user.id,
                username: user.username,
                email: user.email,
                loginTime: new Date().toISOString()
            };
            localStorage.setItem(this.STORAGE_KEYS.CURRENT_USER, JSON.stringify(userSession));
            return { success: true, user: userSession };
        }

        return { success: false, error: 'Invalid username or password' };
    }

    async signup(username, email, password) {
        await this.delay();

        const users = JSON.parse(localStorage.getItem(this.STORAGE_KEYS.USERS) || '[]');

        // Check if username already exists
        if (users.find(u => u.username === username)) {
            return { success: false, error: 'Username already exists' };
        }

        // Check if email already exists
        if (users.find(u => u.email === email)) {
            return { success: false, error: 'Email already registered' };
        }

        const newUser = {
            id: users.length + 1,
            username,
            email,
            password
        };

        users.push(newUser);
        localStorage.setItem(this.STORAGE_KEYS.USERS, JSON.stringify(users));

        const userSession = {
            id: newUser.id,
            username: newUser.username,
            email: newUser.email,
            loginTime: new Date().toISOString()
        };
        localStorage.setItem(this.STORAGE_KEYS.CURRENT_USER, JSON.stringify(userSession));

        return { success: true, user: userSession };
    }

    async logout() {
        await this.delay(100);
        localStorage.removeItem(this.STORAGE_KEYS.CURRENT_USER);
        return { success: true };
    }

    getCurrentUser() {
        const user = localStorage.getItem(this.STORAGE_KEYS.CURRENT_USER);
        return user ? JSON.parse(user) : null;
    }

    isAuthenticated() {
        return this.getCurrentUser() !== null;
    }

    /**
     * Leaderboard Methods
     */

    async getLeaderboard(mode = 'all', limit = 50) {
        await this.delay();

        let leaderboard = JSON.parse(localStorage.getItem(this.STORAGE_KEYS.LEADERBOARD) || '[]');

        // Filter by mode if specified
        if (mode !== 'all') {
            leaderboard = leaderboard.filter(entry => entry.mode === mode);
        }

        // Sort by score (descending) and limit
        leaderboard.sort((a, b) => b.score - a.score);
        leaderboard = leaderboard.slice(0, limit);

        return { success: true, leaderboard };
    }

    async submitScore(score, mode) {
        await this.delay();

        const currentUser = this.getCurrentUser();
        if (!currentUser) {
            return { success: false, error: 'User not authenticated' };
        }

        const leaderboard = JSON.parse(localStorage.getItem(this.STORAGE_KEYS.LEADERBOARD) || '[]');

        const newEntry = {
            id: leaderboard.length + 1,
            userId: currentUser.id,
            username: currentUser.username,
            score,
            mode,
            date: new Date().toISOString()
        };

        leaderboard.push(newEntry);
        localStorage.setItem(this.STORAGE_KEYS.LEADERBOARD, JSON.stringify(leaderboard));

        return { success: true, entry: newEntry };
    }

    async getUserHighScore(mode = 'all') {
        await this.delay();

        const currentUser = this.getCurrentUser();
        if (!currentUser) {
            return { success: false, error: 'User not authenticated' };
        }

        let leaderboard = JSON.parse(localStorage.getItem(this.STORAGE_KEYS.LEADERBOARD) || '[]');

        // Filter by user
        leaderboard = leaderboard.filter(entry => entry.userId === currentUser.id);

        // Filter by mode if specified
        if (mode !== 'all') {
            leaderboard = leaderboard.filter(entry => entry.mode === mode);
        }

        // Get highest score
        const highScore = leaderboard.length > 0
            ? Math.max(...leaderboard.map(entry => entry.score))
            : 0;

        return { success: true, highScore };
    }

    /**
     * Active Games / Watch Methods
     */

    async getActiveGames() {
        await this.delay(200);

        // Generate mock active games with some variation
        const mockPlayers = ['speedmaster', 'player1', 'snakepro', 'gamerX', 'player2'];
        const modes = ['walls', 'pass-through'];

        const activeGames = mockPlayers.map((username, index) => ({
            id: index + 1,
            username,
            mode: modes[Math.floor(Math.random() * modes.length)],
            currentScore: Math.floor(Math.random() * 200) + 20,
            gameStartTime: new Date(Date.now() - Math.random() * 300000).toISOString(),
            isPlaying: true
        }));

        return { success: true, games: activeGames };
    }

    async getGameState(gameId) {
        await this.delay(100);

        // This will be used to get the current state of a specific game
        // The actual game state will be managed by the watch controller
        return {
            success: true,
            gameId,
            timestamp: new Date().toISOString()
        };
    }

    async startGame(mode) {
        await this.delay(100);

        const currentUser = this.getCurrentUser();
        if (!currentUser) {
            return { success: false, error: 'User not authenticated' };
        }

        const gameSession = {
            id: Date.now(),
            userId: currentUser.id,
            username: currentUser.username,
            mode,
            startTime: new Date().toISOString(),
            isActive: true
        };

        return { success: true, gameSession };
    }

    async endGame(gameId, score) {
        await this.delay(100);

        return {
            success: true,
            gameId,
            score,
            endTime: new Date().toISOString()
        };
    }
}

// Export singleton instance
export const api = new MockAPI();

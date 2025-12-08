/**
 * Centralized Mock Backend API Service
 * All backend calls should go through this module
 */

class APIClient {
    constructor({ baseUrl = 'http://localhost:8000' } = {}) {
        this.baseUrl = baseUrl.replace(/\/$/, '');
        this.STORAGE_KEYS = {
            CURRENT_USER: 'snake_current_user'
        };
    }

    async request(path, options = {}) {
        const url = `${this.baseUrl}${path}`;
        try {
            const res = await fetch(url, options);
            const text = await res.text();
            const data = text ? JSON.parse(text) : {};

            if (!res.ok) {
                return { success: false, status: res.status, error: data.error || data.message || res.statusText };
            }

            return { success: true, status: res.status, data };
        } catch (err) {
            return { success: false, error: err.message || 'Network error' };
        }
    }

    // Authentication
    async login(username, password) {
        const result = await this.request('/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (result.success) {
            const user = result.data.user || result.data;
            if (user) localStorage.setItem(this.STORAGE_KEYS.CURRENT_USER, JSON.stringify(user));
            return { success: true, user };
        }

        return { success: false, error: result.error };
    }

    async signup(username, email, password) {
        const result = await this.request('/auth/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });

        if (result.success && (result.status === 200 || result.status === 201)) {
            const user = result.data.user || result.data;
            if (user) localStorage.setItem(this.STORAGE_KEYS.CURRENT_USER, JSON.stringify(user));
            return { success: true, user };
        }

        return { success: false, error: result.error };
    }

    async logout() {
        const result = await this.request('/auth/logout', { method: 'POST' });
        localStorage.removeItem(this.STORAGE_KEYS.CURRENT_USER);
        return result.success ? { success: true } : { success: false, error: result.error };
    }

    async getCurrentUserServer() {
        const result = await this.request('/auth/me', { method: 'GET' });
        if (result.success) return { success: true, user: result.data };
        return { success: false, error: result.error };
    }

    getCurrentUser() {
        const user = localStorage.getItem(this.STORAGE_KEYS.CURRENT_USER);
        return user ? JSON.parse(user) : null;
    }

    isAuthenticated() {
        return this.getCurrentUser() !== null;
    }

    // Leaderboard
    async getLeaderboard(mode = 'all', limit = 50) {
        const params = new URLSearchParams();
        if (mode) params.set('mode', mode);
        if (limit) params.set('limit', String(limit));

        const result = await this.request(`/leaderboard?${params.toString()}`, { method: 'GET' });
        if (result.success) return { success: true, leaderboard: result.data.leaderboard || result.data };
        return { success: false, error: result.error };
    }

    async submitScore(score, mode) {
        const result = await this.request('/leaderboard', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ score, mode })
        });

        if (result.success && (result.status === 200 || result.status === 201)) {
            return { success: true, entry: result.data.entry || result.data };
        }

        return { success: false, error: result.error };
    }

    async getUserHighScore(mode = 'all') {
        const params = new URLSearchParams();
        if (mode) params.set('mode', mode);
        const result = await this.request(`/users/me/highscore?${params.toString()}`, { method: 'GET' });
        if (result.success) return { success: true, highScore: result.data.highScore ?? result.data };
        return { success: false, error: result.error };
    }

    // Active games / watch
    async getActiveGames() {
        const result = await this.request('/active-games', { method: 'GET' });
        if (result.success) return { success: true, games: result.data.games || result.data };
        return { success: false, error: result.error };
    }

    async getGameState(gameId) {
        const result = await this.request(`/games/${gameId}`, { method: 'GET' });
        if (result.success) return { success: true, ...result.data };
        return { success: false, error: result.error };
    }

    async startGame(mode) {
        const result = await this.request('/games', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mode })
        });

        if (result.success && (result.status === 200 || result.status === 201)) {
            return { success: true, gameSession: result.data.gameSession || result.data };
        }

        return { success: false, error: result.error };
    }

    async endGame(gameId, score) {
        const body = score !== undefined ? { score } : undefined;
        const result = await this.request(`/games/${gameId}/end`, {
            method: 'POST',
            headers: body ? { 'Content-Type': 'application/json' } : undefined,
            body: body ? JSON.stringify(body) : undefined
        });

        if (result.success) return { success: true, ...result.data };
        return { success: false, error: result.error };
    }
}

export const api = new APIClient();

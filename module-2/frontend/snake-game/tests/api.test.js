/**
 * Tests for Mock API Service
 */

import { describe, test, expect, beforeEach, afterEach } from '@jest/globals';
import { api } from '../js/api.js';

describe('MockAPI', () => {
    // Store original localStorage
    let localStorageData = {};

    beforeEach(() => {
        // Clear localStorage data completely
        localStorageData = {};

        // Mock localStorage
        global.localStorage = {
            getItem: (key) => localStorageData[key] || null,
            setItem: (key, value) => {
                localStorageData[key] = value;
            },
            removeItem: (key) => {
                delete localStorageData[key];
            },
            clear: () => {
                localStorageData = {};
            }
        };

        // Force re-initialize storage with fresh data
        // Note: initializeStorage only sets data if keys don't exist,
        // so we need to ensure localStorage is completely empty first
        api.initializeStorage();
    });

    afterEach(() => {
        // Clean up - remove current user to ensure tests are isolated
        if (localStorageData['snake_current_user']) {
            delete localStorageData['snake_current_user'];
        }
        localStorageData = {};
    });

    describe('Initialization', () => {
        test('should initialize with default users', () => {
            const users = JSON.parse(localStorage.getItem('snake_users'));
            expect(users).toBeDefined();
            expect(users.length).toBeGreaterThan(0);
        });

        test('should initialize with default leaderboard', () => {
            const leaderboard = JSON.parse(localStorage.getItem('snake_leaderboard'));
            expect(leaderboard).toBeDefined();
            expect(leaderboard.length).toBeGreaterThan(0);
        });

        test('should not overwrite existing data', () => {
            const customUsers = [{ id: 999, username: 'custom' }];
            localStorage.setItem('snake_users', JSON.stringify(customUsers));

            api.initializeStorage();

            const users = JSON.parse(localStorage.getItem('snake_users'));
            expect(users[0].id).toBe(999);
        });
    });

    describe('Authentication - Login', () => {
        test('should login with valid credentials', async () => {
            const result = await api.login('player1', 'pass123');

            expect(result.success).toBe(true);
            expect(result.user).toBeDefined();
            expect(result.user.username).toBe('player1');
        });

        test('should fail login with invalid username', async () => {
            const result = await api.login('nonexistent', 'pass123');

            expect(result.success).toBe(false);
            expect(result.error).toBeDefined();
        });

        test('should fail login with invalid password', async () => {
            const result = await api.login('player1', 'wrongpass');

            expect(result.success).toBe(false);
            expect(result.error).toBeDefined();
        });

        test('should store current user session on login', async () => {
            await api.login('player1', 'pass123');

            const currentUser = localStorage.getItem('snake_current_user');
            expect(currentUser).toBeDefined();

            const user = JSON.parse(currentUser);
            expect(user.username).toBe('player1');
        });

        test('should include login timestamp', async () => {
            const result = await api.login('player1', 'pass123');

            expect(result.user.loginTime).toBeDefined();
            expect(new Date(result.user.loginTime)).toBeInstanceOf(Date);
        });
    });

    describe('Authentication - Signup', () => {
        test('should signup new user with valid data', async () => {
            const result = await api.signup('newuser', 'new@test.com', 'pass123');

            expect(result.success).toBe(true);
            expect(result.user).toBeDefined();
            expect(result.user.username).toBe('newuser');
        });

        test('should fail signup with existing username', async () => {
            const result = await api.signup('player1', 'different@test.com', 'pass123');

            expect(result.success).toBe(false);
            expect(result.error).toContain('Username already exists');
        });

        test('should fail signup with existing email', async () => {
            const result = await api.signup('differentuser', 'player1@test.com', 'pass123');

            expect(result.success).toBe(false);
            expect(result.error).toContain('Email already registered');
        });

        test('should add new user to users list', async () => {
            await api.signup('newuser', 'new@test.com', 'pass123');

            const users = JSON.parse(localStorage.getItem('snake_users'));
            const newUser = users.find(u => u.username === 'newuser');

            expect(newUser).toBeDefined();
            expect(newUser.email).toBe('new@test.com');
        });

        test('should auto-login after successful signup', async () => {
            await api.signup('newuser', 'new@test.com', 'pass123');

            const currentUser = api.getCurrentUser();
            expect(currentUser).toBeDefined();
            expect(currentUser.username).toBe('newuser');
        });
    });

    describe('Authentication - Logout', () => {
        test('should logout successfully', async () => {
            await api.login('player1', 'pass123');
            const result = await api.logout();

            expect(result.success).toBe(true);
        });

        test('should remove current user session', async () => {
            await api.login('player1', 'pass123');
            await api.logout();

            const currentUser = localStorage.getItem('snake_current_user');
            expect(currentUser).toBeNull();
        });
    });

    describe('Authentication - Session Management', () => {
        test('should return current user when logged in', async () => {
            await api.login('player1', 'pass123');
            const currentUser = api.getCurrentUser();

            expect(currentUser).toBeDefined();
            expect(currentUser.username).toBe('player1');
        });

        test('should return null when not logged in', () => {
            const currentUser = api.getCurrentUser();
            expect(currentUser).toBeNull();
        });

        test('should correctly report authentication status', async () => {
            expect(api.isAuthenticated()).toBe(false);

            await api.login('player1', 'pass123');
            expect(api.isAuthenticated()).toBe(true);

            await api.logout();
            expect(api.isAuthenticated()).toBe(false);
        });
    });

    describe('Leaderboard - Get Leaderboard', () => {
        test('should return all leaderboard entries', async () => {
            const result = await api.getLeaderboard('all');

            expect(result.success).toBe(true);
            expect(result.leaderboard).toBeDefined();
            expect(Array.isArray(result.leaderboard)).toBe(true);
        });

        test('should filter by mode', async () => {
            const result = await api.getLeaderboard('walls');

            expect(result.success).toBe(true);
            result.leaderboard.forEach(entry => {
                expect(entry.mode).toBe('walls');
            });
        });

        test('should sort by score descending', async () => {
            const result = await api.getLeaderboard('all');

            for (let i = 0; i < result.leaderboard.length - 1; i++) {
                expect(result.leaderboard[i].score).toBeGreaterThanOrEqual(
                    result.leaderboard[i + 1].score
                );
            }
        });

        test('should respect limit parameter', async () => {
            const result = await api.getLeaderboard('all', 3);

            expect(result.leaderboard.length).toBeLessThanOrEqual(3);
        });
    });

    describe('Leaderboard - Submit Score', () => {
        beforeEach(async () => {
            await api.login('player1', 'pass123');
        });

        test('should submit score when authenticated', async () => {
            const result = await api.submitScore(150, 'walls');

            expect(result.success).toBe(true);
            expect(result.entry).toBeDefined();
            expect(result.entry.score).toBe(150);
        });

        test('should fail when not authenticated', async () => {
            await api.logout();
            const result = await api.submitScore(150, 'walls');

            expect(result.success).toBe(false);
            expect(result.error).toContain('not authenticated');
        });

        test('should add entry to leaderboard', async () => {
            await api.submitScore(999, 'walls');

            const leaderboard = JSON.parse(localStorage.getItem('snake_leaderboard'));
            const entry = leaderboard.find(e => e.score === 999);

            expect(entry).toBeDefined();
        });

        test('should include username in entry', async () => {
            const result = await api.submitScore(150, 'walls');

            expect(result.entry.username).toBe('player1');
        });

        test('should include timestamp', async () => {
            const result = await api.submitScore(150, 'walls');

            expect(result.entry.date).toBeDefined();
            expect(new Date(result.entry.date)).toBeInstanceOf(Date);
        });
    });

    describe('Leaderboard - Get User High Score', () => {
        beforeEach(async () => {
            await api.login('player1', 'pass123');
        });

        test('should return user high score', async () => {
            const result = await api.getUserHighScore('all');

            expect(result.success).toBe(true);
            expect(result.highScore).toBeDefined();
            expect(typeof result.highScore).toBe('number');
        });

        test('should return 0 for new user with no scores', async () => {
            await api.signup('brandnew', 'brandnew@test.com', 'pass123');
            const result = await api.getUserHighScore('all');

            expect(result.highScore).toBe(0);
        });

        test('should filter by mode', async () => {
            await api.submitScore(100, 'walls');
            await api.submitScore(200, 'pass-through');

            const result = await api.getUserHighScore('walls');
            expect(result.highScore).toBe(100);
        });

        test('should return highest score when multiple entries', async () => {
            await api.submitScore(100, 'walls');
            await api.submitScore(200, 'walls');
            await api.submitScore(150, 'walls');

            const result = await api.getUserHighScore('walls');
            expect(result.highScore).toBe(200);
        });

        test('should fail when not authenticated', async () => {
            await api.logout();
            const result = await api.getUserHighScore('all');

            expect(result.success).toBe(false);
        });
    });

    describe('Active Games', () => {
        test('should return list of active games', async () => {
            const result = await api.getActiveGames();

            expect(result.success).toBe(true);
            expect(result.games).toBeDefined();
            expect(Array.isArray(result.games)).toBe(true);
        });

        test('should return game information', async () => {
            const result = await api.getActiveGames();

            if (result.games.length > 0) {
                const game = result.games[0];
                expect(game).toHaveProperty('id');
                expect(game).toHaveProperty('username');
                expect(game).toHaveProperty('mode');
                expect(game).toHaveProperty('currentScore');
            }
        });
    });

    describe('Game Session', () => {
        beforeEach(async () => {
            await api.login('player1', 'pass123');
        });

        test('should start game when authenticated', async () => {
            const result = await api.startGame('walls');

            expect(result.success).toBe(true);
            expect(result.gameSession).toBeDefined();
            expect(result.gameSession.mode).toBe('walls');
        });

        test('should fail to start game when not authenticated', async () => {
            await api.logout();
            const result = await api.startGame('walls');

            expect(result.success).toBe(false);
        });

        test('should end game successfully', async () => {
            const startResult = await api.startGame('walls');
            const endResult = await api.endGame(startResult.gameSession.id, 150);

            expect(endResult.success).toBe(true);
            expect(endResult.score).toBe(150);
        });
    });
});

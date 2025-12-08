/**
 * Authentication Controller
 * Handles login and signup UI interactions
 */

import { api } from './api.js';

export class AuthController {
    constructor() {
        this.authContainer = document.getElementById('auth-container');
        this.gameContainer = document.getElementById('game-container');
        this.loginForm = document.getElementById('login-form');
        this.signupForm = document.getElementById('signup-form');
        this.authError = document.getElementById('auth-error');

        this.setupEventListeners();
        this.checkAuthStatus();
    }

    setupEventListeners() {
        // Login button
        document.getElementById('login-btn').addEventListener('click', () => this.handleLogin());

        // Signup button
        document.getElementById('signup-btn').addEventListener('click', () => this.handleSignup());

        // Show signup form
        document.getElementById('show-signup').addEventListener('click', (e) => {
            e.preventDefault();
            this.showSignupForm();
        });

        // Show login form
        document.getElementById('show-login').addEventListener('click', (e) => {
            e.preventDefault();
            this.showLoginForm();
        });

        // Logout button
        document.getElementById('logout-btn').addEventListener('click', () => this.handleLogout());

        // Enter key support
        document.getElementById('login-username').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleLogin();
        });

        document.getElementById('login-password').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleLogin();
        });

        document.getElementById('signup-username').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleSignup();
        });

        document.getElementById('signup-email').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleSignup();
        });

        document.getElementById('signup-password').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleSignup();
        });
    }

    showLoginForm() {
        this.loginForm.classList.remove('hidden');
        this.signupForm.classList.add('hidden');
        this.hideError();
    }

    showSignupForm() {
        this.loginForm.classList.add('hidden');
        this.signupForm.classList.remove('hidden');
        this.hideError();
    }

    showError(message) {
        this.authError.textContent = message;
        this.authError.classList.remove('hidden');
    }

    hideError() {
        this.authError.classList.add('hidden');
    }

    async handleLogin() {
        const username = document.getElementById('login-username').value.trim();
        const password = document.getElementById('login-password').value;

        if (!username || !password) {
            this.showError('Please fill in all fields');
            return;
        }

        this.hideError();

        try {
            const result = await api.login(username, password);

            if (result.success) {
                this.onLoginSuccess(result.user);
            } else {
                this.showError(result.error);
            }
        } catch (error) {
            this.showError('An error occurred. Please try again.');
            console.error('Login error:', error);
        }
    }

    async handleSignup() {
        const username = document.getElementById('signup-username').value.trim();
        const email = document.getElementById('signup-email').value.trim();
        const password = document.getElementById('signup-password').value;

        if (!username || !email || !password) {
            this.showError('Please fill in all fields');
            return;
        }

        // Basic email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            this.showError('Please enter a valid email address');
            return;
        }

        // Password validation
        if (password.length < 6) {
            this.showError('Password must be at least 6 characters');
            return;
        }

        this.hideError();

        try {
            const result = await api.signup(username, email, password);

            if (result.success) {
                this.onLoginSuccess(result.user);
            } else {
                this.showError(result.error);
            }
        } catch (error) {
            this.showError('An error occurred. Please try again.');
            console.error('Signup error:', error);
        }
    }

    async handleLogout() {
        try {
            await api.logout();
            this.onLogoutSuccess();
        } catch (error) {
            console.error('Logout error:', error);
        }
    }

    onLoginSuccess(user) {
        // Clear form inputs
        document.getElementById('login-username').value = '';
        document.getElementById('login-password').value = '';
        document.getElementById('signup-username').value = '';
        document.getElementById('signup-email').value = '';
        document.getElementById('signup-password').value = '';

        // Update username display
        document.getElementById('username-display').textContent = user.username;

        // Show game container, hide auth
        this.authContainer.classList.add('hidden');
        this.gameContainer.classList.remove('hidden');

        // Dispatch custom event
        window.dispatchEvent(new CustomEvent('userLoggedIn', { detail: user }));
    }

    onLogoutSuccess() {
        // Show auth container, hide game
        this.authContainer.classList.remove('hidden');
        this.gameContainer.classList.add('hidden');

        // Reset to login form
        this.showLoginForm();

        // Dispatch custom event
        window.dispatchEvent(new Event('userLoggedOut'));
    }

    checkAuthStatus() {
        const currentUser = api.getCurrentUser();

        if (currentUser) {
            this.onLoginSuccess(currentUser);
        } else {
            this.showLoginForm();
        }
    }

    getCurrentUser() {
        return api.getCurrentUser();
    }
}

/**
 * Leaderboard Controller
 * Handles leaderboard display and filtering
 */

import { api } from './api.js';

export class LeaderboardController {
    constructor() {
        this.currentFilter = 'all';
        this.leaderboardData = [];
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Filter buttons
        const filterButtons = document.querySelectorAll('.filter-btn');
        filterButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const mode = btn.dataset.mode;
                this.setFilter(mode);

                // Update active state
                filterButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            });
        });
    }

    setFilter(mode) {
        this.currentFilter = mode;
        this.loadLeaderboard();
    }

    async loadLeaderboard() {
        try {
            const result = await api.getLeaderboard(this.currentFilter);

            if (result.success) {
                this.leaderboardData = result.leaderboard;
                this.renderLeaderboard();
            }
        } catch (error) {
            console.error('Error loading leaderboard:', error);
        }
    }

    renderLeaderboard() {
        const tbody = document.getElementById('leaderboard-body');
        tbody.innerHTML = '';

        const currentUser = api.getCurrentUser();

        this.leaderboardData.forEach((entry, index) => {
            const row = document.createElement('tr');

            // Highlight current user's entries
            if (currentUser && entry.userId === currentUser.id) {
                row.classList.add('current-user');
            }

            const rank = index + 1;
            const rankDisplay = rank === 1 ? '🥇' : rank === 2 ? '🥈' : rank === 3 ? '🥉' : rank;

            row.innerHTML = `
                <td>${rankDisplay}</td>
                <td>${this.escapeHtml(entry.username)}</td>
                <td><strong>${entry.score}</strong></td>
                <td><span class="mode-badge ${entry.mode}">${this.formatMode(entry.mode)}</span></td>
                <td>${this.formatDate(entry.date)}</td>
            `;

            tbody.appendChild(row);
        });

        if (this.leaderboardData.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = '<td colspan="5" style="text-align: center; padding: 40px;">No scores yet. Be the first to play!</td>';
            tbody.appendChild(row);
        }
    }

    formatMode(mode) {
        return mode === 'pass-through' ? 'Pass-Through' : 'Walls';
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now - date;
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

        if (diffDays === 0) {
            return 'Today';
        } else if (diffDays === 1) {
            return 'Yesterday';
        } else if (diffDays < 7) {
            return `${diffDays} days ago`;
        } else {
            return date.toLocaleDateString();
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    async submitScore(score, mode) {
        try {
            const result = await api.submitScore(score, mode);

            if (result.success) {
                // Reload leaderboard to show new score
                await this.loadLeaderboard();
                return true;
            }
            return false;
        } catch (error) {
            console.error('Error submitting score:', error);
            return false;
        }
    }

    show() {
        this.loadLeaderboard();
    }
}

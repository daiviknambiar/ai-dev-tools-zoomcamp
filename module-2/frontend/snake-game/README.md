# Multiplayer Snake Game

A modern, interactive snake game with multiplayer features, leaderboards, and spectator mode. Built with vanilla JavaScript and comprehensive test coverage.

## Features

### Game Modes
- **Pass-Through Mode**: Snake passes through walls and appears on the opposite side
- **Walls Mode**: Game ends when snake hits a wall

### Multiplayer Features
- **Leaderboard**: Track top scores across all players and game modes
- **Watch Mode**: Spectate other players' games in real-time
- **User Authentication**: Login and signup functionality
- **Score Tracking**: Personal high scores and global rankings

### Interactive UI
- Clean, modern interface with smooth animations
- Real-time score updates
- Responsive design for different screen sizes
- Keyboard controls (Arrow Keys or WASD)
- Pause/Resume functionality

## Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript (ES6 Modules)
- **Canvas API**: For game rendering
- **Testing**: Jest with jsdom
- **Storage**: LocalStorage for persistence
- **Architecture**: MVC pattern with centralized API service

## Project Structure

```
snake-game/
├── index.html              # Main HTML file
├── css/
│   └── styles.css          # Application styles
├── js/
│   ├── app.js             # Main application controller
│   ├── api.js             # Centralized mock backend API
│   ├── auth.js            # Authentication controller
│   ├── game.js            # Snake game engine and renderer
│   ├── leaderboard.js     # Leaderboard controller
│   └── watch.js           # Watch/spectator controller
├── tests/
│   ├── api.test.js        # API service tests
│   └── game.test.js       # Game logic tests
├── package.json           # Dependencies and scripts
├── jest.config.js         # Jest configuration
└── README.md             # This file
```

## Installation

1. Clone the repository:
```bash
cd module-2/snake-game
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### Development Server

Start a local development server:

```bash
npm run serve
```

Then open your browser to `http://localhost:8000`

### Alternative: Direct File Access

You can also open `index.html` directly in your browser. However, due to CORS restrictions with ES6 modules, using a local server is recommended.

## Running Tests

Run all tests:
```bash
npm test
```

Run tests in watch mode:
```bash
npm run test:watch
```

Run tests with coverage:
```bash
npm run test:coverage
```

## How to Play

### Login/Signup
1. Create an account or login with existing credentials
2. Default test accounts:
   - Username: `player1`, Password: `pass123`
   - Username: `player2`, Password: `pass123`

### Playing the Game
1. Select your preferred game mode (Pass-Through or Walls)
2. Click "Start Game"
3. Use Arrow Keys or WASD to control the snake
4. Press Space or P to pause/resume
5. Eat red food to grow and increase your score

### Leaderboard
- View top scores across all players
- Filter by game mode
- Your scores are highlighted in yellow

### Watch Mode
- See other players currently playing
- Click on a player to watch their game
- AI-simulated gameplay for demonstration

## Game Controls

- **Arrow Keys** or **WASD**: Move snake (Up, Down, Left, Right)
- **Space** or **P**: Pause/Resume game
- **Enter**: Submit forms (login/signup)

## Architecture

### Centralized API Service

All backend interactions are centralized in `js/api.js`, making it easy to replace mock implementations with real API calls:

```javascript
import { api } from './api.js';

// Authentication
await api.login(username, password);
await api.signup(username, email, password);
await api.logout();

// Leaderboard
await api.getLeaderboard(mode, limit);
await api.submitScore(score, mode);
await api.getUserHighScore(mode);

// Active Games
await api.getActiveGames();
await api.startGame(mode);
await api.endGame(gameId, score);
```

### Game Engine

The game engine in `js/game.js` handles:
- Snake movement and collision detection
- Food generation and consumption
- Wall wrapping (pass-through mode)
- Wall collision (walls mode)
- Score calculation
- AI simulation for spectator mode

### Test Coverage

Comprehensive test suite covering:
- Game logic (movement, collision, scoring)
- Authentication (login, signup, logout)
- Leaderboard (filtering, sorting, submission)
- API service (all endpoints and edge cases)
- Mode switching (pass-through vs walls)

## Future Enhancements

To connect to a real backend:

1. Replace mock methods in `js/api.js` with actual HTTP requests
2. Update the `delay()` method to handle real network latency
3. Add error handling for network failures
4. Implement WebSocket for real-time multiplayer
5. Add real player spectating instead of AI simulation

## Development Notes

- All game state is managed in the game engine
- LocalStorage is used to persist user sessions and scores
- The watch mode uses AI simulation to demonstrate multiplayer functionality
- Tests use mocked localStorage to avoid state pollution

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

Requires ES6 module support and Canvas API.

## License

MIT License

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app
from app.services.nba_api_client import get_nba_client


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def mock_nba_client():
    """Create mock NBA API client."""
    mock_client = AsyncMock()
    return mock_client


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check(self, client):
        """Test health check returns success."""
        response = client.get("/api/v1/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data


class TestPlayersEndpoints:
    """Test player-related endpoints."""
    
    def test_list_players_success(self, client, mock_nba_client):
        """Test listing players successfully."""
        mock_nba_client.get_players.return_value = {
            "data": [
                {
                    "id": 237,
                    "first_name": "LeBron",
                    "last_name": "James",
                    "position": "F",
                    "team": {
                        "id": 14,
                        "name": "LA Lakers",
                        "abbreviation": "LAL",
                    },
                }
            ],
            "meta": {
                "current_page": 1,
                "per_page": 25,
                "next_page": None,
                "total_pages": 1,
                "total_count": 1,
            },
        }
        
        app.dependency_overrides[get_nba_client] = lambda: mock_nba_client
        
        response = client.get("/api/v1/players?search=LeBron")
        
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "meta" in data
        assert len(data["data"]) == 1
        assert data["data"][0]["first_name"] == "LeBron"
        
        app.dependency_overrides.clear()
    
    def test_list_players_pagination(self, client, mock_nba_client):
        """Test players list pagination."""
        mock_nba_client.get_players.return_value = {
            "data": [],
            "meta": {
                "current_page": 2,
                "per_page": 10,
                "next_page": 3,
                "total_pages": 5,
                "total_count": 50,
            },
        }
        
        app.dependency_overrides[get_nba_client] = lambda: mock_nba_client
        
        response = client.get("/api/v1/players?page=2&per_page=10")
        
        assert response.status_code == 200
        data = response.json()
        assert data["meta"]["current_page"] == 2
        assert data["meta"]["per_page"] == 10
        
        app.dependency_overrides.clear()
    
    def test_get_player_success(self, client, mock_nba_client):
        """Test getting single player successfully."""
        mock_nba_client.get_player.return_value = {
            "id": 237,
            "first_name": "LeBron",
            "last_name": "James",
            "position": "F",
            "height": "6-9",
            "weight": "250",
            "team": {
                "id": 14,
                "name": "LA Lakers",
                "abbreviation": "LAL",
            },
        }
        
        mock_nba_client.get_player_stats.return_value = {
            "data": [
                {
                    "games_played": 45,
                    "points": 25.3,
                    "rebounds": 7.5,
                    "assists": 8.1,
                    "season": 2024,
                }
            ]
        }
        
        app.dependency_overrides[get_nba_client] = lambda: mock_nba_client
        
        response = client.get("/api/v1/players/237")
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["id"] == 237
        assert data["data"]["first_name"] == "LeBron"
        
        app.dependency_overrides.clear()
    
    def test_get_player_not_found(self, client, mock_nba_client):
        """Test getting non-existent player."""
        from app.services.nba_api_client import NBAAPINotFoundError
        
        mock_nba_client.get_player.side_effect = NBAAPINotFoundError("Not found")
        
        app.dependency_overrides[get_nba_client] = lambda: mock_nba_client
        
        response = client.get("/api/v1/players/999999")
        
        assert response.status_code == 404
        
        app.dependency_overrides.clear()
    
    def test_get_player_stats_success(self, client, mock_nba_client):
        """Test getting player stats successfully."""
        mock_nba_client.get_player_stats.return_value = {
            "data": [
                {
                    "games_played": 45,
                    "points": 25.3,
                    "rebounds": 7.5,
                    "assists": 8.1,
                    "season": 2024,
                }
            ]
        }
        
        app.dependency_overrides[get_nba_client] = lambda: mock_nba_client
        
        response = client.get("/api/v1/players/237/stats?season=2024")
        
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) == 1
        assert data["data"][0]["points"] == 25.3
        
        app.dependency_overrides.clear()


class TestGamesEndpoints:
    """Test game-related endpoints."""
    
    def test_get_live_games_success(self, client, mock_nba_client):
        """Test getting live games successfully."""
        mock_nba_client.get_live_games.return_value = {
            "data": [
                {
                    "id": 12345,
                    "date": "2024-01-25T19:30:00Z",
                    "season": 2024,
                    "status": "InProgress",
                    "home_team": {
                        "id": 14,
                        "name": "LA Lakers",
                        "abbreviation": "LAL",
                    },
                    "visitor_team": {
                        "id": 2,
                        "name": "Boston Celtics",
                        "abbreviation": "BOS",
                    },
                    "home_team_score": 85,
                    "visitor_team_score": 82,
                }
            ]
        }
        
        app.dependency_overrides[get_nba_client] = lambda: mock_nba_client
        
        response = client.get("/api/v1/games/live")
        
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) == 1
        assert data["data"][0]["status"] == "InProgress"
        
        app.dependency_overrides.clear()
    
    def test_get_game_success(self, client, mock_nba_client):
        """Test getting single game successfully."""
        mock_nba_client.get_game.return_value = {
            "id": 12345,
            "date": "2024-01-25T19:30:00Z",
            "season": 2024,
            "status": "Final",
            "home_team": {
                "id": 14,
                "name": "LA Lakers",
                "abbreviation": "LAL",
            },
            "visitor_team": {
                "id": 2,
                "name": "Boston Celtics",
                "abbreviation": "BOS",
            },
            "home_team_score": 108,
            "visitor_team_score": 105,
        }
        
        app.dependency_overrides[get_nba_client] = lambda: mock_nba_client
        
        response = client.get("/api/v1/games/12345")
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["id"] == 12345
        assert data["data"]["status"] == "Final"
        
        app.dependency_overrides.clear()
    
    def test_get_games_with_date_range(self, client, mock_nba_client):
        """Test getting games with date range."""
        mock_nba_client.get_games.return_value = {
            "data": [
                {
                    "id": 12345,
                    "date": "2024-01-25T19:30:00Z",
                    "status": "Final",
                    "home_team": {"name": "LA Lakers"},
                    "visitor_team": {"name": "Boston Celtics"},
                    "home_team_score": 108,
                    "visitor_team_score": 105,
                }
            ],
            "meta": {"current_page": 1},
        }
        
        app.dependency_overrides[get_nba_client] = lambda: mock_nba_client
        
        response = client.get(
            "/api/v1/games?start_date=2024-01-25&end_date=2024-01-25"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) == 1
        
        app.dependency_overrides.clear()

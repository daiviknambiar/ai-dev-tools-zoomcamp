import pytest
import requests_mock
from services.api_client import APIClient, APIClientError


@pytest.fixture
def api_client():
    """Create API client for testing."""
    return APIClient(base_url="http://test-api:8000")


class TestAPIClient:
    """Test suite for API client."""
    
    def test_health_check_success(self, api_client):
        """Test successful health check."""
        with requests_mock.Mocker() as m:
            m.get(
                "http://test-api:8000/api/v1/health",
                json={
                    "status": "healthy",
                    "timestamp": "2024-01-25T10:00:00Z",
                    "version": "1.0.0",
                },
            )
            
            result = api_client.health_check()
            
            assert result["status"] == "healthy"
            assert "timestamp" in result
    
    def test_get_players_success(self, api_client):
        """Test successful player list retrieval."""
        with requests_mock.Mocker() as m:
            m.get(
                "http://test-api:8000/api/v1/players",
                json={
                    "data": [
                        {
                            "id": 237,
                            "first_name": "LeBron",
                            "last_name": "James",
                            "team": {"name": "LA Lakers"},
                        }
                    ],
                    "meta": {"current_page": 1, "per_page": 25},
                },
            )
            
            result = api_client.get_players(search="LeBron")
            
            assert "data" in result
            assert len(result["data"]) == 1
            assert result["data"][0]["first_name"] == "LeBron"
    
    def test_get_player_success(self, api_client):
        """Test successful single player retrieval."""
        with requests_mock.Mocker() as m:
            m.get(
                "http://test-api:8000/api/v1/players/237",
                json={
                    "data": {
                        "id": 237,
                        "first_name": "LeBron",
                        "last_name": "James",
                    }
                },
            )
            
            result = api_client.get_player(237)
            
            assert "data" in result
            assert result["data"]["id"] == 237
    
    def test_get_player_not_found(self, api_client):
        """Test player not found error."""
        with requests_mock.Mocker() as m:
            m.get(
                "http://test-api:8000/api/v1/players/999999",
                status_code=404,
                json={"error": "Not found"},
            )
            
            with pytest.raises(APIClientError, match="Resource not found"):
                api_client.get_player(999999)
    
    def test_get_player_stats_success(self, api_client):
        """Test successful player stats retrieval."""
        with requests_mock.Mocker() as m:
            m.get(
                "http://test-api:8000/api/v1/players/237/stats",
                json={
                    "data": [
                        {
                            "games_played": 45,
                            "points": 25.3,
                            "rebounds": 7.5,
                            "assists": 8.1,
                            "season": 2024,
                        }
                    ]
                },
            )
            
            result = api_client.get_player_stats(237, season=2024)
            
            assert "data" in result
            assert len(result["data"]) == 1
            assert result["data"][0]["points"] == 25.3
    
    def test_get_live_games_success(self, api_client):
        """Test successful live games retrieval."""
        with requests_mock.Mocker() as m:
            m.get(
                "http://test-api:8000/api/v1/games/live",
                json={
                    "data": [
                        {
                            "id": 12345,
                            "date": "2024-01-25T19:30:00Z",
                            "status": "InProgress",
                            "home_team": {"name": "LA Lakers"},
                            "visitor_team": {"name": "Boston Celtics"},
                        }
                    ]
                },
            )
            
            result = api_client.get_live_games()
            
            assert "data" in result
            assert len(result["data"]) == 1
            assert result["data"][0]["status"] == "InProgress"
    
    def test_get_game_success(self, api_client):
        """Test successful single game retrieval."""
        with requests_mock.Mocker() as m:
            m.get(
                "http://test-api:8000/api/v1/games/12345",
                json={
                    "data": {
                        "id": 12345,
                        "status": "Final",
                        "home_team_score": 108,
                        "visitor_team_score": 105,
                    }
                },
            )
            
            result = api_client.get_game(12345)
            
            assert "data" in result
            assert result["data"]["id"] == 12345
    
    def test_get_games_with_filters_success(self, api_client):
        """Test successful games retrieval with filters."""
        with requests_mock.Mocker() as m:
            m.get(
                "http://test-api:8000/api/v1/games",
                json={
                    "data": [
                        {
                            "id": 12345,
                            "date": "2024-01-25T19:30:00Z",
                            "status": "Final",
                        }
                    ],
                    "meta": {"current_page": 1},
                },
            )
            
            result = api_client.get_games(
                start_date="2024-01-25",
                end_date="2024-01-25",
            )
            
            assert "data" in result
            assert len(result["data"]) == 1
    
    def test_timeout_error(self, api_client):
        """Test timeout error handling."""
        with requests_mock.Mocker() as m:
            m.get(
                "http://test-api:8000/api/v1/players",
                exc=requests_mock.exceptions.ConnectTimeout,
            )
            
            with pytest.raises(APIClientError, match="Request timeout"):
                api_client.get_players()
    
    def test_server_error(self, api_client):
        """Test server error handling."""
        with requests_mock.Mocker() as m:
            m.get(
                "http://test-api:8000/api/v1/players",
                status_code=500,
                json={"error": "Internal server error"},
            )
            
            with pytest.raises(APIClientError, match="Server error"):
                api_client.get_players()

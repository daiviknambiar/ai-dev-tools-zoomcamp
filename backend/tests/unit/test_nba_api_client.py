import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx

from app.services.nba_api_client import (
    NBAAPIClient,
    NBAAPINotFoundError,
    NBAAPITimeoutError,
    NBAAPIClientError,
)


@pytest.fixture
def nba_client():
    """Create NBA API client for testing."""
    return NBAAPIClient()


@pytest.fixture
def mock_httpx_client():
    """Create mock httpx client."""
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    return mock_client


class TestNBAAPIClient:
    """Test suite for NBAAPIClient."""
    
    @pytest.mark.asyncio
    async def test_get_players_success(self, nba_client, mock_httpx_client):
        """Test successful player list retrieval."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "id": 237,
                    "first_name": "LeBron",
                    "last_name": "James",
                    "team": {"id": 14, "name": "LA Lakers"},
                }
            ],
            "meta": {"current_page": 1, "per_page": 25},
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.request = AsyncMock(return_value=mock_response)
        
        nba_client._client = mock_httpx_client
        
        result = await nba_client.get_players(search="LeBron", page=1, per_page=25)
        
        assert "data" in result
        assert len(result["data"]) == 1
        assert result["data"][0]["first_name"] == "LeBron"
        assert result["data"][0]["last_name"] == "James"
    
    @pytest.mark.asyncio
    async def test_get_player_success(self, nba_client, mock_httpx_client):
        """Test successful single player retrieval."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "id": 237,
                "first_name": "LeBron",
                "last_name": "James",
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.request = AsyncMock(return_value=mock_response)
        
        nba_client._client = mock_httpx_client
        
        result = await nba_client.get_player(237)
        
        assert result["id"] == 237
        assert result["first_name"] == "LeBron"
    
    @pytest.mark.asyncio
    async def test_get_player_not_found(self, nba_client, mock_httpx_client):
        """Test player not found error."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_httpx_client.request = AsyncMock(return_value=mock_response)
        
        nba_client._client = mock_httpx_client
        
        with pytest.raises(NBAAPINotFoundError):
            await nba_client.get_player(999999)
    
    @pytest.mark.asyncio
    async def test_get_player_timeout(self, nba_client, mock_httpx_client):
        """Test timeout error handling."""
        mock_httpx_client.request = AsyncMock(
            side_effect=httpx.TimeoutException("Timeout")
        )
        
        nba_client._client = mock_httpx_client
        
        with pytest.raises(NBAAPITimeoutError):
            await nba_client.get_player(237)
    
    @pytest.mark.asyncio
    async def test_get_player_stats_success(self, nba_client, mock_httpx_client):
        """Test successful player stats retrieval."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
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
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.request = AsyncMock(return_value=mock_response)
        
        nba_client._client = mock_httpx_client
        
        result = await nba_client.get_player_stats(237, season=2024)
        
        assert "data" in result
        assert len(result["data"]) == 1
        assert result["data"][0]["points"] == 25.3
        assert result["data"][0]["season"] == 2024
    
    @pytest.mark.asyncio
    async def test_get_games_success(self, nba_client, mock_httpx_client):
        """Test successful games retrieval."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "id": 12345,
                    "date": "2024-01-25T19:30:00Z",
                    "home_team": {"name": "LA Lakers"},
                    "visitor_team": {"name": "Boston Celtics"},
                    "status": "Final",
                }
            ],
            "meta": {"current_page": 1},
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.request = AsyncMock(return_value=mock_response)
        
        nba_client._client = mock_httpx_client
        
        result = await nba_client.get_games(
            start_date="2024-01-25", end_date="2024-01-25"
        )
        
        assert "data" in result
        assert len(result["data"]) == 1
        assert result["data"][0]["id"] == 12345
    
    @pytest.mark.asyncio
    async def test_rate_limit_error(self, nba_client, mock_httpx_client):
        """Test rate limit error handling."""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_httpx_client.request = AsyncMock(return_value=mock_response)
        
        nba_client._client = mock_httpx_client
        
        with pytest.raises(NBAAPIClientError, match="Rate limit exceeded"):
            await nba_client.get_player(237)
    
    @pytest.mark.asyncio
    async def test_server_error(self, nba_client, mock_httpx_client):
        """Test server error handling."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_httpx_client.request = AsyncMock(return_value=mock_response)
        
        nba_client._client = mock_httpx_client
        
        with pytest.raises(NBAAPIClientError, match="Server error"):
            await nba_client.get_player(237)
    
    @pytest.mark.asyncio
    async def test_close_client(self, nba_client, mock_httpx_client):
        """Test client cleanup."""
        nba_client._client = mock_httpx_client
        
        await nba_client.close()
        
        assert nba_client._client is None
        mock_httpx_client.aclose.assert_called_once()

import asyncio
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.config import settings


class NBAAPIClientError(Exception):
    """Base exception for NBA API client errors."""
    pass


class NBAAPINotFoundError(NBAAPIClientError):
    """Raised when a resource is not found."""
    pass


class NBAAPITimeoutError(NBAAPIClientError):
    """Raised when API request times out."""
    pass


class NBAAPIClient:
    """
    Client for interacting with BallDontLie NBA API.
    
    Provides methods to fetch player stats, game information, and betting odds.
    Includes retry logic and error handling.
    """
    
    def __init__(self):
        self.base_url = settings.balldontlie_api_url
        self.api_key = settings.balldontlie_api_key
        self.timeout = settings.request_timeout
        self._client: Optional[httpx.AsyncClient] = None
        
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=headers,
                timeout=self.timeout,
                follow_redirects=True,
            )
        return self._client
    
    async def close(self):
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
        reraise=True,
    )
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make HTTP request with retry logic.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            Response data as dictionary
            
        Raises:
            NBAAPINotFoundError: When resource is not found
            NBAAPITimeoutError: When request times out
            NBAAPIClientError: For other API errors
        """
        client = await self._get_client()
        
        try:
            response = await client.request(
                method=method,
                url=endpoint,
                params=params,
            )
            
            if response.status_code == 404:
                raise NBAAPINotFoundError(f"Resource not found: {endpoint}")
            elif response.status_code == 429:
                raise NBAAPIClientError("Rate limit exceeded")
            elif response.status_code >= 500:
                raise NBAAPIClientError(f"Server error: {response.status_code}")
            
            response.raise_for_status()
            return response.json()
            
        except httpx.TimeoutException as e:
            raise NBAAPITimeoutError(f"Request timeout: {endpoint}") from e
        except httpx.HTTPStatusError as e:
            raise NBAAPIClientError(f"HTTP error: {e.response.status_code}") from e
        except httpx.RequestError as e:
            raise NBAAPIClientError(f"Request failed: {str(e)}") from e
    
    async def get_players(
        self,
        search: Optional[str] = None,
        page: int = 1,
        per_page: int = 25,
    ) -> Dict[str, Any]:
        """
        Get list of NBA players.
        
        Args:
            search: Search term for player name
            page: Page number
            per_page: Results per page
            
        Returns:
            Dictionary with 'data' (list of players) and 'meta' (pagination info)
        """
        params = {
            "page": page,
            "per_page": per_page,
        }
        if search:
            params["search"] = search
        
        return await self._make_request("GET", "/players", params=params)
    
    async def get_player(self, player_id: int) -> Dict[str, Any]:
        """
        Get player details by ID.
        
        Args:
            player_id: Player ID
            
        Returns:
            Player data dictionary
        """
        response = await self._make_request("GET", f"/players/{player_id}")
        return response.get("data", response)
    
    async def get_player_stats(
        self,
        player_id: int,
        season: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get player statistics.
        
        Args:
            player_id: Player ID
            season: Optional season year (e.g., 2024 for 2024-25 season)
            
        Returns:
            Dictionary with player stats
        """
        params = {
            "player_ids[]": player_id,
            "per_page": 100,
        }
        if season:
            params["seasons[]"] = season
        
        return await self._make_request("GET", "/stats", params=params)
    
    async def get_games(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        team_id: Optional[int] = None,
        page: int = 1,
        per_page: int = 25,
    ) -> Dict[str, Any]:
        """
        Get games by date range.
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            team_id: Filter by team ID
            page: Page number
            per_page: Results per page
            
        Returns:
            Dictionary with 'data' (list of games) and 'meta' (pagination info)
        """
        params = {
            "page": page,
            "per_page": per_page,
        }
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if team_id:
            params["team_ids[]"] = team_id
        
        return await self._make_request("GET", "/games", params=params)
    
    async def get_live_games(self) -> Dict[str, Any]:
        """
        Get live and upcoming games.
        
        Returns today's and upcoming games.
        
        Returns:
            Dictionary with game data
        """
        today = datetime.now().strftime("%Y-%m-%d")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        return await self.get_games(
            start_date=today,
            end_date=tomorrow,
            per_page=100,
        )
    
    async def get_game(self, game_id: int) -> Dict[str, Any]:
        """
        Get game details by ID.
        
        Args:
            game_id: Game ID
            
        Returns:
            Game data dictionary
        """
        response = await self._make_request("GET", f"/games/{game_id}")
        return response.get("data", response)
    
    async def get_team(self, team_id: int) -> Dict[str, Any]:
        """
        Get team details by ID.
        
        Args:
            team_id: Team ID
            
        Returns:
            Team data dictionary
        """
        response = await self._make_request("GET", f"/teams/{team_id}")
        return response.get("data", response)


# Singleton instance
_nba_client: Optional[NBAAPIClient] = None


async def get_nba_client() -> NBAAPIClient:
    """
    Dependency injection function for FastAPI routes.
    
    Returns:
        NBA API client instance
    """
    global _nba_client
    if _nba_client is None:
        _nba_client = NBAAPIClient()
    return _nba_client


async def close_nba_client():
    """Close the NBA API client."""
    global _nba_client
    if _nba_client:
        await _nba_client.close()
        _nba_client = None

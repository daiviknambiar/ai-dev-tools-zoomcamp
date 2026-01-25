import os
from typing import Optional, Dict, Any, List
import requests
from requests.exceptions import RequestException, Timeout


class APIClientError(Exception):
    """Base exception for API client errors."""
    pass


class APIClient:
    """
    Centralized API client for communicating with the FastAPI backend.
    
    Handles all HTTP requests, error handling, and response parsing.
    """
    
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL for backend API. Defaults to env variable or localhost.
        """
        self.base_url = base_url or os.getenv(
            "BACKEND_URL", "http://localhost:8000"
        )
        self.api_prefix = "/api/v1"
        self.timeout = 30
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make HTTP request to backend API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON request body
            
        Returns:
            Response data as dictionary
            
        Raises:
            APIClientError: When request fails
        """
        url = f"{self.base_url}{self.api_prefix}{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                timeout=self.timeout,
            )
            
            if response.status_code == 404:
                raise APIClientError(f"Resource not found: {endpoint}")
            elif response.status_code >= 500:
                raise APIClientError(f"Server error: {response.status_code}")
            
            response.raise_for_status()
            return response.json()
            
        except Timeout:
            raise APIClientError(f"Request timeout for {endpoint}")
        except RequestException as e:
            raise APIClientError(f"Request failed: {str(e)}")
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check API health status.
        
        Returns:
            Health status information
        """
        return self._make_request("GET", "/health")
    
    def get_players(
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
            Dictionary with 'data' (players list) and 'meta' (pagination)
        """
        params = {"page": page, "per_page": per_page}
        if search:
            params["search"] = search
        
        return self._make_request("GET", "/players", params=params)
    
    def get_player(self, player_id: int) -> Dict[str, Any]:
        """
        Get player details by ID.
        
        Args:
            player_id: Player ID
            
        Returns:
            Player data dictionary
        """
        return self._make_request("GET", f"/players/{player_id}")
    
    def get_player_stats(
        self,
        player_id: int,
        season: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get player statistics.
        
        Args:
            player_id: Player ID
            season: Optional season year
            
        Returns:
            Player statistics
        """
        params = {}
        if season:
            params["season"] = season
        
        return self._make_request("GET", f"/players/{player_id}/stats", params=params)
    
    def get_live_games(self) -> Dict[str, Any]:
        """
        Get live and upcoming games.
        
        Returns:
            Dictionary with live games data
        """
        return self._make_request("GET", "/games/live")
    
    def get_game(self, game_id: int) -> Dict[str, Any]:
        """
        Get game details by ID.
        
        Args:
            game_id: Game ID
            
        Returns:
            Game data dictionary
        """
        return self._make_request("GET", f"/games/{game_id}")
    
    def get_games(
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
            Dictionary with games list
        """
        params = {"page": page, "per_page": per_page}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if team_id:
            params["team_id"] = team_id
        
        return self._make_request("GET", "/games", params=params)


# Singleton instance
_api_client: Optional[APIClient] = None


def get_api_client() -> APIClient:
    """
    Get or create API client instance.
    
    Returns:
        API client instance
    """
    global _api_client
    if _api_client is None:
        _api_client = APIClient()
    return _api_client

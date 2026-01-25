from typing import Optional
from pydantic import BaseModel, Field


class Team(BaseModel):
    """NBA team information."""
    
    id: int = Field(..., description="Team ID", example=14)
    name: str = Field(..., description="Team name", example="LA Lakers")
    full_name: Optional[str] = Field(None, description="Full team name", example="Los Angeles Lakers")
    abbreviation: str = Field(..., description="Team abbreviation", example="LAL")
    city: Optional[str] = Field(None, description="Team city", example="Los Angeles")
    conference: Optional[str] = Field(None, description="Conference", example="West")
    division: Optional[str] = Field(None, description="Division", example="Pacific")


class Player(BaseModel):
    """NBA player information."""
    
    id: int = Field(..., description="Player ID", example=237)
    first_name: str = Field(..., description="Player first name", example="LeBron")
    last_name: str = Field(..., description="Player last name", example="James")
    position: Optional[str] = Field(None, description="Player position", example="F")
    height: Optional[str] = Field(None, description="Player height", example="6-9")
    weight: Optional[str] = Field(None, description="Player weight in lbs", example="250")
    jersey_number: Optional[str] = Field(None, description="Jersey number", example="23")
    college: Optional[str] = Field(None, description="College", example="St. Vincent-St. Mary HS (OH)")
    country: Optional[str] = Field(None, description="Country", example="USA")
    draft_year: Optional[int] = Field(None, description="Draft year", example=2003)
    draft_round: Optional[int] = Field(None, description="Draft round", example=1)
    draft_number: Optional[int] = Field(None, description="Draft pick number", example=1)
    team: Optional[Team] = Field(None, description="Current team")


class PlayerStats(BaseModel):
    """Player statistics."""
    
    games_played: int = Field(..., description="Games played", example=45)
    minutes: Optional[str] = Field(None, description="Minutes per game", example="35.2")
    points: float = Field(..., description="Points per game", example=25.3)
    rebounds: float = Field(..., description="Rebounds per game", example=7.5)
    assists: float = Field(..., description="Assists per game", example=8.1)
    steals: Optional[float] = Field(None, description="Steals per game", example=1.3)
    blocks: Optional[float] = Field(None, description="Blocks per game", example=0.6)
    turnovers: Optional[float] = Field(None, description="Turnovers per game", example=3.5)
    field_goal_pct: Optional[float] = Field(None, description="Field goal percentage", example=0.523)
    three_point_pct: Optional[float] = Field(None, description="3-point percentage", example=0.412)
    free_throw_pct: Optional[float] = Field(None, description="Free throw percentage", example=0.750)
    season: int = Field(..., description="Season year", example=2024)


class PlayerDetail(Player):
    """Player with detailed statistics."""
    
    current_season_stats: Optional[PlayerStats] = Field(
        None, 
        description="Current season statistics"
    )


class PaginationMeta(BaseModel):
    """Pagination metadata."""
    
    current_page: int = Field(..., description="Current page number", example=1)
    next_page: Optional[int] = Field(None, description="Next page number", example=2)
    per_page: int = Field(..., description="Results per page", example=25)
    total_pages: Optional[int] = Field(None, description="Total pages", example=10)
    total_count: Optional[int] = Field(None, description="Total count", example=250)


class PlayersListResponse(BaseModel):
    """Response for player list endpoint."""
    
    data: list[Player] = Field(..., description="List of players")
    meta: PaginationMeta = Field(..., description="Pagination metadata")


class PlayerDetailResponse(BaseModel):
    """Response for player detail endpoint."""
    
    data: PlayerDetail = Field(..., description="Player details")


class PlayerStatsResponse(BaseModel):
    """Response for player stats endpoint."""
    
    data: list[PlayerStats] = Field(..., description="Player statistics by season")


class ErrorResponse(BaseModel):
    """Error response."""
    
    error: str = Field(..., description="Error message", example="Resource not found")
    detail: Optional[str] = Field(
        None, 
        description="Detailed error information",
        example="Player with ID 999999 does not exist"
    )

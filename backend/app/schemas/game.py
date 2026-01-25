from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.player import Team


class BettingOutcome(BaseModel):
    """Betting outcome for a market."""
    
    name: str = Field(..., description="Outcome name", example="LA Lakers")
    price: float = Field(..., description="Odds price", example=-150)
    point: Optional[float] = Field(None, description="Point spread/total", example=-5.5)


class BettingOdds(BaseModel):
    """Betting odds information."""
    
    bookmaker: str = Field(..., description="Bookmaker name", example="DraftKings")
    market_type: str = Field(
        ..., 
        description="Market type",
        example="h2h"
    )
    outcomes: list[BettingOutcome] = Field(..., description="Betting outcomes")
    last_update: Optional[datetime] = Field(
        None, 
        description="Last update timestamp"
    )


class Game(BaseModel):
    """NBA game information."""
    
    id: int = Field(..., description="Game ID", example=12345)
    date: datetime = Field(..., description="Game date and time")
    season: int = Field(..., description="Season year", example=2024)
    status: str = Field(..., description="Game status", example="Final")
    period: Optional[int] = Field(None, description="Current/final period", example=4)
    time: Optional[str] = Field(None, description="Game clock", example="Final")
    home_team: Team = Field(..., description="Home team")
    visitor_team: Team = Field(..., description="Visitor team")
    home_team_score: int = Field(..., description="Home team score", example=108)
    visitor_team_score: int = Field(..., description="Visitor team score", example=105)


class GameWithOdds(Game):
    """Game with betting odds."""
    
    betting_odds: list[BettingOdds] = Field(
        default_factory=list,
        description="Betting odds for the game"
    )


class GamesListResponse(BaseModel):
    """Response for games list endpoint."""
    
    data: list[Game] = Field(..., description="List of games")
    meta: Optional[dict] = Field(None, description="Metadata")


class LiveGamesResponse(BaseModel):
    """Response for live games endpoint."""
    
    data: list[GameWithOdds] = Field(..., description="List of live/upcoming games with odds")


class GameDetailResponse(BaseModel):
    """Response for game detail endpoint."""
    
    data: GameWithOdds = Field(..., description="Game details with odds")

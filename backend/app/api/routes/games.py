from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.game import (
    GamesListResponse,
    LiveGamesResponse,
    GameDetailResponse,
    GameWithOdds,
    ErrorResponse,
)
from app.services.nba_api_client import (
    NBAAPIClient,
    get_nba_client,
    NBAAPINotFoundError,
    NBAAPIClientError,
)


router = APIRouter()


@router.get(
    "/games/live",
    response_model=LiveGamesResponse,
    responses={
        500: {"model": ErrorResponse},
    },
)
async def get_live_games(
    client: NBAAPIClient = Depends(get_nba_client),
):
    """
    Get currently live or upcoming NBA games with betting odds.
    
    Returns games from today and tomorrow.
    """
    try:
        games_data = await client.get_live_games()
        games = games_data.get("data", [])
        
        # Convert to GameWithOdds format
        # Note: BallDontLie free tier may not include betting odds
        # This is a placeholder for when odds data is available
        games_with_odds = [
            {
                **game,
                "betting_odds": [],  # Placeholder for odds data
            }
            for game in games
        ]
        
        return LiveGamesResponse(data=games_with_odds)
    except NBAAPIClientError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/games/{game_id}",
    response_model=GameDetailResponse,
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def get_game(
    game_id: int,
    client: NBAAPIClient = Depends(get_nba_client),
):
    """
    Get detailed information about a specific game including betting odds.
    
    - **game_id**: The ID of the game to retrieve
    """
    try:
        game_data = await client.get_game(game_id)
        
        # Add betting odds placeholder
        game_with_odds = {
            **game_data,
            "betting_odds": [],  # Placeholder for odds data
        }
        
        return GameDetailResponse(data=game_with_odds)
    except NBAAPINotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Game with ID {game_id} not found",
        )
    except NBAAPIClientError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/games",
    response_model=GamesListResponse,
    responses={
        500: {"model": ErrorResponse},
    },
)
async def get_games(
    start_date: Optional[str] = Query(
        None,
        description="Start date (YYYY-MM-DD)",
        regex=r"^\d{4}-\d{2}-\d{2}$",
    ),
    end_date: Optional[str] = Query(
        None,
        description="End date (YYYY-MM-DD)",
        regex=r"^\d{4}-\d{2}-\d{2}$",
    ),
    team_id: Optional[int] = Query(None, description="Filter by team ID"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(25, ge=1, le=100, description="Results per page"),
    client: NBAAPIClient = Depends(get_nba_client),
):
    """
    Get NBA games for a specific date range.
    
    - **start_date**: Start date in YYYY-MM-DD format (optional)
    - **end_date**: End date in YYYY-MM-DD format (optional)
    - **team_id**: Filter by team ID (optional)
    - **page**: Page number for pagination (default: 1)
    - **per_page**: Number of results per page (default: 25, max: 100)
    """
    try:
        games_data = await client.get_games(
            start_date=start_date,
            end_date=end_date,
            team_id=team_id,
            page=page,
            per_page=per_page,
        )
        
        return GamesListResponse(
            data=games_data.get("data", []),
            meta=games_data.get("meta"),
        )
    except NBAAPIClientError as e:
        raise HTTPException(status_code=500, detail=str(e))

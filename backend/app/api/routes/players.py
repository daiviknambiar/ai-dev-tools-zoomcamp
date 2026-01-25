from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.player import (
    PlayersListResponse,
    PlayerDetailResponse,
    PlayerStatsResponse,
    PaginationMeta,
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
    "/players",
    response_model=PlayersListResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def list_players(
    search: Optional[str] = Query(None, description="Search players by name"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(25, ge=1, le=100, description="Results per page"),
    client: NBAAPIClient = Depends(get_nba_client),
):
    """
    Get a list of NBA players with optional filtering.
    
    - **search**: Search term for player name (optional)
    - **page**: Page number for pagination (default: 1)
    - **per_page**: Number of results per page (default: 25, max: 100)
    """
    try:
        data = await client.get_players(search=search, page=page, per_page=per_page)
        
        return PlayersListResponse(
            data=data.get("data", []),
            meta=PaginationMeta(
                current_page=data.get("meta", {}).get("current_page", page),
                next_page=data.get("meta", {}).get("next_page"),
                per_page=data.get("meta", {}).get("per_page", per_page),
                total_pages=data.get("meta", {}).get("total_pages"),
                total_count=data.get("meta", {}).get("total_count"),
            ),
        )
    except NBAAPIClientError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/players/{player_id}",
    response_model=PlayerDetailResponse,
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def get_player(
    player_id: int,
    client: NBAAPIClient = Depends(get_nba_client),
):
    """
    Get detailed information for a specific player.
    
    - **player_id**: The ID of the player to retrieve
    """
    try:
        player_data = await client.get_player(player_id)
        
        # Try to get current season stats
        try:
            stats_data = await client.get_player_stats(player_id, season=2024)
            stats = stats_data.get("data", [])
            current_season_stats = stats[0] if stats else None
        except Exception:
            current_season_stats = None
        
        return PlayerDetailResponse(
            data={
                **player_data,
                "current_season_stats": current_season_stats,
            }
        )
    except NBAAPINotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Player with ID {player_id} not found",
        )
    except NBAAPIClientError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/players/{player_id}/stats",
    response_model=PlayerStatsResponse,
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def get_player_stats(
    player_id: int,
    season: Optional[int] = Query(None, description="Season year (e.g., 2024)"),
    client: NBAAPIClient = Depends(get_nba_client),
):
    """
    Get season and career statistics for a specific player.
    
    - **player_id**: The ID of the player
    - **season**: Optional season year (e.g., 2024 for 2024-25 season)
    """
    try:
        stats_data = await client.get_player_stats(player_id, season=season)
        return PlayerStatsResponse(data=stats_data.get("data", []))
    except NBAAPINotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Stats for player ID {player_id} not found",
        )
    except NBAAPIClientError as e:
        raise HTTPException(status_code=500, detail=str(e))

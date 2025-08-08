"""
FastAPI application entry point for the Farkle backend.

This module wires together the database, CRUD layer and Pydantic schemas to
expose a RESTful API.  It intentionally contains minimal business logic;
database interactions are delegated to ``crud.py``.
"""

from typing import List
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Query

from .database import Base, engine, get_db
from .schemas import (
    PlayerCreateRequest,
    GameResultRequest,
    PlayerStatsResponse,
    LeaderboardEntry,
)
from .crud import (
    create_player,
    create_game_result,
    get_player_stats,
    get_leaderboard,
    get_user_players,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Farkle Backend", version="0.2.0")


@app.post("/create-player", summary="Create a new player profile")
def create_player_endpoint(
    request: PlayerCreateRequest,
    db = Depends(get_db),
):
    """Create a new player profile for a given user.

    If the user doesn't already exist it will be created automatically.  Returns
    the newly created ``player_id``.
    """
    return {"player_id": create_player(db, request.user_id, request.display_name)}


@app.post("/game-result", summary="Submit a completed game session")
def post_game_result_endpoint(
    request: GameResultRequest,
    db = Depends(get_db),
):
    """Submit a completed game session including results for each participating player.

    A new ``Game`` row is created and ``GameResult`` rows are linked to individual
    players.  Users and players must already exist; unknown ``player_id`` values
    will result in an HTTP 404.
    """
    return {
        "game_id": create_game_result(
            db,
            request.user_id,
            request.played_at,
            request.results,
        )
    }


@app.get(
    "/player-stats",
    response_model=PlayerStatsResponse,
    summary="Get aggregated stats for a player",
)
def player_stats_endpoint(
    player_id: str = Query(..., description="ID of the player"),
    db = Depends(get_db),
):
    """Return aggregated statistics for a single player profile."""
    return get_player_stats(db, player_id)


@app.get(
    "/leaderboard",
    response_model=List[LeaderboardEntry],
    summary="Get leaderboard",
)
def leaderboard_endpoint(
    sort: str = Query(
        "avg_score",
        description="Sort field: 'avg_score', 'wins', or 'total_points'",
        pattern="^(avg_score|wins|total_points)$",
    ),
    limit: int = Query(25, ge=1, le=100, description="Number of results to return"),
    db = Depends(get_db),
):
    """Return the leaderboard sorted by the specified field."""
    return get_leaderboard(db, sort, limit)


@app.get(
    "/user-players",
    response_model=List[LeaderboardEntry],
    summary="List all players for a user",
)
def user_players_endpoint(
    user_id: str = Query(..., description="User ID to list players for"),
    db = Depends(get_db),
):
    """Return all player profiles associated with a given user."""
    return get_user_players(db, user_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
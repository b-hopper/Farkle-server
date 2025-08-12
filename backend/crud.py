"""
CRUD helper functions for the Farkle backend.

These functions encapsulate the database logic used by the API.  Moving
database operations into a separate module improves testability and keeps
the FastAPI endpoint functions small and focused on request/response
handling.
"""

import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import func, cast, Integer
from sqlalchemy.orm import Session

from .models import User, PlayerProfile, Game, GameResult


def create_player(db: Session, user_id: str, display_name: str) -> str:
    """Ensure the user exists and create a new player profile.

    If the user does not already exist, an anonymous user record is created.
    Returns the generated player_id.
    """
    user = db.get(User, user_id)
    if not user:
        user = User(user_id=user_id, login_type="anonymous")
        db.add(user)
        db.commit()
        db.refresh(user)
    # Create the player profile
    player_id = str(uuid.uuid4())
    profile = PlayerProfile(
        player_id=player_id,
        user_id=user.user_id,
        display_name=display_name,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return player_id


def create_game_result(
    db: Session,
    user_id: str,
    played_at: Optional[datetime],
    results: List,
) -> str:
    """Create a game session and associated results.

    ``results`` is a list of objects/dicts with keys ``player_id``, ``score``,
    ``turns``, ``farkles`` and ``won``.  If the user or any referenced
    player does not exist, an HTTPException is raised with a 404 status.
    Returns the new ``game_id``.
    """
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    game_id = str(uuid.uuid4())
    game = Game(
        game_id=game_id,
        user_id=user.user_id,
        played_at=played_at or datetime.utcnow(),
    )
    db.add(game)
    for res in results:
        # ``res`` may be a Pydantic model or a dict-like object.  Use attribute
        # access first then fallback to dict indexing.
        player_id = getattr(res, "player_id", None) or res.get("player_id")
        score = getattr(res, "score", None) or res.get("score")
        turns = getattr(res, "turns", None) or res.get("turns")
        farkles = getattr(res, "farkles", None) or res.get("farkles")
        won = getattr(res, "won", None) or res.get("won")
        player = db.get(PlayerProfile, player_id)
        if not player:
            raise HTTPException(status_code=404, detail=f"Player {player_id} not found")
        result = GameResult(
            result_id=str(uuid.uuid4()),
            game_id=game_id,
            player_id=player_id,
            score=score,
            turns_taken=turns,
            farkles=farkles,
            won=won,
        )
        db.add(result)
    db.commit()
    return game_id


def get_player_stats(db: Session, player_id: str) -> dict:
    """Return aggregated statistics for a single player profile.

    Calculates number of games played, wins, total points, average score,
    total farkles, and the highest single-game score.  If the player does
    not exist, an HTTPException is raised.
    Returns a dictionary compatible with ``PlayerStatsResponse``.
    """
    player = db.get(PlayerProfile, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    stats = (
        db.query(
            func.count(GameResult.result_id).label("games_played"),
            func.sum(cast(GameResult.won, Integer)).label("wins"),
            func.sum(GameResult.score).label("total_points"),
            func.avg(GameResult.score).label("avg_score"),
            func.sum(GameResult.farkles).label("total_farkles"),
            func.max(GameResult.score).label("high_score"),
        )
        .filter(GameResult.player_id == player_id)
        .one()
    )
    games_played = stats.games_played or 0
    avg_score = float(stats.avg_score) if stats.avg_score is not None else 0.0
    return {
        "player_id": player.player_id,
        "display_name": player.display_name,
        "games_played": games_played,
        "wins": int(stats.wins or 0),
        "total_points": int(stats.total_points or 0),
        "avg_score": avg_score,
        "total_farkles": int(stats.total_farkles or 0),
        "high_score": int(stats.high_score or 0),
    }


def get_leaderboard(db: Session, sort: str, limit: int):
    """Return a leaderboard sorted by the specified field.

    The leaderboard includes all players aggregated across all games.  Sorting
    options include average score, wins, and total points.  ``limit``
    restricts the number of rows returned.  Returns a list of dictionaries
    compatible with ``LeaderboardEntry``.
    """
    aggregation = (
        db.query(
            PlayerProfile.player_id,
            PlayerProfile.display_name,
            func.sum(cast(GameResult.won, Integer)).label("wins"),
            func.avg(GameResult.score).label("avg_score"),
            func.sum(GameResult.score).label("total_points"),
        )
        .join(GameResult, PlayerProfile.player_id == GameResult.player_id)
        .group_by(PlayerProfile.player_id, PlayerProfile.display_name)
        .all()
    )
    sorted_list = sorted(
        aggregation,
        key=lambda row: (getattr(row, sort) or 0),
        reverse=True,
    )[:limit]
    return [
        {
            "player_id": row.player_id,
            "display_name": row.display_name,
            "wins": int(row.wins or 0),
            "avg_score": float(row.avg_score or 0.0),
            "total_points": int(row.total_points or 0),
        }
        for row in sorted_list
    ]



def get_user_players(db: Session, user_id: str):
    """Return all player profiles associated with a given user.

    Each entry includes basic statistics (wins, average score, total points).
    Returns a list of dictionaries compatible with ``LeaderboardEntry``.  If
    the user does not exist, an HTTPException is raised.
    """
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    results = (
        db.query(
            PlayerProfile.player_id,
            PlayerProfile.display_name,
            func.sum(cast(GameResult.won, Integer)).label("wins"),
            func.avg(GameResult.score).label("avg_score"),
            func.sum(GameResult.score).label("total_points"),
        )
        .join(GameResult, PlayerProfile.player_id == GameResult.player_id, isouter=True)
        .filter(PlayerProfile.user_id == user_id)
        .group_by(PlayerProfile.player_id, PlayerProfile.display_name)
        .all()
    )
    return [
        {
            "player_id": row.player_id,
            "display_name": row.display_name,
            "wins": int(row.wins or 0),
            "avg_score": float(row.avg_score or 0.0),
            "total_points": int(row.total_points or 0),
        }
        for row in results
    ]

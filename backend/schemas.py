"""
Pydantic schemas for request and response bodies.

These classes define the structure of JSON payloads accepted by and
returned from the API.  Using Pydantic ensures data validation and
automatic documentation generation in FastAPI.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class PlayerCreateRequest(BaseModel):
    user_id: str = Field(..., description="UUID or Google ID of the user")
    display_name: str = Field(..., description="Name of the local player")


class GameResultEntry(BaseModel):
    player_id: str
    score: int
    turns: int
    farkles: int
    won: bool


class GameResultRequest(BaseModel):
    user_id: str
    played_at: Optional[datetime] = None
    results: List[GameResultEntry]


class PlayerStatsResponse(BaseModel):
    player_id: str
    display_name: str
    games_played: int
    wins: int
    total_points: int
    avg_score: float
    total_farkles: int
    high_score: int


class PlayerInfoEntry(BaseModel):
    player_id: str
    display_name: str
    wins: int
    avg_score: float
    total_points: int


class LeaderboardResponse(BaseModel):
    rows: List[PlayerInfoEntry]

class PlayerInfoResponse(BaseModel):
    players: List[PlayerInfoEntry]
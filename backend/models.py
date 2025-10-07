"""
SQLAlchemy ORM models for the Farkle backend.

These classes map to tables in the database and define relationships
between users, player profiles, games, and game results.  The models
are imported by the CRUD layer and by Alembic for future migrations.
"""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"
    # A user can be identified by a Google Play Games ID or a locally generated
    # UUID.  Using string columns avoids database-specific UUID types and
    # keeps the code portable.
    user_id: str = Column(String, primary_key=True, index=True)
    login_type: str = Column(String, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    # Relationships
    players = relationship("PlayerProfile", back_populates="user")
    games = relationship("Game", back_populates="user")


class PlayerProfile(Base):
    __tablename__ = "player_profiles"
    player_id: str = Column(String, primary_key=True, index=True)
    user_id: str = Column(String, ForeignKey("users.user_id"), nullable=False)
    display_name: str = Column(String, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    # Relationships
    user = relationship("User", back_populates="players")
    results = relationship("GameResult", back_populates="player", passive_deletes=True)


class Game(Base):
    __tablename__ = "games"
    game_id: str = Column(String, primary_key=True, index=True)
    user_id: str = Column(String, ForeignKey("users.user_id"), nullable=False)
    played_at: datetime = Column(DateTime, default=datetime.utcnow)
    # Relationships
    user = relationship("User", back_populates="games")
    results = relationship("GameResult", back_populates="game")


class GameResult(Base):
    __tablename__ = "game_results"
    result_id: str = Column(String, primary_key=True, index=True)
    game_id: str = Column(String, ForeignKey("games.game_id"), nullable=False)
    player_id: str = Column(String,
                            ForeignKey("player_profiles.player_id", ondelete="SET NULL"),
                            nullable=True,
                            index=True)
    score: int = Column(Integer, nullable=False)
    turns_taken: int = Column(Integer, nullable=False)
    farkles: int = Column(Integer, nullable=False)
    won: bool = Column(Boolean, nullable=False)
    # Relationships
    game = relationship("Game", back_populates="results")
    player = relationship("PlayerProfile", back_populates="results")

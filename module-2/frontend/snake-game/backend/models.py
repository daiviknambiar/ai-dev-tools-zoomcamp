"""
SQLAlchemy ORM models for the Snake Game application.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    leaderboard_entries = relationship("LeaderboardEntry", back_populates="user")
    games = relationship("Game", back_populates="user")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "loginTime": self.created_at.isoformat() if self.created_at else None,
        }


class LeaderboardEntry(Base):
    __tablename__ = "leaderboard"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    username = Column(String(255), nullable=False)
    score = Column(Integer, nullable=False, index=True)
    mode = Column(String(50), nullable=False)  # 'walls' or 'pass-through'
    date = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="leaderboard_entries")

    def to_dict(self):
        return {
            "id": self.id,
            "userId": self.user_id,
            "username": self.username,
            "score": self.score,
            "mode": self.mode,
            "date": self.date.isoformat() if self.date else None,
        }


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    username = Column(String(255), nullable=False)
    mode = Column(String(50), nullable=False)  # 'walls' or 'pass-through'
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    score = Column(Integer, nullable=True)
    is_active = Column(Integer, default=1)  # SQLite compatibility: use int as bool

    # Relationships
    user = relationship("User", back_populates="games")

    def to_dict(self):
        return {
            "id": self.id,
            "userId": self.user_id,
            "username": self.username,
            "mode": self.mode,
            "startTime": self.start_time.isoformat() if self.start_time else None,
            "endTime": self.end_time.isoformat() if self.end_time else None,
            "score": self.score,
            "isActive": bool(self.is_active),
        }

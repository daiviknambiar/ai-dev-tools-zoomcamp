"""
FastAPI backend for Snake Game with SQLAlchemy ORM database support.
Supports PostgreSQL and SQLite.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session

from database import SessionLocal, init_db
from models import User, LeaderboardEntry, Game

# Initialize database tables (lazy init for tests)
_db_initialized = False

def ensure_db_init():
    """Ensure database is initialized only once."""
    global _db_initialized
    if not _db_initialized:
        try:
            init_db()
            _db_initialized = True
        except Exception:
            # Database may already be initialized or we're in a test environment
            pass

app = FastAPI(title="Snake Game Backend")

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic request models
class LoginRequest(BaseModel):
    username: str
    password: str


class SignupRequest(BaseModel):
    username: str
    email: str
    password: str


class ScoreRequest(BaseModel):
    score: int
    mode: str


class StartGameRequest(BaseModel):
    mode: str


class EndGameRequest(BaseModel):
    score: Optional[int] = None


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Helper functions
def current_time():
    return datetime.utcnow().isoformat()


def seed_default_users(db: Session):
    """Seed database with default test users if empty."""
    if db.query(User).count() == 0:
        default_users = [
            User(username="player1", email="player1@test.com", password="pass123"),
            User(username="player2", email="player2@test.com", password="pass123"),
            User(username="speedmaster", email="speed@test.com", password="pass123"),
        ]
        db.add_all(default_users)
        db.commit()
        
        # Seed leaderboard entries
        leaderboard_entries = [
            LeaderboardEntry(user_id=1, username="player1", score=150, mode="walls"),
            LeaderboardEntry(user_id=2, username="player2", score=230, mode="pass-through"),
        ]
        db.add_all(leaderboard_entries)
        db.commit()




# Routes: Authentication
@app.post("/auth/login")
async def login(payload: LoginRequest, db: Session = Depends(get_db)):
    ensure_db_init()
    seed_default_users(db)
    
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or user.password != payload.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return JSONResponse(status_code=200, content={"user": user.to_dict()})


@app.post("/auth/signup")
async def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    seed_default_users(db)
    
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(username=payload.username, email=payload.email, password=payload.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return JSONResponse(status_code=201, content={"user": new_user.to_dict()})


@app.post("/auth/logout")
async def logout():
    return {"success": True}


@app.get("/auth/me")
async def me():
    raise HTTPException(status_code=401, detail="Not authenticated")



# Routes: Leaderboard
@app.get("/leaderboard")
async def get_leaderboard(mode: Optional[str] = "all", limit: int = 50, db: Session = Depends(get_db)):
    seed_default_users(db)
    
    query = db.query(LeaderboardEntry)
    if mode and mode != "all":
        query = query.filter(LeaderboardEntry.mode == mode)
    
    entries = query.order_by(LeaderboardEntry.score.desc()).limit(limit).all()
    return {"leaderboard": [e.to_dict() for e in entries]}


@app.post("/leaderboard")
async def submit_score(payload: ScoreRequest, db: Session = Depends(get_db)):
    seed_default_users(db)
    
    # Use first user (player1) for now
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    entry = LeaderboardEntry(
        user_id=user.id,
        username=user.username,
        score=payload.score,
        mode=payload.mode
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)

    return JSONResponse(status_code=201, content={"entry": entry.to_dict()})


@app.get("/users/me/highscore")
async def user_highscore(mode: Optional[str] = "all", db: Session = Depends(get_db)):
    seed_default_users(db)
    
    user = db.query(User).first()
    if not user:
        return {"highScore": 0}

    query = db.query(LeaderboardEntry).filter(LeaderboardEntry.user_id == user.id)
    if mode and mode != "all":
        query = query.filter(LeaderboardEntry.mode == mode)

    high = max([e.score for e in query.all()], default=0)
    return {"highScore": high}



# Routes: Active Games
@app.get("/active-games")
async def active_games(db: Session = Depends(get_db)):
    seed_default_users(db)
    
    # Return mock active games (for spectator mode)
    mock_players = [
        {
            "id": 1,
            "username": "speedmaster",
            "mode": "walls",
            "currentScore": 120,
            "gameStartTime": current_time(),
            "isPlaying": True,
        },
        {
            "id": 2,
            "username": "player1",
            "mode": "pass-through",
            "currentScore": 80,
            "gameStartTime": current_time(),
            "isPlaying": True,
        },
    ]
    return {"games": mock_players}


# Routes: Games
@app.post("/games")
async def start_game(payload: StartGameRequest, db: Session = Depends(get_db)):
    seed_default_users(db)
    
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    game = Game(
        user_id=user.id,
        username=user.username,
        mode=payload.mode,
        is_active=1
    )
    db.add(game)
    db.commit()
    db.refresh(game)

    return JSONResponse(status_code=201, content={"gameSession": game.to_dict()})


@app.get("/games/{game_id}")
async def game_state(game_id: int, db: Session = Depends(get_db)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        return {"gameId": game_id, "timestamp": current_time()}

    return {"gameId": game_id, "timestamp": current_time(), **game.to_dict()}


@app.post("/games/{game_id}/end")
async def end_game(game_id: int, payload: Optional[EndGameRequest] = None, db: Session = Depends(get_db)):
    game = db.query(Game).filter(Game.id == game_id).first()
    
    if game:
        game.end_time = datetime.utcnow()
        game.score = payload.score if payload else None
        game.is_active = 0
        db.commit()

    return {
        "gameId": game_id,
        "score": payload.score if payload else None,
        "endTime": current_time(),
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

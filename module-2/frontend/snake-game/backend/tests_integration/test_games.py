"""
Integration tests for game endpoints.
Uses SQLite in-memory database.
"""

def test_start_game(client):
    """Test starting a game."""
    response = client.post("/games", json={"mode": "walls"})
    
    assert response.status_code == 201
    data = response.json()
    assert data["gameSession"]["mode"] == "walls"
    assert data["gameSession"]["isActive"] is True
    assert "startTime" in data["gameSession"]


def test_get_game_state(client):
    """Test getting a game's state."""
    # Start a game
    start_response = client.post("/games", json={"mode": "pass-through"})
    game_id = start_response.json()["gameSession"]["id"]
    
    # Get game state
    response = client.get(f"/games/{game_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["gameId"] == game_id
    assert "timestamp" in data


def test_end_game(client):
    """Test ending a game."""
    # Start a game
    start_response = client.post("/games", json={"mode": "walls"})
    game_id = start_response.json()["gameSession"]["id"]
    
    # End game with score
    response = client.post(f"/games/{game_id}/end", json={"score": 500})
    assert response.status_code == 200
    data = response.json()
    assert data["gameId"] == game_id
    assert data["score"] == 500
    assert "endTime" in data


def test_end_game_without_score(client):
    """Test ending a game without score."""
    # Start a game
    start_response = client.post("/games", json={"mode": "pass-through"})
    game_id = start_response.json()["gameSession"]["id"]
    
    # End game without score
    response = client.post(f"/games/{game_id}/end")
    assert response.status_code == 200
    data = response.json()
    assert data["gameId"] == game_id
    assert data["score"] is None


def test_get_active_games(client):
    """Test getting active games."""
    response = client.get("/active-games")
    
    assert response.status_code == 200
    data = response.json()
    assert "games" in data
    assert isinstance(data["games"], list)
    # Should have mock players
    assert len(data["games"]) > 0


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

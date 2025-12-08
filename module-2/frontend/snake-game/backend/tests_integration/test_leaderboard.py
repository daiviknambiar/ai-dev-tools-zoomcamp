"""
Integration tests for leaderboard endpoints.
Uses SQLite in-memory database.
"""

def test_get_leaderboard(client):
    """Test retrieving leaderboard."""
    response = client.get("/leaderboard")
    
    assert response.status_code == 200
    data = response.json()
    assert "leaderboard" in data
    assert isinstance(data["leaderboard"], list)


def test_get_leaderboard_by_mode(client):
    """Test retrieving leaderboard filtered by mode."""
    # Submit scores
    client.post("/leaderboard", json={"score": 100, "mode": "walls"})
    client.post("/leaderboard", json={"score": 150, "mode": "pass-through"})
    
    # Get walls mode
    response = client.get("/leaderboard?mode=walls")
    assert response.status_code == 200
    data = response.json()
    for entry in data["leaderboard"]:
        assert entry["mode"] == "walls"
    
    # Get pass-through mode
    response = client.get("/leaderboard?mode=pass-through")
    assert response.status_code == 200
    data = response.json()
    for entry in data["leaderboard"]:
        assert entry["mode"] == "pass-through"


def test_submit_score(client):
    """Test submitting a score."""
    response = client.post("/leaderboard", json={
        "score": 250,
        "mode": "walls"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["entry"]["score"] == 250
    assert data["entry"]["mode"] == "walls"


def test_get_user_highscore(client):
    """Test getting user's high score."""
    # Submit multiple scores
    client.post("/leaderboard", json={"score": 100, "mode": "walls"})
    client.post("/leaderboard", json={"score": 150, "mode": "walls"})
    client.post("/leaderboard", json={"score": 200, "mode": "pass-through"})
    
    # Get high score for all modes
    response = client.get("/users/me/highscore")
    assert response.status_code == 200
    assert response.json()["highScore"] == 200
    
    # Get high score for specific mode
    response = client.get("/users/me/highscore?mode=walls")
    assert response.status_code == 200
    assert response.json()["highScore"] == 150


def test_leaderboard_sorted_by_score(client):
    """Test that leaderboard is sorted by score (highest first)."""
    # Submit scores in random order
    client.post("/leaderboard", json={"score": 100, "mode": "walls"})
    client.post("/leaderboard", json={"score": 300, "mode": "walls"})
    client.post("/leaderboard", json={"score": 200, "mode": "walls"})
    
    response = client.get("/leaderboard?mode=walls")
    assert response.status_code == 200
    data = response.json()
    entries = data["leaderboard"]
    
    # Check sorted order
    scores = [e["score"] for e in entries]
    assert scores == sorted(scores, reverse=True)

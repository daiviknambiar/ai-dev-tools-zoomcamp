"""
Integration tests for authentication endpoints.
Uses SQLite in-memory database.
"""

import pytest


def test_login_success(client):
    """Test successful login."""
    # Signup first
    client.post("/auth/signup", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    
    # Login
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["username"] == "testuser"
    assert data["user"]["email"] == "test@example.com"


def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    response = client.post("/auth/login", json={
        "username": "nonexistent",
        "password": "wrongpass"
    })
    
    assert response.status_code == 401
    assert "Invalid" in response.json()["detail"]


def test_signup_success(client):
    """Test successful user signup."""
    response = client.post("/auth/signup", json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "password123"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["user"]["username"] == "newuser"
    assert data["user"]["email"] == "new@example.com"


def test_signup_duplicate_username(client):
    """Test signup with duplicate username."""
    # Create first user
    client.post("/auth/signup", json={
        "username": "duplicate",
        "email": "first@example.com",
        "password": "pass123"
    })
    
    # Try to create user with same username
    response = client.post("/auth/signup", json={
        "username": "duplicate",
        "email": "second@example.com",
        "password": "pass123"
    })
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_signup_duplicate_email(client):
    """Test signup with duplicate email."""
    # Create first user
    client.post("/auth/signup", json={
        "username": "user1",
        "email": "duplicate@example.com",
        "password": "pass123"
    })
    
    # Try to create user with same email
    response = client.post("/auth/signup", json={
        "username": "user2",
        "email": "duplicate@example.com",
        "password": "pass123"
    })
    
    assert response.status_code == 400
    assert "registered" in response.json()["detail"]


def test_logout(client):
    """Test logout endpoint."""
    response = client.post("/auth/logout")
    
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_me_not_authenticated(client):
    """Test /auth/me without authentication."""
    response = client.get("/auth/me")
    
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]

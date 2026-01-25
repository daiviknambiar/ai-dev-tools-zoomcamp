# Quick Start Guide

Get the NBA Stats & Betting Odds application running in under 5 minutes!

---

## 🚀 Option 1: Docker (Recommended)

**Prerequisites**: Docker and Docker Compose installed

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/nba-stats-betting-app.git
cd nba-stats-betting-app

# 2. Start all services
docker-compose up --build

# 3. Access the application
# Frontend: http://localhost:8501
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

That's it! 🎉

---

## 🔧 Option 2: Local Development

### Prerequisites

- Python 3.11+
- Git

### Backend Setup

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run backend
uvicorn app.main:app --reload --port 8000
```

Backend running at: http://localhost:8000

### Frontend Setup

**Open a new terminal**

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set backend URL (create .streamlit/secrets.toml)
mkdir -p .streamlit
echo '[api]' > .streamlit/secrets.toml
echo 'backend_url = "http://localhost:8000"' >> .streamlit/secrets.toml

# 6. Run frontend
streamlit run app.py
```

Frontend will open automatically at: http://localhost:8501

---

## ✅ Verify Installation

### Check Backend Health

```bash
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-25T10:00:00Z",
  "version": "1.0.0"
}
```

### Check Frontend

1. Open http://localhost:8501
2. Look for "✅ API Connected" in sidebar
3. Try searching for a player (e.g., "LeBron")

---

## 🧪 Run Tests

### Backend Tests

```bash
cd backend
pytest --cov=app --cov-report=html
```

View coverage: `open htmlcov/index.html`

### Frontend Tests

```bash
cd frontend
pytest -v
```

---

## 🐛 Troubleshooting

### Port Already in Use

If ports 8000 or 8501 are busy:

```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different ports
uvicorn app.main:app --port 8001
streamlit run app.py --server.port 8502
```

### Module Not Found

```bash
# Make sure you're in the virtual environment
which python  # Should show venv path

# Reinstall dependencies
pip install -r requirements.txt
```

### API Connection Failed

1. Ensure backend is running
2. Check backend URL in frontend secrets
3. Verify CORS settings in `backend/app/main.py`

---

## 📚 Next Steps

- Read [README.md](README.md) for full documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for cloud deployment
- See [TESTING.md](TESTING.md) for testing guidelines
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for system design

---

## 🆘 Need Help?

- Check GitHub Issues
- Read the documentation
- Contact the maintainers

**Happy coding! 🏀**

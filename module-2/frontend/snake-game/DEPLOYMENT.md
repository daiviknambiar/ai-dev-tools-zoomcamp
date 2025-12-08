# Snake Game - Deployment Guide

This document covers building and deploying the Snake Game (frontend + backend in a single container).

## Project Structure

```
module-2/frontend/snake-game/
├── Dockerfile                 # Multi-stage Docker build
├── .dockerignore              # Optimize Docker build
├── render.yaml                # Render.com IaC definition
├── RENDER_DEPLOYMENT.md       # Detailed Render deployment steps
├── package.json               # Frontend npm scripts
├── index.html                 # Frontend entry point
├── js/                        # Frontend JavaScript modules
├── css/                       # Frontend styles
├── backend/
│   ├── main.py               # FastAPI backend with static file serving
│   ├── database.py           # SQLAlchemy ORM configuration
│   ├── models.py             # Database models (User, LeaderboardEntry, Game)
│   ├── pyproject.toml        # Python dependencies via uv
│   ├── .env.example          # Environment variable template
│   └── tests_integration/    # Integration tests (SQLite)
```

## Local Development

### Prerequisites

- Node.js 18+ (for frontend)
- Python 3.13+ (for backend)
- uv package manager (`pip install uv`)
- Docker (for containerized testing)

### Setup

1. **Install dependencies:**

```bash
cd module-2/frontend/snake-game

# Backend dependencies
cd backend && uv sync && cd ..

# Frontend dependencies (if not using container)
npm install
```

2. **Configure environment:**

```bash
cp backend/.env.example backend/.env
# Edit backend/.env as needed (defaults are fine for local dev)
```

3. **Initialize database:**

```bash
cd backend
uv run python -c "from database import init_db; init_db()"
cd ..
```

### Run Locally

**Option 1: Run backend and frontend separately**

```bash
# Terminal 1: Start backend
cd backend
uv run python -m uvicorn main:app --port 8000 --reload

# Terminal 2: Start frontend
npm run serve
# or with Node.js http-server:
python3 -m http.server 3000
```

**Option 2: Run concurrently**

```bash
npm run dev
# This runs both backend (8000) and frontend (3000) via concurrently
```

**Option 3: Run containerized**

```bash
# Build Docker image
docker build -t snake-game:latest .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=sqlite:////tmp/snake_game.db \
  snake-game:latest

# Access at http://localhost:8000
```

### Testing

```bash
cd backend

# Run all integration tests
uv run pytest tests_integration/ -v

# Run specific test
uv run pytest tests_integration/test_auth.py -v

# Run with coverage
uv run pytest tests_integration/ --cov --cov-report=html
```

## Docker Build

### Build Locally

```bash
cd module-2/frontend/snake-game

# Build image
docker build -t snake-game:latest .

# Build with build arguments
docker build -t snake-game:latest \
  --build-arg PYTHON_VERSION=3.13 \
  --build-arg NODE_VERSION=20 \
  .

# Verify image
docker images | grep snake-game
docker run -it snake-game:latest /bin/bash
```

### Push to Registry

```bash
# Docker Hub
docker tag snake-game:latest yourusername/snake-game:latest
docker push yourusername/snake-game:latest

# GitHub Container Registry
docker tag snake-game:latest ghcr.io/yourusername/snake-game:latest
docker push ghcr.io/yourusername/snake-game:latest
```

## Render Deployment

### Option 1: Deploy with render.yaml (Recommended)

```bash
# 1. Push to GitHub repository
git add render.yaml
git commit -m "Add Render deployment configuration"
git push origin main

# 2. Go to https://dashboard.render.com
# 3. Click "New" → "Blueprint"
# 4. Connect GitHub repository
# 5. Select render.yaml
# 6. Click "Create"
```

### Option 2: Manual Dashboard Deployment

1. **Create PostgreSQL Database:**
   - Dashboard → New+ → PostgreSQL
   - Copy **Internal Database URL**

2. **Create Web Service:**
   - Dashboard → New+ → Web Service
   - Runtime: Docker
   - Image URL: `yourusername/snake-game:latest`
   - Port: 8000
   - Health Check: `/health`

3. **Configure Environment:**
   - DATABASE_URL: (from PostgreSQL service)
   - DEBUG: false

See [RENDER_DEPLOYMENT.md](./RENDER_DEPLOYMENT.md) for detailed steps.

## Environment Variables

### Backend Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./snake_game.db` | Database connection string |
| `DEBUG` | `false` | Enable debug logging |
| `CORS_ORIGINS` | `*` | CORS allowed origins (comma-separated) |

### Database URLs

**SQLite (Local Development):**
```
sqlite:///./snake_game.db
```

**PostgreSQL:**
```
postgresql://user:password@localhost:5432/database
```

**Render PostgreSQL (from service):**
Automatically injected via `fromDatabase` in render.yaml

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Documentation
```
http://localhost:8000/docs       # Swagger UI
http://localhost:8000/redoc      # ReDoc
```

### Frontend
```
http://localhost:8000/           # Served via FastAPI static files
```

## Architecture

### Multi-Stage Docker Build

1. **Frontend Stage:**
   - Node.js 20 Alpine
   - Installs npm dependencies
   - Builds/copies static files

2. **Backend Builder Stage:**
   - Python 3.13 Slim
   - Installs uv package manager
   - Syncs Python dependencies

3. **Final Runtime Stage:**
   - Python 3.13 Slim (minimal)
   - Copies virtual environment from builder
   - Mounts frontend static files
   - Runs FastAPI with Uvicorn

### Benefits
- Minimal final image size (~500MB)
- All dependencies baked in
- No runtime compilation needed
- Fast startup and deployment

## Database

### Tables
- `user` - User accounts and authentication
- `leaderboard_entry` - Score submissions
- `game` - Game sessions and results

### Migrations

For schema changes:

```bash
# Create migration (if using Alembic)
alembic revision --autogenerate -m "Add new column"

# Apply migration
alembic upgrade head
```

Currently using direct ORM model approach (run `init_db()` to create schema).

## Scaling

### Increase Capacity

**Upgrade from Free → Starter:**
- Render Dashboard → Service Settings
- Plan: Starter ($7/month)
- Restarts on code changes, no auto-shutdown

### Performance Monitoring

```bash
# Check service logs
render logs --service-id <service-id>

# View metrics
# Render Dashboard → Metrics tab
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs <container-id>

# Common issues:
# - PORT already in use: docker run -p 9000:8000 ...
# - Missing .env: Set DATABASE_URL environment variable
```

### Database Connection Error

```bash
# Verify DATABASE_URL format
echo $DATABASE_URL

# For SQLite: sqlite:///path/to/db.db
# For Postgres: postgresql://user:pass@host:port/db
```

### Slow First Request

- Normal on free tier (waking from idle)
- Upgrade to Starter plan for always-on

### Frontend Not Loading

1. Check if `index.html` is being served:
   ```bash
   curl http://localhost:8000/
   ```
2. Verify FastAPI static file mounting in `main.py`
3. Check Docker build includes frontend files

## Production Checklist

- [ ] Set `DEBUG=false` in environment
- [ ] Use PostgreSQL (not SQLite) for production
- [ ] Restrict `CORS_ORIGINS` 
- [ ] Enable HTTPS/SSL
- [ ] Set up automated backups
- [ ] Configure monitoring/alerting
- [ ] Use strong database passwords
- [ ] Enable auto-deployment from GitHub
- [ ] Test database failover
- [ ] Document deployment process

## Support & Resources

- [Render Documentation](https://render.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [SQLAlchemy Postgres](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## Next Steps

1. Build and test Docker image locally
2. Push to Docker Hub or GitHub Container Registry
3. Deploy to Render via render.yaml or dashboard
4. Monitor logs and health checks
5. Set up auto-deployment from GitHub
6. Upgrade to Starter plan for production use

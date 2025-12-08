# Render Deployment Guide

This guide walks through deploying the Snake Game to Render.com with a containerized setup.

## Prerequisites

- [Render.com](https://render.com) account
- Docker image built and optionally pushed to Docker Hub or GitHub Container Registry
- PostgreSQL database (Render can provision this)

## Option 1: Deploy with Render.yaml (Recommended)

Render.yaml allows you to define your entire infrastructure as code.

### 1. Create `render.yaml` in project root:

```yaml
services:
  - type: web
    name: snake-game-backend
    runtime: docker
    dockerfilePath: ./module-2/frontend/snake-game/Dockerfile
    dockerContext: ./module-2/frontend/snake-game
    region: oregon
    plan: free  # or starter, standard, etc.
    
    # Environment variables
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: snake-game-db
          property: connectionString
    
    # Port configuration
    ports:
      - port: 8000
        protocol: http
    
    # Health check
    healthCheckPath: /health
    
    # Deployment settings
    maxInstances: 1
    minInstances: 1

  # PostgreSQL database
  - type: pserv
    name: snake-game-db
    ipAllowList: []  # Allow all IPs
    plan: free  # or starter, standard, etc.
    region: oregon
    postgresMajorVersion: 15

  # Redis (optional, for caching/sessions)
  # - type: redis
  #   name: snake-game-redis
  #   region: oregon
  #   plan: free
```

### 2. Deploy using Render CLI or dashboard:

**Using Render CLI:**
```bash
npm install -g @render-com/cli
render deploy --file render.yaml
```

**Using Dashboard:**
1. Go to https://dashboard.render.com
2. Click "New" → "Blueprint"
3. Connect your GitHub repository
4. Select the `render.yaml` file
5. Click "Deploy"

## Option 2: Deploy Manually via Dashboard

### Step 1: Create a PostgreSQL Database

1. Go to https://dashboard.render.com
2. Click "New+" → "PostgreSQL"
3. Configuration:
   - **Name**: `snake-game-db`
   - **Database**: `snakedb`
   - **User**: `snakeuser`
   - **Region**: Choose closest to you (e.g., Oregon)
   - **Plan**: Free (1 GB storage, shared CPU)
4. Click "Create Database"
5. Copy the **Internal Database URL** - you'll need this

### Step 2: Deploy Backend as Docker Service

1. Build and push Docker image to Docker Hub or GitHub Container Registry:

```bash
# Login to Docker Hub
docker login

# Build image
docker build -t yourusername/snake-game:latest \
  -f module-2/frontend/snake-game/Dockerfile \
  module-2/frontend/snake-game/

# Push image
docker push yourusername/snake-game:latest
```

2. In Render Dashboard, click "New+" → "Web Service"
3. Configuration:
   - **Name**: `snake-game`
   - **Runtime**: `Docker`
   - **Image URL**: `yourusername/snake-game:latest`
   - **Region**: Same as database (e.g., Oregon)
   - **Plan**: Free (512 MB RAM, shared CPU)
   - **Port**: `8000`
   - **Health Check Path**: `/health`

4. Environment Variables (click "Advanced"):
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the Internal Database URL from PostgreSQL service
   - Format should be: `postgresql://user:password@host:port/database`

5. Click "Create Web Service"

### Step 3: Configure Database Connection

1. Go to your PostgreSQL service in Render Dashboard
2. Copy the **Internal Database URL**
3. Go to your Web Service → "Environment"
4. Add/update the `DATABASE_URL` variable with the Internal URL

## Environment Variables

Configure these in your Render service:

```
DATABASE_URL=postgresql://user:password@host:port/database
DEBUG=false
CORS_ORIGINS=*  # Restrict in production
```

## Post-Deployment

### Initialize Database

Run migrations/initialization:

```bash
# SSH into service (via Render Dashboard)
# Or use render CLI
render exec snake-game-backend -- python -c "from database import init_db; init_db()"
```

### Access Your App

- **Backend API**: `https://snake-game.onrender.com`
- **Health Check**: `https://snake-game.onrender.com/health`
- **API Docs**: `https://snake-game.onrender.com/docs` (Swagger UI)
- **Frontend**: `https://snake-game.onrender.com/` (served via FastAPI static files)

## Troubleshooting

### Deployment Fails

1. Check Render build logs in Dashboard
2. Verify `DATABASE_URL` is correctly set
3. Ensure PostgreSQL service is in same region
4. Check Docker image builds locally: `docker build -f Dockerfile .`

### App Crashes After Deploy

1. Check logs: Render Dashboard → Service → Logs
2. Common issues:
   - Database connection string incorrect
   - PostgreSQL service not running
   - Port mismatch (should be 8000)

### Database Connection Errors

1. Verify DATABASE_URL format:
   ```
   postgresql://username:password@host:port/database
   ```
2. Check PostgreSQL service status in Dashboard
3. Use Internal URL for connections within Render

### Frontend Not Loading

1. Verify static files mounted in FastAPI
2. Check that `index.html` is in correct directory
3. Frontend files should be at same level as backend when deployed

## Performance Tips

### For Free Tier

- Free tier services auto-spin down after 15 min inactivity
- First request after sleep may take 30+ seconds
- Upgrade to Starter plan ($7/month) for always-on

### Database Optimization

- Use connection pooling (SQLAlchemy uses this by default)
- Consider Render Redis for session caching
- Monitor query performance in logs

### Scaling

- Starter plan: $7/month per service
- Standard plan: $12/month per service
- Configure autoscaling in service settings

## Monitoring

### View Logs

```bash
render logs snake-game-backend
```

### Health Endpoint

```bash
curl https://snake-game.onrender.com/health
```

### Metrics

Render Dashboard shows:
- CPU usage
- Memory usage
- Request count
- Build logs
- Deployment history

## Production Checklist

- [ ] Set `DEBUG=false`
- [ ] Restrict `CORS_ORIGINS` (remove `*`)
- [ ] Use strong database password
- [ ] Enable automatic deployments from GitHub
- [ ] Set up error monitoring (e.g., Sentry)
- [ ] Configure backup for PostgreSQL
- [ ] Test database restoration process

## Redeployment

### Automatic (Recommended)

1. Go to Web Service → Settings
2. "Auto-Deploy" → "Yes"
3. Redeploys on every push to main branch

### Manual

```bash
# Via Render CLI
render deploy --service-id <service-id>

# Or push to trigger auto-deploy if enabled
git push origin main
```

## Cost Estimation

**Free Tier** (for testing):
- Web Service: Free (auto-spins down)
- PostgreSQL: Free (100 MB)
- Total: $0/month

**Production Setup** (Starter Plan):
- Web Service: $7/month
- PostgreSQL Starter: $15/month
- Total: $22/month

## Support

- [Render Documentation](https://render.com/docs)
- [Render Community](https://render.com/community)
- Render Support: support@render.com

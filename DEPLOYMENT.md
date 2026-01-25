# Deployment Guide

This document provides comprehensive instructions for deploying the NBA Stats & Betting Odds application to various cloud platforms.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Streamlit Cloud Deployment (Recommended)](#streamlit-cloud-deployment-recommended)
- [Alternative Deployment Options](#alternative-deployment-options)
- [Environment Variables](#environment-variables)
- [Deployment Verification](#deployment-verification)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before deploying, ensure you have:

1. **GitHub Account**: Application code pushed to a GitHub repository
2. **Streamlit Cloud Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **API Access**: (Optional) BallDontLie API key if required
4. **Local Testing**: Verified application works locally

---

## Streamlit Cloud Deployment (Recommended)

Streamlit Cloud offers free hosting for Streamlit applications with built-in support for Python backends.

### Step 1: Prepare Your Repository

Ensure your repository has the correct structure:

```
your-repo/
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   └── .streamlit/
│       └── config.toml
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── ...
└── README.md
```

### Step 2: Deploy Frontend to Streamlit Cloud

1. **Go to Streamlit Cloud**: Navigate to [share.streamlit.io](https://share.streamlit.io)

2. **Sign in with GitHub**: Authorize Streamlit Cloud to access your repositories

3. **Create New App**:
   - Click "New app"
   - Select your repository
   - Set **Main file path**: `frontend/app.py`
   - Set **Python version**: 3.11
   - Click "Advanced settings"

4. **Configure Secrets** (in Advanced settings):
   ```toml
   [api]
   backend_url = "YOUR_BACKEND_URL"  # We'll update this after backend deployment
   ```

5. **Deploy**: Click "Deploy"

The frontend will be available at: `https://your-app-name.streamlit.app`

### Step 3: Deploy Backend

#### Option A: Streamlit Cloud (Multi-Page App Approach)

For a simplified deployment, you can run both frontend and backend through Streamlit Cloud by creating a background process for FastAPI.

**Not Recommended for Production** - Use separate backend deployment instead.

#### Option B: Railway (Recommended for Backend)

1. **Sign up for Railway**: Go to [railway.app](https://railway.app)

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Select the `backend` directory

3. **Configure Build**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables**:
   ```
   DEBUG=False
   APP_NAME=NBA Stats API
   BALLDONTLIE_API_URL=https://api.balldontlie.io/v1
   ```

5. **Deploy**: Railway will automatically deploy

6. **Get Backend URL**: Copy the generated URL (e.g., `https://your-backend.up.railway.app`)

#### Option C: Render

1. **Sign up for Render**: Go to [render.com](https://render.com)

2. **Create Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `backend` directory

3. **Configure Service**:
   - **Name**: nba-stats-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables**:
   ```
   DEBUG=False
   BALLDONTLIE_API_URL=https://api.balldontlie.io/v1
   ```

5. **Deploy**: Click "Create Web Service"

6. **Get Backend URL**: Copy the service URL

### Step 4: Update Frontend Configuration

1. Go back to Streamlit Cloud dashboard
2. Click on your app → "Settings" → "Secrets"
3. Update the backend URL:
   ```toml
   [api]
   backend_url = "https://your-backend.railway.app"  # or Render URL
   ```
4. Save and reboot the app

### Step 5: Verify Deployment

1. Visit your Streamlit app URL
2. Check that "✅ API Connected" appears in the sidebar
3. Test player search functionality
4. Check live games page

---

## Alternative Deployment Options

### Docker Deployment (Self-Hosted)

If you have your own server or cloud instance:

1. **Install Docker and Docker Compose**:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   sudo apt-get install docker-compose
   ```

2. **Clone Repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/nba-stats-betting-app.git
   cd nba-stats-betting-app
   ```

3. **Start Services**:
   ```bash
   docker-compose up -d
   ```

4. **Access Application**:
   - Frontend: http://your-server:8501
   - Backend API: http://your-server:8000
   - API Docs: http://your-server:8000/docs

### AWS Deployment

#### Backend on Elastic Beanstalk

1. **Install EB CLI**:
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB Application**:
   ```bash
   cd backend
   eb init -p python-3.11 nba-stats-backend
   ```

3. **Create Environment**:
   ```bash
   eb create nba-stats-backend-env
   ```

4. **Deploy**:
   ```bash
   eb deploy
   ```

#### Frontend on Streamlit Cloud

Deploy frontend as described above, pointing to your EB backend URL.

### Google Cloud Platform

#### Backend on Cloud Run

1. **Build Container**:
   ```bash
   cd backend
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/nba-stats-backend
   ```

2. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy nba-stats-backend \
     --image gcr.io/YOUR_PROJECT_ID/nba-stats-backend \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

3. **Get Service URL**: Note the deployed service URL

4. **Deploy Frontend**: Use Streamlit Cloud pointing to Cloud Run URL

---

## Environment Variables

### Backend Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DEBUG` | Enable debug mode | No | `False` |
| `APP_NAME` | Application name | No | `NBA Stats & Betting Odds API` |
| `BALLDONTLIE_API_URL` | BallDontLie API base URL | Yes | `https://api.balldontlie.io/v1` |
| `BALLDONTLIE_API_KEY` | API key (if required) | No | None |
| `REQUEST_TIMEOUT` | API request timeout (seconds) | No | `30` |
| `MAX_RETRIES` | Max retry attempts | No | `3` |

### Frontend Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BACKEND_URL` | Backend API URL | Yes |

---

## Deployment Verification

### Health Check Endpoints

1. **Backend Health**:
   ```bash
   curl https://your-backend-url/api/v1/health
   ```
   
   Expected response:
   ```json
   {
     "status": "healthy",
     "timestamp": "2024-01-25T10:00:00Z",
     "version": "1.0.0"
   }
   ```

2. **Frontend Health**:
   ```bash
   curl https://your-frontend-url/_stcore/health
   ```

### Functional Tests

1. **Test Player Search**:
   ```bash
   curl "https://your-backend-url/api/v1/players?search=LeBron"
   ```

2. **Test Live Games**:
   ```bash
   curl "https://your-backend-url/api/v1/games/live"
   ```

3. **Visit Frontend**: Navigate to your Streamlit URL and test:
   - Player search functionality
   - Live games display
   - Navigation between pages

---

## Troubleshooting

### Common Issues

#### 1. Frontend Can't Connect to Backend

**Symptoms**: "❌ API Connection Failed" in sidebar

**Solutions**:
- Verify backend is deployed and running
- Check backend URL in Streamlit secrets is correct
- Ensure backend URL includes protocol (`https://`)
- Check CORS settings in backend allow frontend origin

**Fix CORS**:
```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.streamlit.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 2. Backend Timeout Errors

**Symptoms**: Requests timeout or fail

**Solutions**:
- Check BallDontLie API is accessible
- Increase timeout in backend config
- Verify network connectivity
- Check API rate limits

#### 3. Module Not Found Errors

**Symptoms**: Import errors on deployment

**Solutions**:
- Ensure all dependencies in `requirements.txt`
- Check Python version compatibility (3.11+)
- Verify file paths are correct

#### 4. Memory/Resource Issues

**Symptoms**: Application crashes or slow performance

**Solutions**:
- Upgrade to paid tier with more resources
- Optimize API calls and caching
- Reduce concurrent requests

### Logs and Debugging

#### Streamlit Cloud Logs

1. Go to Streamlit Cloud dashboard
2. Click on your app
3. View "Logs" tab for real-time output

#### Railway Logs

1. Go to Railway dashboard
2. Select your project
3. Click "View Logs"

#### Render Logs

1. Go to Render dashboard
2. Select your service
3. View "Logs" tab

### Getting Help

- **GitHub Issues**: Report bugs at repository issues page
- **Streamlit Forum**: [discuss.streamlit.io](https://discuss.streamlit.io)
- **Stack Overflow**: Tag questions with `streamlit` and `fastapi`

---

## Performance Optimization

### Backend Optimization

1. **Enable Caching**:
   ```python
   # Add caching for frequent requests
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def get_player_cached(player_id: int):
       return client.get_player(player_id)
   ```

2. **Connection Pooling**: Already configured in httpx client

3. **Rate Limiting**: Implement to prevent API abuse

### Frontend Optimization

1. **Streamlit Caching**:
   ```python
   @st.cache_data(ttl=300)  # Cache for 5 minutes
   def fetch_players(search_term):
       return api_client.get_players(search=search_term)
   ```

2. **Lazy Loading**: Load data only when needed

3. **Pagination**: Implement for large datasets

---

## Monitoring and Analytics

### Uptime Monitoring

Use services like:
- **UptimeRobot**: Free uptime monitoring
- **Pingdom**: Comprehensive monitoring
- **StatusCake**: Free tier available

### Application Analytics

- **Streamlit Analytics**: Built into Streamlit Cloud
- **Google Analytics**: Add to frontend
- **Custom Logging**: Log usage patterns

---

## Continuous Deployment

The project includes GitHub Actions workflows for automated deployment:

1. **Commit Changes**: Push to main branch
   ```bash
   git add .
   git commit -m "Update feature"
   git push origin main
   ```

2. **Automatic Tests**: CI workflow runs tests

3. **Automatic Deployment**: CD workflow deploys on success

4. **Verify**: Check deployment logs in GitHub Actions

---

## Cost Estimation

### Free Tier Deployment

- **Streamlit Cloud**: Free for public repos
- **Railway**: $5/month credit (enough for small apps)
- **Render**: Free tier available with limitations

**Total**: $0-5/month

### Production Deployment

- **Streamlit Cloud**: $250/month (Team plan)
- **Railway**: ~$20/month (scaled backend)
- **Domain**: ~$12/year

**Total**: ~$282/month

---

## Next Steps

After deployment:

1. ✅ Set up custom domain (optional)
2. ✅ Configure SSL certificates (automatic with most platforms)
3. ✅ Set up monitoring and alerts
4. ✅ Create backup procedures
5. ✅ Document known issues and workarounds

---

## Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] All tests passing locally
- [ ] Environment variables configured
- [ ] Backend deployed and accessible
- [ ] Frontend deployed and accessible
- [ ] Frontend connected to backend
- [ ] Health checks passing
- [ ] Functional tests passed
- [ ] Documentation updated
- [ ] Monitoring set up

---

**Deployment Status**: Once deployed, update the README with live URLs:
- Frontend: `https://your-app.streamlit.app`
- Backend API: `https://your-backend.railway.app`
- API Docs: `https://your-backend.railway.app/docs`

---

**Need Help?** Open an issue on GitHub or contact the maintainers.

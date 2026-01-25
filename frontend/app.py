import streamlit as st
from services.api_client import get_api_client, APIClientError


# Page configuration
st.set_page_config(
    page_title="NBA Stats & Betting Odds",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #888;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF6B6B;
        color: white;
    }
    .stButton>button:hover {
        background-color: #FF5252;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.markdown('<h1 class="main-header">🏀 NBA Stats & Betting Odds</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Your unified dashboard for NBA statistics and betting odds</p>',
    unsafe_allow_html=True,
)

# API Health Check
api_client = get_api_client()

try:
    health = api_client.health_check()
    if health.get("status") == "healthy":
        st.sidebar.success("✅ API Connected")
except APIClientError as e:
    st.sidebar.error(f"❌ API Connection Failed: {str(e)}")
    st.error(
        """
        **Unable to connect to backend API**
        
        Please ensure the backend server is running:
        ```bash
        cd backend
        uvicorn app.main:app --reload
        ```
        """
    )
    st.stop()

# Sidebar navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("---")

# About section
st.sidebar.markdown("### About")
st.sidebar.info(
    """
    This app combines NBA player statistics with live betting odds, 
    helping bettors make informed decisions quickly.
    
    **Features:**
    - 🔍 Player search and stats
    - 🔴 Live game scores
    - 📊 Betting odds (when available)
    - 📈 Statistical insights
    """
)

# Main content
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div style="
            padding: 2rem;
            border-radius: 0.5rem;
            background-color: #262730;
            text-align: center;
            border-top: 4px solid #FF6B6B;
        ">
            <h2>👤 Players</h2>
            <p>Search and explore NBA player statistics</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("")
    if st.button("Browse Players →", key="players_btn"):
        st.switch_page("pages/1_Players.py")

with col2:
    st.markdown(
        """
        <div style="
            padding: 2rem;
            border-radius: 0.5rem;
            background-color: #262730;
            text-align: center;
            border-top: 4px solid #4ECDC4;
        ">
            <h2>🔴 Live Games</h2>
            <p>View live games with scores and odds</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("")
    if st.button("Watch Live Games →", key="games_btn"):
        st.switch_page("pages/2_Live_Games.py")

with col3:
    st.markdown(
        """
        <div style="
            padding: 2rem;
            border-radius: 0.5rem;
            background-color: #262730;
            text-align: center;
            border-top: 4px solid #FFE66D;
        ">
            <h2>📊 API Docs</h2>
            <p>Explore the backend API documentation</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("")
    st.link_button("View API Docs →", "http://localhost:8000/docs", use_container_width=True)

st.markdown("---")

# Quick stats/info
st.markdown("### 🚀 Quick Start")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        **For Bettors:**
        1. Search for players in the Players section
        2. View current season statistics
        3. Check live games and betting odds
        4. Make informed betting decisions
        """
    )

with col2:
    st.markdown(
        """
        **Data Sources:**
        - NBA player stats from BallDontLie API
        - Real-time game scores
        - Betting odds (when available)
        - Historical performance data
        """
    )

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit and FastAPI | Data provided by BallDontLie.io")

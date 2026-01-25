import streamlit as st
from datetime import datetime
from services.api_client import get_api_client, APIClientError
from components.game_display import (
    display_game_card,
    display_live_games_header,
    display_no_games_message,
)
from components.player_card import display_error, display_loading


# Page configuration
st.set_page_config(
    page_title="Live NBA Games - Stats & Odds",
    page_icon="🔴",
    layout="wide",
)

# Header
display_live_games_header()

# API client
api_client = get_api_client()

# Auto-refresh toggle
st.sidebar.title("Settings")
auto_refresh = st.sidebar.checkbox("Auto-refresh (30s)", value=False)

if auto_refresh:
    st.sidebar.info("Page will refresh every 30 seconds")
    # Note: In production, you'd use st.rerun() with a timer

# Date filter
st.sidebar.markdown("---")
st.sidebar.markdown("### Filter Games")

# Get live games
try:
    with display_loading("Loading live games..."):
        response = api_client.get_live_games()
    
    games = response.get("data", [])
    
    if not games:
        display_no_games_message()
    else:
        # Show game count
        st.markdown(f"### 📊 {len(games)} Game(s) Found")
        st.markdown("---")
        
        # Filter games by status
        live_games = [g for g in games if g.get("status") == "InProgress"]
        upcoming_games = [g for g in games if g.get("status") == "Scheduled"]
        completed_games = [g for g in games if g.get("status") == "Final"]
        
        # Tabs for different game statuses
        if live_games or upcoming_games or completed_games:
            tabs = []
            tab_names = []
            
            if live_games:
                tab_names.append(f"🔴 Live ({len(live_games)})")
                tabs.append(live_games)
            
            if upcoming_games:
                tab_names.append(f"🟡 Upcoming ({len(upcoming_games)})")
                tabs.append(upcoming_games)
            
            if completed_games:
                tab_names.append(f"🟢 Final ({len(completed_games)})")
                tabs.append(completed_games)
            
            tab_objects = st.tabs(tab_names)
            
            for tab, games_list in zip(tab_objects, tabs):
                with tab:
                    for game in games_list:
                        display_game_card(game, show_odds=True)
                        st.markdown("")
        else:
            # Show all games if no status-based filtering
            for game in games:
                display_game_card(game, show_odds=True)
                st.markdown("")
    
    # Last updated
    st.sidebar.markdown("---")
    st.sidebar.caption(f"Last updated: {datetime.now().strftime('%I:%M:%S %p')}")
    
    if st.sidebar.button("🔄 Refresh Now"):
        st.rerun()

except APIClientError as e:
    display_error(f"Failed to load games: {str(e)}")
    st.info(
        """
        **Troubleshooting:**
        - Check if the backend API is running
        - Verify your internet connection
        - Try refreshing the page
        """
    )

# Sidebar - Additional filters
st.sidebar.markdown("---")
st.sidebar.markdown("### Date Range")

date_option = st.sidebar.radio(
    "Select date range",
    ["Today & Tomorrow", "Custom Range"],
    help="Filter games by date",
)

if date_option == "Custom Range":
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("Start date")
    with col2:
        end_date = st.date_input("End date")
    
    if st.sidebar.button("Apply Filter"):
        try:
            response = api_client.get_games(
                start_date=str(start_date),
                end_date=str(end_date),
            )
            games = response.get("data", [])
            
            st.success(f"Found {len(games)} games in date range")
            
            for game in games:
                display_game_card(game, show_odds=True)
        
        except APIClientError as e:
            display_error(f"Failed to load games: {str(e)}")

# Betting odds info
st.sidebar.markdown("---")
st.sidebar.markdown("### Betting Odds")
st.sidebar.info(
    """
    **Note:** Betting odds are provided when available from the data source.
    
    Odds may not be available for all games, especially practice or preseason games.
    """
)

# Help
st.sidebar.markdown("---")
st.sidebar.markdown("### Legend")
st.sidebar.markdown(
    """
    - 🔴 **Live**: Game in progress
    - 🟡 **Upcoming**: Scheduled game
    - 🟢 **Final**: Completed game
    """
)

# Back to home
st.sidebar.markdown("---")
if st.sidebar.button("← Back to Home"):
    st.switch_page("app.py")

# Footer
st.markdown("---")
st.caption("Live scores update in real-time | Betting odds provided when available")

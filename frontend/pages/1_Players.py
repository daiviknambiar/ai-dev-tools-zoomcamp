import streamlit as st
from services.api_client import get_api_client, APIClientError
from components.player_card import (
    display_player_card,
    display_search_box,
    display_error,
    display_info,
    display_loading,
)


# Page configuration
st.set_page_config(
    page_title="NBA Players - Stats & Odds",
    page_icon="👤",
    layout="wide",
)

# Header
st.title("👤 NBA Players")
st.markdown("Search and explore NBA player statistics and betting information")
st.markdown("---")

# API client
api_client = get_api_client()

# Search interface
search_query = display_search_box()

# Search button and results
if search_query:
    try:
        with display_loading(f"Searching for '{search_query}'..."):
            response = api_client.get_players(search=search_query, per_page=50)
        
        players = response.get("data", [])
        
        if not players:
            display_info(f"No players found matching '{search_query}'")
        else:
            st.success(f"Found {len(players)} player(s)")
            
            # Display players
            for player in players:
                with st.expander(
                    f"{player.get('first_name', '')} {player.get('last_name', '')} - "
                    f"{player.get('team', {}).get('abbreviation', 'N/A')}"
                ):
                    try:
                        # Try to get player details with stats
                        player_detail = api_client.get_player(player["id"])
                        player_data = player_detail.get("data", player)
                        
                        display_player_card(
                            player_data,
                            player_data.get("current_season_stats"),
                        )
                        
                        # Additional actions
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"View Full Stats", key=f"stats_{player['id']}"):
                                try:
                                    stats_response = api_client.get_player_stats(player["id"])
                                    stats_data = stats_response.get("data", [])
                                    
                                    if stats_data:
                                        st.markdown("#### Season Statistics")
                                        for stat in stats_data[:5]:  # Show last 5 seasons
                                            st.json(stat)
                                    else:
                                        st.info("No historical stats available")
                                except APIClientError as e:
                                    st.error(f"Error loading stats: {str(e)}")
                        
                    except APIClientError as e:
                        display_error(f"Error loading details for player: {str(e)}")
                        display_player_card(player)
    
    except APIClientError as e:
        display_error(f"Search failed: {str(e)}")

else:
    # Show popular players or instructions
    st.info(
        """
        👆 **How to use:**
        - Enter a player name in the search box above
        - Search works with first name, last name, or both
        - Example searches: "LeBron", "James", "LeBron James"
        - Click on a player to see detailed statistics
        """
    )
    
    # Featured players section
    st.markdown("### ⭐ Featured Players")
    st.markdown("Search for popular players:")
    
    col1, col2, col3, col4 = st.columns(4)
    
    featured_players = [
        ("LeBron James", col1),
        ("Stephen Curry", col2),
        ("Kevin Durant", col3),
        ("Giannis Antetokounmpo", col4),
    ]
    
    for player_name, col in featured_players:
        with col:
            if st.button(f"🔍 {player_name}", key=f"featured_{player_name}", use_container_width=True):
                st.rerun()

# Sidebar
st.sidebar.title("Filters")
st.sidebar.markdown("---")

# Team filter (would require team list from API)
st.sidebar.markdown("### Filter by Team")
st.sidebar.info("Team filtering coming soon!")

# Position filter
st.sidebar.markdown("### Filter by Position")
positions = st.sidebar.multiselect(
    "Select positions",
    ["PG", "SG", "SF", "PF", "C"],
    help="Filter players by position",
)

# Pagination info
if search_query:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Pagination")
    st.sidebar.info("Showing results from current search")

# Help section
st.sidebar.markdown("---")
st.sidebar.markdown("### Help")
st.sidebar.markdown(
    """
    **Tips:**
    - Be specific with player names
    - Use the search box to find any NBA player
    - Click on players to see detailed stats
    - Stats are updated regularly
    """
)

# Back to home
st.sidebar.markdown("---")
if st.sidebar.button("← Back to Home"):
    st.switch_page("app.py")

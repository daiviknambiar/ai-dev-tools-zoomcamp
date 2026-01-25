import streamlit as st
from typing import Optional, Dict, Any


def display_player_card(player: Dict[str, Any], stats: Optional[Dict[str, Any]] = None):
    """
    Display a player information card.
    
    Args:
        player: Player data dictionary
        stats: Optional player statistics
    """
    with st.container():
        st.markdown(
            f"""
            <div style="
                padding: 1.5rem;
                border-radius: 0.5rem;
                background-color: #262730;
                margin-bottom: 1rem;
                border-left: 4px solid #FF6B6B;
            ">
            """,
            unsafe_allow_html=True,
        )
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.subheader(f"{player.get('first_name', '')} {player.get('last_name', '')}")
            
            team = player.get("team", {})
            if team:
                st.text(f"🏀 {team.get('full_name', team.get('name', 'N/A'))}")
            
            info_items = []
            if player.get("position"):
                info_items.append(f"Position: {player['position']}")
            if player.get("height"):
                info_items.append(f"Height: {player['height']}")
            if player.get("weight"):
                info_items.append(f"Weight: {player['weight']} lbs")
            
            if info_items:
                st.text(" | ".join(info_items))
        
        with col2:
            if player.get("jersey_number"):
                st.markdown(
                    f"""
                    <div style="text-align: center; font-size: 3rem; font-weight: bold; color: #FF6B6B;">
                        #{player['jersey_number']}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        
        # Display stats if available
        if stats:
            st.markdown("---")
            st.markdown("**Season Stats**")
            
            stat_cols = st.columns(5)
            
            metrics = [
                ("PPG", stats.get("points", 0), "🏀"),
                ("RPG", stats.get("rebounds", 0), "🎯"),
                ("APG", stats.get("assists", 0), "🤝"),
                ("FG%", f"{stats.get('field_goal_pct', 0) * 100:.1f}%", "📊"),
                ("Games", stats.get("games_played", 0), "🎮"),
            ]
            
            for col, (label, value, emoji) in zip(stat_cols, metrics):
                with col:
                    st.metric(label, f"{emoji} {value}")
        
        st.markdown("</div>", unsafe_allow_html=True)


def display_player_comparison(player1: Dict[str, Any], player2: Dict[str, Any]):
    """
    Display side-by-side player comparison.
    
    Args:
        player1: First player data
        player2: Second player data
    """
    col1, col2 = st.columns(2)
    
    with col1:
        display_player_card(player1, player1.get("current_season_stats"))
    
    with col2:
        display_player_card(player2, player2.get("current_season_stats"))


def display_search_box() -> Optional[str]:
    """
    Display player search box.
    
    Returns:
        Search query string or None
    """
    search_query = st.text_input(
        "🔍 Search for a player",
        placeholder="Enter player name (e.g., LeBron James)",
        help="Search by player first name or last name",
    )
    
    return search_query if search_query else None


def display_error(message: str):
    """
    Display error message.
    
    Args:
        message: Error message to display
    """
    st.error(f"❌ {message}")


def display_info(message: str):
    """
    Display info message.
    
    Args:
        message: Info message to display
    """
    st.info(f"ℹ️ {message}")


def display_success(message: str):
    """
    Display success message.
    
    Args:
        message: Success message to display
    """
    st.success(f"✅ {message}")


def display_loading(message: str = "Loading..."):
    """
    Display loading spinner with message.
    
    Args:
        message: Loading message
    """
    return st.spinner(message)

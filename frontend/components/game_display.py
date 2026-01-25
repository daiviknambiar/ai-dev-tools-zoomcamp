import streamlit as st
from typing import Dict, Any, List
from datetime import datetime


def display_game_card(game: Dict[str, Any], show_odds: bool = True):
    """
    Display a game information card.
    
    Args:
        game: Game data dictionary
        show_odds: Whether to display betting odds
    """
    home_team = game.get("home_team", {})
    visitor_team = game.get("visitor_team", {})
    status = game.get("status", "Unknown")
    
    with st.container():
        st.markdown(
            f"""
            <div style="
                padding: 1.5rem;
                border-radius: 0.5rem;
                background-color: #262730;
                margin-bottom: 1rem;
                border-left: 4px solid #4ECDC4;
            ">
            """,
            unsafe_allow_html=True,
        )
        
        # Game header
        col1, col2 = st.columns([3, 1])
        
        with col1:
            game_date = game.get("date")
            if game_date:
                try:
                    dt = datetime.fromisoformat(game_date.replace("Z", "+00:00"))
                    formatted_date = dt.strftime("%b %d, %Y at %I:%M %p")
                    st.caption(f"📅 {formatted_date}")
                except:
                    st.caption(f"📅 {game_date}")
        
        with col2:
            status_color = {
                "Final": "🟢",
                "InProgress": "🔴",
                "Scheduled": "🟡",
            }.get(status, "⚪")
            st.caption(f"{status_color} {status}")
        
        # Teams and scores
        st.markdown("---")
        
        team_col1, vs_col, team_col2 = st.columns([2, 1, 2])
        
        with team_col1:
            st.markdown(f"### {visitor_team.get('abbreviation', 'N/A')}")
            st.text(visitor_team.get('name', 'Visitor Team'))
            if status == "Final" or status == "InProgress":
                score = game.get("visitor_team_score", 0)
                st.markdown(f"<h2 style='color: #FF6B6B;'>{score}</h2>", unsafe_allow_html=True)
        
        with vs_col:
            st.markdown("<h3 style='text-align: center;'>vs</h3>", unsafe_allow_html=True)
        
        with team_col2:
            st.markdown(f"### {home_team.get('abbreviation', 'N/A')}")
            st.text(home_team.get('name', 'Home Team'))
            if status == "Final" or status == "InProgress":
                score = game.get("home_team_score", 0)
                st.markdown(f"<h2 style='color: #FF6B6B;'>{score}</h2>", unsafe_allow_html=True)
        
        # Betting odds (if available and requested)
        if show_odds and game.get("betting_odds"):
            st.markdown("---")
            st.markdown("**Betting Odds**")
            display_betting_odds(game["betting_odds"])
        
        st.markdown("</div>", unsafe_allow_html=True)


def display_betting_odds(odds: List[Dict[str, Any]]):
    """
    Display betting odds information.
    
    Args:
        odds: List of betting odds dictionaries
    """
    if not odds:
        st.caption("No betting odds available")
        return
    
    for odd in odds:
        bookmaker = odd.get("bookmaker", "Unknown")
        market_type = odd.get("market_type", "Unknown")
        outcomes = odd.get("outcomes", [])
        
        st.markdown(f"**{bookmaker}** - {market_type}")
        
        if outcomes:
            cols = st.columns(len(outcomes))
            for col, outcome in zip(cols, outcomes):
                with col:
                    name = outcome.get("name", "N/A")
                    price = outcome.get("price", 0)
                    point = outcome.get("point")
                    
                    st.text(name)
                    st.text(f"Price: {price:+.0f}")
                    if point is not None:
                        st.text(f"Point: {point:+.1f}")


def display_live_games_header():
    """Display header for live games section."""
    st.markdown(
        """
        <div style="
            padding: 1rem;
            border-radius: 0.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin-bottom: 2rem;
        ">
            <h2 style="color: white; margin: 0;">🔴 Live & Upcoming Games</h2>
            <p style="color: white; opacity: 0.9; margin: 0.5rem 0 0 0;">
                Real-time scores and betting odds
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_no_games_message():
    """Display message when no games are available."""
    st.info("No live or upcoming games at the moment. Check back later!")


def format_game_time(game_date: str) -> str:
    """
    Format game date/time for display.
    
    Args:
        game_date: ISO format date string
        
    Returns:
        Formatted date string
    """
    try:
        dt = datetime.fromisoformat(game_date.replace("Z", "+00:00"))
        return dt.strftime("%I:%M %p")
    except:
        return game_date

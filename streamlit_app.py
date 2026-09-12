"""
NBA matchup tool - minimal Streamlit app, Phase 1.

HONEST PURPOSE OF THIS FIRST VERSION: this is NOT the full matchup
tool yet - it's a real, direct test to confirm the nba_api connection
actually works once deployed with real internet access (which I don't
have in my own build environment). Once this confirms real, live data
comes back correctly, the next step is building out the full Stage 1/
Stage 2 scanning UI to match what the MLB and NFL tools already do.
"""

import streamlit as st
import pandas as pd
from nba_prop_model_combined import (
    pull_synergy_playtypes, pull_player_usage_and_minutes,
    pull_advanced_rebounding_stats, pull_advanced_passing_stats,
    NBA_PLAY_TYPES, NBA_PROP_PLAYTYPE_MAP, NBA_NON_PLAYTYPE_PROPS,
)

st.set_page_config(page_title="NBA Matchup Tool", layout="wide")
st.title("🏀 NBA Matchup Tool — Phase 1 (connection test)")

st.warning(
    "This is a first, honest test version - it confirms the real, live "
    "data connection works, not the full matchup scanner yet. Once this "
    "pulls real data successfully, the next step is building out full "
    "Stage 1/2 scanning like the MLB and NFL tools already have."
)

season = st.text_input("Season (format: 2025-26)", value="2025-26")

st.header("Step 1 — Test the real, live play-type data connection")
if st.button("Pull real team defensive play-type data"):
    with st.spinner("Pulling real, live data from stats.nba.com..."):
        try:
            team_defense = pull_synergy_playtypes(
                season=season, player_or_team="T", type_grouping="defensive",
            )
            st.success(f"Real connection confirmed - {len(team_defense)} rows pulled.")
            st.dataframe(team_defense.head(20))
        except Exception as e:
            st.error(f"Real connection failed: {e}")

st.header("Step 2 — Test real player usage/minutes data")
if st.button("Pull real player usage data"):
    with st.spinner("Pulling real, live player usage data..."):
        try:
            usage_df = pull_player_usage_and_minutes(season=season)
            st.success(f"Real connection confirmed - {len(usage_df)} players pulled.")
            st.dataframe(usage_df.head(20))
        except Exception as e:
            st.error(f"Real connection failed: {e}")

st.header("Step 3 — Test real, advanced rebounding metrics")
if st.button("Pull real advanced rebounding data"):
    with st.spinner("Pulling real, live rebounding-tracking data..."):
        try:
            reb_df = pull_advanced_rebounding_stats(season=season)
            st.success(f"Real connection confirmed - {len(reb_df)} players pulled.")
            st.dataframe(reb_df.head(20))
        except Exception as e:
            st.error(f"Real connection failed: {e}")

st.header("Step 4 — Test real, advanced passing/assist metrics")
if st.button("Pull real advanced passing data"):
    with st.spinner("Pulling real, live passing-tracking data..."):
        try:
            pass_df = pull_advanced_passing_stats(season=season)
            st.success(f"Real connection confirmed - {len(pass_df)} players pulled.")
            st.dataframe(pass_df.head(20))
        except Exception as e:
            st.error(f"Real connection failed: {e}")

st.header("What's mapped so far")
st.write("Props mapped to real play-type data:", list(NBA_PROP_PLAYTYPE_MAP.keys()))
st.write("Props that need a different, non-play-type stat (honest gap):", list(NBA_NON_PLAYTYPE_PROPS))

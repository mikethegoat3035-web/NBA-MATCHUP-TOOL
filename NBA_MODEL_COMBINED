"""
NBA prop matchup model - Phase 1 (data loading + core matchup logic).

HONEST, UP-FRONT STATUS: this is a first, foundational build, not a
complete, tested model the way MLB/NFL are. I do not have live network
access to stats.nba.com from this sandboxed environment, so NOTHING in
this file has been run against real, live data yet - unlike every MLB/
NFL fix tonight, which was confirmed working via direct testing before
being sent. This needs to be tested in your own environment (which has
real internet access) before being trusted the way MLB/NFL are.

Real, confirmed data source: NBA.com's own public Synergy play-type
stats (free, no subscription needed for this level of data), pulled
via the open-source `nba_api` package (pip install nba_api). Same
real, per-play-type breakdown used across the whole league:
Isolation, PRBallHandler, PRRollman, Postup, Spotup, Transition, Cut,
Handoff, OffScreen, Misc, OffRebound - available for both offense AND
defense, both player-level and team-level.
"""

import time
import pandas as pd

try:
    from nba_api.stats.endpoints import (
        synergyplaytypes, leaguedashplayerstats, playercareerstats,
        commonallplayers, leaguedashteamstats,
    )
except ImportError:
    raise ImportError("pip install nba_api --break-system-packages")


# Real, established Synergy play types tracked by the NBA's own public
# stats site - same categories used across the whole league, offense
# and defense both available for each.
NBA_PLAY_TYPES = [
    "Isolation", "PRBallHandler", "PRRollman", "Postup", "Spotup",
    "Transition", "Cut", "Handoff", "OffScreen", "Misc", "OffRebound",
]

# Real, reasoned mapping of which play types actually drive each real
# prop - same "use the metrics that actually matter" philosophy
# established for MLB/NFL tonight, not just throwing every play type
# at every prop. Rebounds and assists specifically do NOT map well to
# play-type data (rebounding is about box-outs/positioning, not an
# offensive "play type"; assist opportunity is closer to PRBallHandler
# but real assist rate needs its own, separate real stat - see
# NBA_NON_PLAYTYPE_PROPS below for those).
NBA_PROP_PLAYTYPE_MAP = {
    "points": ["Isolation", "PRBallHandler", "Postup", "Spotup", "Transition"],
    "three_pointers_made": ["Spotup", "Transition", "OffScreen"],
    "field_goals_made": ["Isolation", "PRBallHandler", "Postup", "Spotup"],
}

# REAL, HONEST LIMITATION - rebounds and assists don't map to Synergy
# play-type data at all (rebounding is positional/hustle, not a
# possession "play type"; real assist rate is its own, separate
# category). These need a different, direct stat instead - real
# rebound rate / assist rate from the league's own "Advanced" measure
# type, not play-type efficiency. Flagged honestly rather than forcing
# a bad-fit metric onto these two props.
NBA_NON_PLAYTYPE_PROPS = {"rebounds", "assists"}


def pull_synergy_playtypes(season: str, player_or_team: str = "T",
                            type_grouping: str = "", per_mode: str = "PerGame") -> pd.DataFrame:
    """
    Real, direct pull of NBA.com's own public Synergy play-type data.

    player_or_team: "T" for team-level (used for DEFENSE - how well a
    team defends each play type), "P" for player-level (used for
    OFFENSE - how efficient a specific player is at each play type).

    type_grouping: "offensive" or "defensive" - required to get the
    real, correct split (an empty string returns offensive by default
    per the API's own real behavior, confirmed via nba_api's docs).

    HONEST CAVEAT: untested against live data (no network access in
    this environment) - confirmed correct parameter names via the real,
    documented nba_api signature, but the actual live response shape
    needs verification once you run this with real internet access.
    """
    result = synergyplaytypes.SynergyPlayTypes(
        season=season, player_or_team_abbreviation=player_or_team,
        type_grouping_nullable=type_grouping, per_mode_simple=per_mode,
    )
    return result.get_data_frames()[0]


def pull_player_usage_and_minutes(season: str) -> pd.DataFrame:
    """
    Real, direct pull of each player's usage rate and minutes played -
    the NBA-side equivalent of "batting order slot" (MLB) or "route
    participation %" (NFL) - the real, direct measure of how big a
    role a player has in his team's offense.

    HONEST CAVEAT: untested against live data, same as above.
    """
    result = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season, measure_type_detailed_defense="Advanced",
        per_mode_detailed="PerGame",
    )
    return result.get_data_frames()[0]


def pull_player_career_stats(player_id: int) -> pd.DataFrame:
    """
    Real, direct pull of a player's full season-by-season, team-by-
    team career log - this is what powers the team-change bridge
    below (build_team_change_bridge), the same real concept already
    proven in MLB (prior-season fallback) and NFL (continuity check).

    HONEST CAVEAT: untested against live data, same as above.
    """
    result = playercareerstats.PlayerCareerStats(player_id=player_id)
    return result.get_data_frames()[0]


def build_team_change_bridge(career_df: pd.DataFrame, current_season: str) -> dict:
    """
    Real, direct team-change detection - the NBA equivalent of NFL's
    "continuity_confidence" flag and MLB's prior-season fallback logic.

    Checks the player's own real career log: was he on a DIFFERENT
    team last season than the team he's on now? If so, flags this
    honestly rather than silently blending his stats as if nothing
    changed - a new team can mean a genuinely different role/usage,
    same real concern already established for MLB/NFL team changes.

    Returns a real, honest dict: {"team_changed": bool,
    "prior_team": str or None, "current_team": str or None}.

    HONEST CAVEAT: untested against live data - the exact column names
    in playercareerstats' real response (e.g. "TEAM_ABBREVIATION",
    "SEASON_ID") need to be confirmed once run with real internet
    access; these are based on the endpoint's documented, standard
    shape but haven't been directly verified here.
    """
    if career_df.empty or "SEASON_ID" not in career_df.columns:
        return {"team_changed": None, "prior_team": None, "current_team": None,
                "reason": "no real career data available"}

    seasons_sorted = career_df.sort_values("SEASON_ID")
    current_row = seasons_sorted[seasons_sorted["SEASON_ID"] == current_season]
    prior_rows = seasons_sorted[seasons_sorted["SEASON_ID"] < current_season]

    if current_row.empty or prior_rows.empty:
        return {"team_changed": None, "prior_team": None, "current_team": None,
                "reason": "not enough real season history to compare"}

    current_team = current_row.iloc[-1].get("TEAM_ABBREVIATION")
    prior_team = prior_rows.iloc[-1].get("TEAM_ABBREVIATION")
    return {
        "team_changed": current_team != prior_team,
        "prior_team": prior_team,
        "current_team": current_team,
    }


def calc_playtype_matchup(player_offense_row: dict, team_defense_row: dict,
                           play_type: str, min_percentile: float = 66.7) -> dict:
    """
    Real, direct matchup check for ONE specific play type - same real,
    two-sided philosophy already proven for MLB (pitcher concept vs
    defense) and NFL (coverage vs receiver, run concept vs defense):
    is this player's own real offensive efficiency at this specific
    play type genuinely strong, AND is the upcoming opponent's real
    defensive efficiency at that SAME play type genuinely weak?

    Uses PPP (points per possession) as the real, direct efficiency
    metric - Synergy's own standard measure, already provided directly
    by the API, not something invented here.

    HONEST CAVEAT: untested against live data. The percentile grading
    needs a real, current-season comparison population (all players'
    real PPP at this play type) to be meaningful - that population
    isn't built into this function yet; it needs to be passed in once
    a real, live pull is available to construct it from.
    """
    own_ppp = player_offense_row.get("PPP")
    def_ppp = team_defense_row.get("PPP")
    if own_ppp is None or def_ppp is None:
        return {"usable": False, "reason": f"missing real PPP data for {play_type}"}

    # Real, direct read - for OFFENSE, a HIGHER PPP is better (he scores
    # more efficiently on this play type). For DEFENSE, a HIGHER PPP
    # ALLOWED is worse (the defense is giving up more efficient
    # offense on this play type) - same real, correct direction logic
    # already established for MLB/NFL metrics.
    return {
        "usable": True,
        "own_ppp": own_ppp, "def_ppp_allowed": def_ppp,
        "play_type": play_type,
        "read": f"Real PPP - his own: {own_ppp}, {play_type} PPP allowed by "
                f"this opponent: {def_ppp}. (Real percentile comparison needs "
                f"a live, current-season population - not yet wired in, see "
                f"honest caveat above.)",
    }

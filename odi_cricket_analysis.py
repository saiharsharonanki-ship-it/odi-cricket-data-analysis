"""
ODI Cricket Match Analysis (1971–2024)

Run this script from the project root:
    python odi_cricket_analysis.py

Expected data files:
    data/odi_Matches_Data.csv
    data/odi_Batting_Card.csv
    data/odi_Bowling_Card.csv
    data/players_info.csv

The script creates analysis outputs in:
    outputs/
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUTPUT = ROOT / "outputs"
OUTPUT.mkdir(exist_ok=True)


def load_data():
    matches = pd.read_csv(DATA / "odi_Matches_Data.csv", low_memory=False)
    batting = pd.read_csv(DATA / "odi_Batting_Card.csv", low_memory=False)
    bowling = pd.read_csv(DATA / "odi_Bowling_Card.csv", low_memory=False)
    players = pd.read_csv(DATA / "players_info.csv", low_memory=False)
    return matches, batting, bowling, players


def clean_matches(matches):
    matches = matches.copy()
    matches["Match Date"] = pd.to_datetime(matches["Match Date"], errors="coerce")

    for col in ["Team1 Runs Scored", "Team2 Runs Scored"]:
        matches[col] = pd.to_numeric(matches[col], errors="coerce")

    for col in ["Team1 Name", "Team2 Name", "Toss Winner", "Match Winner"]:
        matches[col] = matches[col].astype("string").str.strip()

    matches["Decade"] = (matches["Match Date"].dt.year // 10 * 10).astype("Int64")
    return matches


def decisive_matches(matches):
    result = matches[matches["Match Winner"].notna()].copy()
    return result[~result["Match Winner"].isin(["<NA>", "nan", "NaN"])]


def team_performance(matches):
    rows = []
    for team in pd.unique(
        pd.concat([matches["Team1 Name"], matches["Team2 Name"]]).dropna()
    ):
        played = (
            (matches["Team1 Name"] == team) |
            (matches["Team2 Name"] == team)
        ).sum()
        wins = (matches["Match Winner"] == team).sum()
        rows.append({
            "Team": team,
            "Matches": int(played),
            "Wins": int(wins),
            "Win Rate": wins / played if played else np.nan
        })
    return pd.DataFrame(rows).sort_values(
        ["Wins", "Win Rate"], ascending=False
    )


def toss_analysis(matches):
    valid = matches[
        matches["Toss Winner"].notna() &
        matches["Toss Winner Choice"].isin(["bat", "bowl"])
    ].copy()

    valid["Toss Outcome"] = np.where(
        valid["Toss Winner"].eq(valid["Match Winner"]),
        "Toss winner won match",
        "Toss winner lost match"
    )

    # Identify the team that batted first from the toss decision.
    valid["First Innings Team"] = np.where(
        valid["Toss Winner Choice"].eq("bat"),
        valid["Toss Winner"],
        np.where(
            valid["Toss Winner"].eq(valid["Team1 Name"]),
            valid["Team2 Name"],
            valid["Team1 Name"]
        )
    )

    valid["First Innings Outcome"] = np.where(
        valid["First Innings Team"].eq(valid["Match Winner"]),
        "First innings team won",
        "First innings team lost"
    )

    return valid


def player_performance(batting, bowling, players):
    players_map = (
        players.drop_duplicates("player_id")
        .set_index("player_id")["player_name"]
    )

    batting = batting.copy()
    batting["batsman"] = pd.to_numeric(batting["batsman"], errors="coerce")
    batting["runs"] = pd.to_numeric(batting["runs"], errors="coerce")
    runs = (
        batting.groupby("batsman")["runs"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    top_batters = pd.DataFrame({
        "Player": [players_map.get(pid, f"Player {int(pid)}") for pid in runs.index],
        "Runs": runs.values
    })

    bowling = bowling.copy()
    bowling["bowler id"] = pd.to_numeric(
        bowling["bowler id"], errors="coerce"
    )
    bowling["wickets"] = pd.to_numeric(
        bowling["wickets"], errors="coerce"
    )
    wickets = (
        bowling.groupby("bowler id")["wickets"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    top_bowlers = pd.DataFrame({
        "Player": [players_map.get(pid, f"Player {int(pid)}") for pid in wickets.index],
        "Wickets": wickets.values
    })

    return top_batters, top_bowlers


def make_charts(matches, teams, toss, top_batters):
    # 1. Matches by decade
    counts = matches["Decade"].value_counts().sort_index()
    plt.figure(figsize=(9, 5))
    plt.bar(counts.index.astype(str), counts.values)
    plt.title("ODI Matches by Decade")
    plt.xlabel("Decade")
    plt.ylabel("Matches")
    plt.tight_layout()
    plt.savefig(OUTPUT / "matches_by_decade.png", dpi=180)
    plt.close()

    # 2. Toss outcome
    counts = toss["Toss Outcome"].value_counts()
    plt.figure(figsize=(7, 5))
    plt.bar(counts.index, counts.values)
    plt.title("Match Outcomes for Toss Winners")
    plt.ylabel("Matches")
    plt.xticks(rotation=10)
    plt.tight_layout()
    plt.savefig(OUTPUT / "toss_outcome.png", dpi=180)
    plt.close()

    # 3. Batting first outcome
    counts = toss["First Innings Outcome"].value_counts()
    plt.figure(figsize=(7, 5))
    plt.bar(counts.index, counts.values)
    plt.title("Outcome of Batting First")
    plt.ylabel("Matches")
    plt.xticks(rotation=10)
    plt.tight_layout()
    plt.savefig(OUTPUT / "bat_first_outcome.png", dpi=180)
    plt.close()

    # 4. Top teams
    top = teams.head(10).sort_values("Wins")
    plt.figure(figsize=(9, 5))
    plt.barh(top["Team"], top["Wins"])
    plt.title("Top 10 ODI Teams by Wins")
    plt.xlabel("Wins")
    plt.tight_layout()
    plt.savefig(OUTPUT / "top_teams_wins.png", dpi=180)
    plt.close()

    # 5. Top batters
    top = top_batters.sort_values("Runs")
    plt.figure(figsize=(9, 5))
    plt.barh(top["Player"], top["Runs"])
    plt.title("Top 10 ODI Run Scorers")
    plt.xlabel("Runs")
    plt.tight_layout()
    plt.savefig(OUTPUT / "top_batters.png", dpi=180)
    plt.close()

    # 6. Average combined runs by decade
    scored = matches.dropna(
        subset=["Team1 Runs Scored", "Team2 Runs Scored"]
    ).copy()
    scored["Total Runs"] = (
        scored["Team1 Runs Scored"] + scored["Team2 Runs Scored"]
    )
    avg_runs = scored.groupby("Decade")["Total Runs"].mean()

    plt.figure(figsize=(9, 5))
    plt.plot(avg_runs.index.astype(str), avg_runs.values, marker="o")
    plt.title("Average Combined Match Runs by Decade")
    plt.xlabel("Decade")
    plt.ylabel("Average combined runs")
    plt.tight_layout()
    plt.savefig(OUTPUT / "avg_runs_by_decade.png", dpi=180)
    plt.close()


def main():
    matches, batting, bowling, players = load_data()
    matches = clean_matches(matches)

    decided = decisive_matches(matches)
    teams = team_performance(decided)
    toss = toss_analysis(decided)
    top_batters, top_bowlers = player_performance(
        batting, bowling, players
    )

    make_charts(matches, teams, toss, top_batters)

    print("\nODI Cricket Analysis")
    print("--------------------")
    print(f"Matches: {len(matches):,}")
    print(f"Date range: {matches['Match Date'].min().date()} to "
          f"{matches['Match Date'].max().date()}")
    print(f"Decisive matches: {len(decided):,}")

    toss_win_rate = (
        toss["Toss Outcome"].eq("Toss winner won match").mean()
    )
    bat_first_rate = (
        toss["First Innings Outcome"].eq("First innings team won").mean()
    )

    print(f"Toss winner match-win rate: {toss_win_rate:.2%}")
    print(f"Batting-first win rate: {bat_first_rate:.2%}")

    print("\nTop teams by wins:")
    print(teams.head(10).to_string(index=False))

    print("\nTop batters:")
    print(top_batters.to_string(index=False))

    print("\nTop bowlers:")
    print(top_bowlers.to_string(index=False))

    print(f"\nCharts saved to: {OUTPUT.resolve()}")


if __name__ == "__main__":
    main()

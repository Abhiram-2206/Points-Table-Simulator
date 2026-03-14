import streamlit as st
import pandas as pd

st.title("🏏 Cricket Points Table Simulator")

# ---------------- SESSION STATE ----------------

if "teams" not in st.session_state:
    st.session_state.teams = {}

# ---------------- FUNCTIONS ----------------

def overs_to_balls(overs):
    whole = int(overs)
    balls = int(round((overs - whole) * 10))
    return whole * 6 + balls


def balls_for_nrr(overs, wickets):

    # ICC rule: if team all out, count full 20 overs
    if wickets == 10:
        return 120

    return overs_to_balls(overs)


class Team:

    def __init__(self, name):

        self.name = name
        self.matches = 0
        self.wins = 0
        self.losses = 0
        self.points = 0

        self.runs_scored = 0
        self.runs_conceded = 0

        self.balls_faced = 0
        self.balls_bowled = 0

    def nrr(self):

        if self.balls_faced == 0 or self.balls_bowled == 0:
            return 0

        run_rate_scored = (self.runs_scored / self.balls_faced) * 6
        run_rate_conceded = (self.runs_conceded / self.balls_bowled) * 6

        return run_rate_scored - run_rate_conceded


# ---------------- ADD TEAM ----------------

st.header("Add Team")

team_name = st.text_input("Team Name")

if st.button("Add Team"):

    if team_name.strip() == "":
        st.warning("Enter a valid team name")

    elif team_name in st.session_state.teams:
        st.warning("Team already exists")

    else:
        st.session_state.teams[team_name] = Team(team_name)
        st.success(f"{team_name} added")


# ---------------- MATCH INPUT ----------------

st.header("Add Match Result")

team_list = list(st.session_state.teams.keys())

if len(team_list) < 2:

    st.info("Add at least 2 teams")

else:

    home = st.selectbox("Home Team", team_list)
    away = st.selectbox("Away Team", team_list)

    st.subheader("Home Innings")

    home_runs = st.number_input("Runs (Home)", min_value=0)
    home_wickets = st.number_input("Wickets Lost (Home)", min_value=0, max_value=10)
    home_overs = st.number_input("Overs Faced (Home)", min_value=0.0)

    st.subheader("Away Innings")

    away_runs = st.number_input("Runs (Away)", min_value=0)
    away_wickets = st.number_input("Wickets Lost (Away)", min_value=0, max_value=10)
    away_overs = st.number_input("Overs Faced (Away)", min_value=0.0)

    if st.button("Submit Match"):

        if home == away:
            st.error("Teams must be different")

        else:

            home_team = st.session_state.teams[home]
            away_team = st.session_state.teams[away]

            home_team.matches += 1
            away_team.matches += 1

            # Runs update
            home_team.runs_scored += home_runs
            home_team.runs_conceded += away_runs

            away_team.runs_scored += away_runs
            away_team.runs_conceded += home_runs

            # Balls update (ICC rule applied)
            home_team.balls_faced += balls_for_nrr(home_overs, home_wickets)
            away_team.balls_faced += balls_for_nrr(away_overs, away_wickets)

            home_team.balls_bowled += balls_for_nrr(away_overs, away_wickets)
            away_team.balls_bowled += balls_for_nrr(home_overs, home_wickets)

            # Result
            if home_runs > away_runs:

                home_team.wins += 1
                home_team.points += 2
                away_team.losses += 1

            elif away_runs > home_runs:

                away_team.wins += 1
                away_team.points += 2
                home_team.losses += 1

            st.success("Match Added")


# ---------------- POINTS TABLE ----------------

st.header("Points Table")

if st.button("Generate Table"):

    data = []

    for team in st.session_state.teams.values():

        data.append({
            "Team": team.name,
            "Matches": team.matches,
            "Wins": team.wins,
            "Losses": team.losses,
            "Points": team.points,
            "NRR": round(team.nrr(), 3)
        })

    df = pd.DataFrame(data)

    if df.empty:
        st.warning("No matches added yet")

    else:

        df = df.sort_values(by=["Points", "NRR"], ascending=False).reset_index(drop=True)

        df.index = df.index + 1
        df.index.name = "Rank"

        st.dataframe(df, use_container_width=True)

        df.to_csv("points_table.csv")

        st.success("Points table exported")
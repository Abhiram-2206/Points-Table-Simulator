import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Cricket Points Table Simulator",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── SESSION STATE ────────────────────────────────────────────────────────────

if "teams" not in st.session_state:
    st.session_state.teams = {}

if "matches" not in st.session_state:
    st.session_state.matches = []

# ─── UTILITIES ────────────────────────────────────────────────────────────────

def overs_to_balls(overs: float) -> int:
    whole = int(overs)
    balls = int(round((overs - whole) * 10))
    return whole * 6 + balls


def balls_for_nrr(overs: float, wickets: int, max_overs: float = 20.0) -> int:
    if wickets == 10:
        return overs_to_balls(max_overs)
    return overs_to_balls(overs)


def valid_overs(overs: float) -> bool:
    ball_digit = round((overs - int(overs)) * 10)
    return 0 <= ball_digit <= 5


def overs_errors(*labeled_overs) -> list:
    errors = []
    for label, o in labeled_overs:
        if not valid_overs(o):
            errors.append(
                f"{label} overs ({o:.1f}) is invalid — "
                f"ball digit must be .0 to .5 (1 over = 6 balls). "
                f"Did you mean {int(o)}.{min(round((o - int(o)) * 10), 5)}?"
            )
    return errors



def match_result_str(bat1: str, bat1_r: int,
                     bat2: str, bat2_r: int, bat2_w: int) -> tuple:
    """
    Returns (winner, result_string) using cricket convention:
      - Batting-1st team wins  → 'won by X runs'
      - Batting-2nd team wins  → 'won by Y wickets'  (wickets remaining = 10 - bat2_w)
      - Tie                    → 'Tie'
    """
    if bat1_r > bat2_r:
        return bat1, f"{bat1} beat {bat2} by {bat1_r - bat2_r} runs"
    elif bat2_r > bat1_r:
        wkts_remaining = 10 - bat2_w
        return bat2, f"{bat2} beat {bat1} by {wkts_remaining} wicket{'s' if wkts_remaining != 1 else ''}"
    else:
        return "Tie", "Match tied — 1 pt each"

# ─── TEAM CLASS ───────────────────────────────────────────────────────────────

class Team:
    def __init__(self, name: str):
        self.name          = name
        self.matches       = 0
        self.wins          = 0
        self.losses        = 0
        self.no_results    = 0
        self.super_overs   = 0
        self.points        = 0
        self.runs_scored   = 0
        self.runs_conceded = 0
        self.balls_faced   = 0
        self.balls_bowled  = 0

    def nrr(self) -> float:
        if self.balls_faced == 0 or self.balls_bowled == 0:
            return 0.0
        return (self.runs_scored / self.balls_faced * 6) - (self.runs_conceded / self.balls_bowled * 6)


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("🏏 Simulator")
    st.caption("ICC · BCCI Rules")
    st.divider()

    page = st.radio(
        "Go to",
        ["🏟️  Manage Teams", "⚡  Add Match", "📊  Points Table", "📋  Match Log", "📖  Rules"],
        label_visibility="collapsed",
    )

    if st.session_state.teams:
        st.divider()
        st.caption("TOURNAMENT STATS")
        c1, c2 = st.columns(2)
        c1.metric("Teams",   len(st.session_state.teams))
        c2.metric("Matches", len(st.session_state.matches))

# ─── PAGE HEADER ──────────────────────────────────────────────────────────────

st.title("🏏 Cricket Points Table Simulator")
st.caption("ICC & BCCI rules · NRR · D/L Method · Super Over · No Result")
st.divider()

# ════════════════════════════════════════════════════════════════════════════════
# PAGE: MANAGE TEAMS
# ════════════════════════════════════════════════════════════════════════════════

if page == "🏟️  Manage Teams":

    st.subheader("Register a Team")

    c1, c2 = st.columns([4, 1])
    with c1:
        team_name = st.text_input("Team name", placeholder="e.g. Mumbai Indians",
                                  label_visibility="collapsed")
    with c2:
        add_btn = st.button("＋ Add Team", use_container_width=True)

    if add_btn:
        if not team_name.strip():
            st.error("Enter a valid team name.")
        elif team_name in st.session_state.teams:
            st.warning(f"'{team_name}' already exists.")
        else:
            st.session_state.teams[team_name] = Team(team_name)
            st.success(f"✅ {team_name} added to the tournament!")
            st.rerun()

    st.divider()

    if not st.session_state.teams:
        st.info("No teams yet. Add at least 2 teams to start the tournament.")
    else:
        teams = list(st.session_state.teams.values())

        st.subheader("Registered Teams")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Teams",   len(teams))
        col2.metric("Matches Played", sum(t.matches for t in teams) // 2)
        col3.metric("Total Points",   sum(t.points for t in teams))

        st.divider()

        for t in teams:
            with st.container(border=True):
                tc1, tc2, tc3, tc4, tc5 = st.columns([3, 1, 1, 1, 1])
                tc1.write(f"**{t.name}**")
                tc2.metric("M",   t.matches)
                tc3.metric("W",   t.wins)
                tc4.metric("L",   t.losses)
                tc5.metric("Pts", t.points)


# ════════════════════════════════════════════════════════════════════════════════
# PAGE: ADD MATCH
# ════════════════════════════════════════════════════════════════════════════════

elif page == "⚡  Add Match":

    team_list = list(st.session_state.teams.keys())

    if len(team_list) < 2:
        st.warning("Add at least 2 teams first — go to **Manage Teams**.")
        st.stop()

    st.subheader("Select Teams")
    c1, mid, c2 = st.columns([5, 1, 5])
    with c1:
        home = st.selectbox("🏏 Batting 1st", team_list, key="sel_home")
    with mid:
        st.write("")
        st.write("")
        st.write("**vs**")
    with c2:
        away_opts = [t for t in team_list if t != home]
        away = st.selectbox("🎯 Batting 2nd", away_opts, key="sel_away")

    st.divider()

    st.subheader("Match Type")
    match_type = st.radio(
        "Match Type",
        ["🏏 Normal Match", "⚡ Super Over", "🌧️ Rain / D-L Method", "🚫 Washed Out (No Result)"],
        horizontal=True,
        label_visibility="collapsed",
    )

    st.divider()

    # ── Innings input helper ──────────────────────────────────────────────────
    def innings_block(label: str, suffix: str, show_allot: bool = False):
        st.subheader(f"🏏 {label} Innings")
        r = st.number_input("Runs",    min_value=0,   step=1,   key=f"r_{suffix}")
        w = st.number_input("Wickets", min_value=0,   max_value=10, step=1, key=f"w_{suffix}")
        o = st.number_input("Overs",   min_value=0.0, step=0.1, key=f"o_{suffix}", format="%.1f")
        if not valid_overs(o):
            st.error(f"⚠️ Invalid overs {o:.1f} — ball digit must be .0 to .5")
        a = None
        if show_allot:
            a = st.number_input("Allotted Overs (D/L)", min_value=1.0, value=20.0,
                                step=0.1, format="%.1f", key=f"a_{suffix}",
                                help="Revised overs allotted under the D/L method")
            if not valid_overs(a):
                st.error(f"⚠️ Invalid allotted overs {a:.1f} — ball digit must be .0 to .5")
        return (r, w, o, a) if show_allot else (r, w, o)

    # ══ NORMAL MATCH ══════════════════════════════════════════════════════════
    if match_type == "🏏 Normal Match":
        c1, c2 = st.columns(2)
        with c1:
            home_r, home_w, home_o = innings_block(home, "home")
        with c2:
            away_r, away_w, away_o = innings_block(away, "away")

        st.divider()
        if st.button("✅ Submit Normal Match", use_container_width=True):
            errs = overs_errors((home, home_o), (away, away_o))
            for e in errs:
                st.error(e)
            if not errs:
                ht = st.session_state.teams[home]
                at = st.session_state.teams[away]
                ht.matches += 1;  at.matches += 1
                ht.runs_scored   += home_r;  ht.runs_conceded += away_r
                at.runs_scored   += away_r;  at.runs_conceded += home_r
                ht.balls_faced   += balls_for_nrr(home_o, home_w)
                at.balls_faced   += balls_for_nrr(away_o, away_w)
                ht.balls_bowled  += balls_for_nrr(away_o, away_w)
                at.balls_bowled  += balls_for_nrr(home_o, home_w)
                winner, result_str = match_result_str(home, home_r, away, away_r, away_w)
                if winner == home:
                    ht.wins += 1;  ht.points += 2;  at.losses += 1
                elif winner == away:
                    at.wins += 1;  at.points += 2;  ht.losses += 1
                else:
                    ht.points += 1;  at.points += 1
                st.session_state.matches.append(
                    dict(bat1=home, bat2=away, bat1_r=home_r, bat2_r=away_r,
                         bat2_w=away_w, ho=home_o, ao=away_o,
                         winner=winner, result_str=result_str, type="normal"))
                st.success(f"🏏 {result_str}")

    # ══ SUPER OVER ════════════════════════════════════════════════════════════
    elif match_type == "⚡ Super Over":
        st.info(
            "Main innings must end in a tie. "
            "Super Over winner gets 2 pts. "
            "Super Over runs are excluded from NRR (ICC rule)."
        )
        c1, c2 = st.columns(2)
        with c1:
            home_r, home_w, home_o = innings_block(home, "so_home")
        with c2:
            away_r, away_w, away_o = innings_block(away, "so_away")

        st.divider()
        st.subheader("Super Over Winner")
        so_winner = st.radio("Who won the Super Over?", [home, away],
                             horizontal=True, key="so_winner",
                             label_visibility="collapsed")

        if st.button("⚡ Submit Super Over Match", use_container_width=True):
            errs = overs_errors((home, home_o), (away, away_o))
            for e in errs:
                st.error(e)
            if errs:
                pass
            elif home_r != away_r:
                st.error(f"Scores must be tied for a Super Over. "
                         f"({home}: {home_r}, {away}: {away_r})")
            else:
                ht = st.session_state.teams[home]
                at = st.session_state.teams[away]
                ht.matches += 1;  at.matches += 1
                ht.runs_scored   += home_r;  ht.runs_conceded += away_r
                at.runs_scored   += away_r;  at.runs_conceded += home_r
                ht.balls_faced   += balls_for_nrr(home_o, home_w)
                at.balls_faced   += balls_for_nrr(away_o, away_w)
                ht.balls_bowled  += balls_for_nrr(away_o, away_w)
                at.balls_bowled  += balls_for_nrr(home_o, home_w)
                loser = away if so_winner == home else home
                st.session_state.teams[so_winner].wins        += 1
                st.session_state.teams[so_winner].points      += 2
                st.session_state.teams[so_winner].super_overs += 1
                st.session_state.teams[loser].losses          += 1
                result_str = f"{so_winner} beat {loser} via Super Over"
                st.session_state.matches.append(
                    dict(bat1=home, bat2=away, bat1_r=home_r, bat2_r=away_r,
                         bat2_w=away_w, ho=home_o, ao=away_o,
                         winner=so_winner, result_str=result_str, type="so"))
                st.success(f"⚡ {result_str} (2 pts)")

    # ══ D/L METHOD ════════════════════════════════════════════════════════════
    elif match_type == "🌧️ Rain / D-L Method":
        st.info(
            "Enter actual runs/overs and allotted overs per team. "
            "The D/L revised target decides the winner. "
            "NRR uses allotted overs as the denominator (ICC rule)."
        )
        c1, c2 = st.columns(2)
        with c1:
            home_r, home_w, home_o, home_a = innings_block(home, "dl_home", show_allot=True)
        with c2:
            away_r, away_w, away_o, away_a = innings_block(away, "dl_away", show_allot=True)

        st.divider()
        st.subheader("D/L Target & Chasing Team")
        dc1, dc2 = st.columns(2)
        with dc1:
            dl_par = st.number_input("D/L Revised Target (runs needed to win)",
                                     min_value=0, step=1, key="dl_par")
        with dc2:
            dl_chaser = st.radio("Which team is chasing?", [home, away],
                                 horizontal=True, key="dl_chaser",
                                 label_visibility="collapsed")

        if st.button("🌧️ Submit D/L Match", use_container_width=True):
            errs = overs_errors(
                (home, home_o), (away, away_o),
                (f"{home} allotted", home_a), (f"{away} allotted", away_a)
            )
            for e in errs:
                st.error(e)
            if not errs:
                ht = st.session_state.teams[home]
                at = st.session_state.teams[away]
                ht.matches += 1;  at.matches += 1
                ht.runs_scored   += home_r;  ht.runs_conceded += away_r
                at.runs_scored   += away_r;  at.runs_conceded += home_r
                ht.balls_faced   += balls_for_nrr(home_o, home_w, home_a)
                at.balls_faced   += balls_for_nrr(away_o, away_w, away_a)
                ht.balls_bowled  += balls_for_nrr(away_o, away_w, away_a)
                at.balls_bowled  += balls_for_nrr(home_o, home_w, home_a)
                chaser_runs = away_r if dl_chaser == away else home_r
                winner = dl_chaser if chaser_runs >= dl_par else (home if dl_chaser == away else away)
                loser  = away if winner == home else home
                st.session_state.teams[winner].wins   += 1
                st.session_state.teams[winner].points += 2
                st.session_state.teams[loser].losses  += 1
                setter  = home if dl_chaser == away else away
                if winner == setter:
                    # chasing team fell short → batting-1st side won by runs
                    dl_result_str = f"{winner} beat {loser} by {dl_par - chaser_runs - 1} runs (D/L)"
                else:
                    # chasing team reached or beat target → won by wickets
                    chaser_w = away_w if dl_chaser == away else home_w
                    wkts_rem = 10 - chaser_w
                    dl_result_str = (f"{winner} beat {loser} by {wkts_rem} "
                                     f"wicket{'s' if wkts_rem != 1 else ''} (D/L)")
                st.session_state.matches.append(
                    dict(bat1=home, bat2=away, bat1_r=home_r, bat2_r=away_r,
                         bat2_w=away_w, winner=winner,
                         result_str=dl_result_str, type="dl", par=dl_par))
                st.success(f"🌧️ {dl_result_str} (2 pts)")

    # ══ WASHED OUT ════════════════════════════════════════════════════════════
    elif match_type == "🚫 Washed Out (No Result)":
        st.info(
            "Match abandoned without a result. "
            "Each team receives 1 point. "
            "NRR is completely unaffected — no runs or balls are recorded."
        )
        if st.button("🚫 Submit Washed Out Match", use_container_width=True):
            ht = st.session_state.teams[home]
            at = st.session_state.teams[away]
            ht.matches    += 1;  at.matches    += 1
            ht.no_results += 1;  at.no_results += 1
            ht.points     += 1;  at.points     += 1
            st.session_state.matches.append(
                dict(bat1=home, bat2=away, winner="No Result",
                     result_str="Match abandoned — No Result", type="nr"))
            st.success(f"🌧️ Washed out — {home} & {away} each get 1 pt. NRR unaffected.")


# ════════════════════════════════════════════════════════════════════════════════
# PAGE: POINTS TABLE
# ════════════════════════════════════════════════════════════════════════════════

elif page == "📊  Points Table":

    if not st.session_state.teams:
        st.info("No teams added yet. Go to **Manage Teams** to get started.")
        st.stop()

    st.subheader("📊 Live Standings")

    rows = sorted(
        [{"team": t, "nrr": t.nrr()} for t in st.session_state.teams.values()],
        key=lambda x: (-x["team"].points, -x["nrr"])
    )

    table_data = []
    for i, r in enumerate(rows):
        t   = r["team"]
        nrr = r["nrr"]
        nrr_str = f"+{nrr:.3f}" if nrr >= 0 else f"{nrr:.3f}"
        so_note = f" (SO×{t.super_overs})" if t.super_overs else ""
        table_data.append({
            "Rank":    i + 1,
            "Team":    t.name + so_note,
            "M":       t.matches,
            "W":       t.wins,
            "L":       t.losses,
            "NR":      t.no_results,
            "Pts":     t.points,
            "NRR":     nrr_str,
        })

    df_display = pd.DataFrame(table_data)
    st.dataframe(df_display, use_container_width=True, hide_index=True)

    st.caption(
        "NRR = (Runs Scored / Balls Faced × 6) − (Runs Conceded / Balls Bowled × 6)  ·  "
        "NR = No Result  ·  SO = Super Over wins  ·  Sorted by Pts then NRR"
    )

    st.divider()

    # CSV download
    csv_data = []
    for i, r in enumerate(rows):
        t = r["team"]
        csv_data.append({
            "Rank": i + 1, "Team": t.name, "M": t.matches,
            "W": t.wins, "L": t.losses, "NR": t.no_results,
            "Pts": t.points, "NRR": round(r["nrr"], 3), "SO Wins": t.super_overs,
        })
    csv_bytes = pd.DataFrame(csv_data).to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Export to CSV",
        data=csv_bytes,
        file_name="points_table.csv",
        mime="text/csv",
    )


# ════════════════════════════════════════════════════════════════════════════════
# PAGE: MATCH LOG
# ════════════════════════════════════════════════════════════════════════════════

elif page == "📋  Match Log":

    if not st.session_state.matches:
        st.info("No matches logged yet. Head to **Add Match** to start logging results.")
        st.stop()

    st.subheader(f"📋 Match Log  —  {len(st.session_state.matches)} matches")
    st.caption("Most recent first")
    st.divider()

    type_emoji = {"normal": "🏏", "so": "⚡", "dl": "🌧️", "nr": "🚫"}
    type_label = {"normal": "Normal", "so": "Super Over", "dl": "D/L", "nr": "No Result"}

    for m in reversed(st.session_state.matches):
        with st.container(border=True):
            col_teams, col_tag = st.columns([5, 1])

            # Support both old (home/away) and new (bat1/bat2) key names
            bat1 = m.get("bat1", m.get("home", "?"))
            bat2 = m.get("bat2", m.get("away", "?"))
            bat1_r = m.get("bat1_r", m.get("hr"))
            bat2_r = m.get("bat2_r", m.get("ar"))

            with col_teams:
                st.write(f"**{bat1}** (bat 1st)  vs  **{bat2}** (bat 2nd)")

                if m["type"] != "nr" and bat1_r is not None:
                    score = f"{bat1}: {bat1_r}  ·  {bat2}: {bat2_r}"
                    if m.get("par") is not None:
                        score += f"  ·  D/L target: {m['par']}"
                    st.caption(score)

                result_str = m.get("result_str", "")
                if m["winner"] == "Tie":
                    st.caption("🤝 Match tied — 1 pt each")
                elif m["winner"] == "No Result":
                    st.caption("🚫 No result — 1 pt each")
                else:
                    st.caption(f"✅ {result_str}")

            with col_tag:
                emoji = type_emoji.get(m["type"], "🏏")
                label = type_label.get(m["type"], m["type"])
                st.write(f"**{emoji} {label}**")


# ════════════════════════════════════════════════════════════════════════════════
# PAGE: RULES
# ════════════════════════════════════════════════════════════════════════════════

elif page == "📖  Rules":

    st.subheader("📖 Scoring Rules Reference")
    st.divider()

    rules = [
        ("🏏 Normal Win / Loss",
         "W: 2 pts · L: 0 pts",
         "✅ Full innings counted in NRR",
         "One team outscores the other. Full runs and balls from both innings count toward NRR."),
        ("🤝 Tie (no Super Over)",
         "1 pt each",
         "✅ Full innings counted in NRR",
         "Both teams finish on equal runs with no Super Over. Each side takes 1 point."),
        ("⚡ Super Over",
         "W: 2 pts · L: 0 pts",
         "✅ Main innings only — Super Over excluded",
         "A tied main innings triggers a 1-over eliminator. Winner gets 2 pts. "
         "Super Over runs and balls are NOT counted in NRR (ICC regulation)."),
        ("🌧️ Rain / D-L Method",
         "W: 2 pts · L: 0 pts",
         "✅ Allotted overs used for NRR",
         "The D/L revised target determines the winner. For NRR, each team's allotted "
         "(revised) overs are used as the denominator — not the actual overs faced."),
        ("🚫 Washed Out / No Result",
         "1 pt each",
         "❌ NRR completely unaffected",
         "Match abandoned before a conclusive result. Each team gets 1 point. "
         "No runs or balls are recorded toward NRR."),
    ]

    for title, pts, nrr_note, desc in rules:
        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 2, 2])
            c1.write(f"**{title}**")
            c2.caption(pts)
            c3.caption(nrr_note)
            st.caption(desc)

    st.divider()
    st.subheader("NRR Formula")

    with st.container(border=True):
        st.code(
            "NRR = (Runs Scored / Balls Faced × 6) − (Runs Conceded / Balls Bowled × 6)",
            language="text"
        )
        st.write("**All-out rule:** If a team loses all 10 wickets, the full allotted overs are "
                 "used in the denominator — not the actual overs faced.")
        st.write("**D/L rule:** In rain-affected matches, each team's allotted (revised) overs "
                 "are used for both batting and bowling denominators, regardless of actual play.")

    st.divider()
    st.subheader("Points Summary")

    summary_df = pd.DataFrame({
        "Scenario":     ["Normal Win", "Normal Loss", "Tie", "Super Over Win",
                         "Super Over Loss", "D/L Win", "D/L Loss", "Washed Out"],
        "Points":       [2, 0, 1, 2, 0, 2, 0, 1],
        "NRR Affected": ["Yes", "Yes", "Yes", "Yes (main innings only)",
                         "Yes (main innings only)", "Yes", "Yes", "No"],
    })
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
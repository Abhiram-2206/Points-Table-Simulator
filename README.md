# 🏏 Cricket Points Table Simulator

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green)
![Rules](https://img.shields.io/badge/Rules-ICC%20%26%20BCCI-orange)
![Status](https://img.shields.io/badge/Project-Completed-brightgreen)

---

## 📌 Project Overview

A fully interactive **Cricket Points Table Simulator** built with Python, Streamlit, and Pandas.

It simulates real tournament standings by tracking:

- Matches Played, Wins, Losses, No Results
- Points (with ICC & BCCI scoring rules)
- Net Run Rate (NRR) — accurately calculated using balls, not just overs
- Match results displayed in proper cricket language (*"won by X runs"* or *"won by Y wickets"*)

Supports all four real-world match scenarios: Normal, Super Over, Rain/D-L Method, and Washed Out.

---

## 🚀 Features

- ✅ **Object-Oriented Design** — `Team` class with per-team stats
- ✅ **Accurate NRR Calculation** — overs converted to balls internally; all-out rule applied
- ✅ **ICC / BCCI Match Types** — Normal, Super Over, D/L Method, Washed Out (No Result)
- ✅ **D/L Method Support** — allotted overs used as NRR denominator per ICC rules
- ✅ **Super Over Handling** — Super Over runs excluded from NRR; main innings only
- ✅ **Overs Validation** — rejects invalid overs like `18.8` (ball digit must be .0–.5)
- ✅ **Cricket Result Language** — *"Team A beat Team B by 36 runs"* or *"by 7 wickets"*
- ✅ **Live Points Table** — sorted by Points then NRR, with Super Over win indicators
- ✅ **Match Log** — full history with batting 1st/2nd, scores, and result strings
- ✅ **CSV Export** — downloads directly to the user's device via browser
- ✅ **Multi-page Streamlit UI** — sidebar navigation across 5 pages
- ✅ **No HTML / CSS / JS** — 100% native Streamlit components

---

## 🧠 Net Run Rate Formula

```
NRR = (Total Runs Scored / Total Balls Faced × 6)
    − (Total Runs Conceded / Total Balls Bowled × 6)
```

**Special rules applied:**

| Rule | Detail |
|---|---|
| All-out | If a team loses all 10 wickets, full allotted overs used in denominator |
| D/L Method | Each team's allotted (revised) overs used — not actual overs faced |
| Super Over | Only main innings runs/balls count toward NRR |
| Washed Out | No runs or balls recorded — NRR completely unaffected |

---

## 🏗️ Project Structure

```
app.py
│
├── Utilities
│   ├── overs_to_balls()       — converts 18.3 → 111 balls
│   ├── balls_for_nrr()        — applies all-out & D/L rules
│   ├── valid_overs()          — validates ball digit is .0–.5
│   ├── overs_errors()         — returns error messages for invalid overs
│   └── match_result_str()     — generates "won by X runs / Y wickets"
│
├── Team class
│   └── nrr()                  — calculates live NRR
│
└── Pages (Streamlit sidebar navigation)
    ├── 🏟️  Manage Teams       — register teams, view per-team stats
    ├── ⚡  Add Match           — log match with type-specific inputs
    ├── 📊  Points Table        — live sorted standings + CSV export
    ├── 📋  Match Log           — full match history with result strings
    └── 📖  Rules               — scoring reference + NRR formula + points table
```

---

## 📋 Match Types

| Type | Points | NRR Impact | Rule |
|---|---|---|---|
| 🏏 Normal Win / Loss | W: 2 · L: 0 | Full innings counted | Standard result |
| 🤝 Tie (no Super Over) | 1 each | Full innings counted | Equal scores, no eliminator |
| ⚡ Super Over | W: 2 · L: 0 | Main innings only | Super Over runs excluded from NRR |
| 🌧️ Rain / D-L Method | W: 2 · L: 0 | Allotted overs used | D/L target decides winner |
| 🚫 Washed Out | 1 each | Unaffected | No runs/balls recorded |

---

## ▶️ How to Run

### Install dependencies

```bash
pip install streamlit pandas
```

### Run the app

```bash
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`.

---

## 📊 Output

- **Live Points Table** — Rank, Team, M, W, L, NR, Pts, NRR (sortable)
- **Match Log** — Each match with batting order, scores, and result description
- **CSV Export** — Click *Export to CSV* on the Points Table page to download to your device

---

## 📦 Requirements

```
Python 3.x
streamlit
pandas
```

---

## 👨‍💻 Author

Developed as part of a Cricket Analytics & NRR Simulation project.

---

⭐ *Star this repo if you found it useful — contributions and enhancements welcome!*

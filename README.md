# 🏏 Cricket Points Table & Net Run Rate (NRR) Simulator

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green)
![Status](https://img.shields.io/badge/Project-Completed-brightgreen)

------------------------------------------------------------------------

## 📌 Project Overview

This project is a **Cricket Points Table Simulator** built using Python
and Pandas.\
It calculates and maintains:

-   Matches Played
-   Wins
-   Losses
-   Points
-   Net Run Rate (NRR)

The system supports multiple teams and multiple matches, automatically
generating a properly sorted points table similar to professional
cricket tournaments.

------------------------------------------------------------------------

## 🚀 Features

-   ✅ Object-Oriented Programming (OOP) Design\
-   ✅ Accurate Net Run Rate (NRR) Calculation\
-   ✅ Multi-match data accumulation\
-   ✅ Automatic sorting by Points & NRR\
-   ✅ CSV Export functionality\
-   ✅ Overs-to-balls conversion logic

------------------------------------------------------------------------

## 🧠 Net Run Rate Formula

""" NRR = (Total Runs Scored / Total Overs Faced) - (Total Runs Conceded
/ Total Overs Bowled) """

Since overs are internally converted into balls:

""" Run Rate = (Runs / Balls) × 6 """

------------------------------------------------------------------------

## 🏗 Project Structure

    1. Import pandas
    2. Define overs_to_balls() utility function
    3. Define Team class
    4. Process match inputs
    5. Generate Pandas DataFrame
    6. Sort by Points and NRR
    7. Export to CSV

------------------------------------------------------------------------

## ▶️ How to Run

### Option 1: Jupyter Notebook

1.  Open the notebook.
2.  Run all cells sequentially.
3.  Enter match details when prompted.
4.  View the generated points table.

### Option 2: Python Script

``` bash
python filename.py
```

------------------------------------------------------------------------

## 📦 Requirements

-   Python 3.x
-   pandas

Install pandas using:

``` bash
pip install pandas
```

------------------------------------------------------------------------

## 📊 Output

-   Formatted points table displayed in notebook/terminal.
-   Generated file: `points_table.csv`

------------------------------------------------------------------------

## 🔮 Possible Enhancements

-   Add tie & Super Over handling
-   Add tournament fixture generator
-   Add visualization (bar charts for points & NRR)
-   Convert into a web-based dashboard
-   Load match data from CSV instead of manual input

------------------------------------------------------------------------

## 👨‍💻 Author

Developed as part of a Cricket Analytics & NRR Simulation practice
project.

------------------------------------------------------------------------

⭐ If you found this useful, consider improving it further with advanced
analytics!

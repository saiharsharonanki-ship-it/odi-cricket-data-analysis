# ODI Cricket Match Analysis (1971–2024)

## Project Overview

This project analyzes historical One Day International (ODI) cricket match data from **1971 to 2024**. The goal is to identify long-term performance trends, examine the relationship between the toss and match outcomes, compare teams, and summarize major batting and bowling performances.

The dataset contains six CSV files covering match results, batting cards, bowling cards, fall-of-wickets, partnerships, and player information.

## Objectives

1. Explore the growth of ODI cricket across decades.
2. Compare ODI teams using match wins and win rates.
3. Analyze whether winning the toss is associated with winning the match.
4. Analyze the outcome of batting first.
5. Identify the leading run scorers and wicket takers represented in the dataset.
6. Examine how average combined match scoring changed across decades.

## Dataset

Source: Kaggle — **ODI Cricket Matches Dataset (1971–2024)**.

The downloaded dataset contains:

- `odi_Matches_Data.csv` — match-level information
- `odi_Batting_Card.csv` — batting performance
- `odi_Bowling_Card.csv` — bowling performance
- `odi_Fow_Card.csv` — fall-of-wickets information
- `odi_Partnership_Card.csv` — batting partnerships
- `players_info.csv` — player information

The match-level file contains **4,745 records** and covers **1971-01-05 to 2024-03-18**.

## Main Findings

- The dataset contains **4,745 ODI match records**.
- **4,535** matches have a recorded winner and are used for winner-based analysis.
- The toss winner won the match in approximately **50.34%** of matches where both toss and match winner were available.
- The team batting first won approximately **48.47%** of analyzed matches.
- **Australia** has the highest number of wins in this dataset, with **608 wins**.
- **Sachin Tendulkar** is the leading run scorer represented in the batting data, with **18,426 runs**.
- **Muthiah Muralidaran** is the leading wicket taker represented in the bowling data, with **534 wickets**.
- Average combined scoring increased substantially from earlier decades to the 2000s and 2010s.

## Methodology

The analysis follows these steps:

1. Load CSV files with Pandas.
2. Convert dates and numeric fields to appropriate data types.
3. Handle missing values by excluding records only from analyses that require the missing field.
4. Separate decisive matches from matches without a recorded winner.
5. Calculate team matches, wins and win rates.
6. Analyze toss outcomes and batting-first outcomes.
7. Aggregate batting runs and bowling wickets by player.
8. Create charts using Matplotlib.
9. Interpret the results and document limitations.

## Project Structure

```text
odi-cricket-analysis/
├── data/
│   ├── odi_Batting_Card.csv
│   ├── odi_Bowling_Card.csv
│   ├── odi_Fow_Card.csv
│   ├── odi_Matches_Data.csv
│   ├── odi_Partnership_Card.csv
│   └── players_info.csv
├── outputs/
├── odi_cricket_analysis.py
├── requirements.txt
├── README.md
└── project_report.pdf
```

## How to Run

### 1. Install Python

Python 3.10+ is recommended.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the analysis

From the project root:

```bash
python odi_cricket_analysis.py
```

The generated charts will be saved inside the `outputs/` folder.

## Important Data Notes

The dataset includes matches without a recorded winner, including no-result and tied matches. These are not treated as wins or losses in team win-rate calculations.

There are also some missing score and toss fields. Instead of filling these values with invented data, the project excludes a record only from the specific calculation that requires the missing value.

The dataset title says 1971–2024, and the supplied snapshot contains matches through **18 March 2024**.

## Limitations

- Match outcomes are observational; the analysis does not prove that the toss causes a team to win.
- Team win rates are influenced by the number and quality of opponents faced.
- Historical ODI rules, formats and playing conditions changed over time.
- Player aggregation depends on the player identifiers supplied by the dataset.
- The dataset is a historical snapshot and may not include matches after its latest recorded date.

## Technologies

- Python
- Pandas
- NumPy
- Matplotlib

## Author

IBM SkillsBuild Data Analysis Project

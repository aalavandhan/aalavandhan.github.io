# Buffett's leverage: research behind the post

Everything here backs the post `_posts/2026-11-23-buffetts-leverage.md`. The post's chart code is in `assets/js/buffetts-leverage/` and its quote books in `_includes/buffetts-leverage/`.

## Reports to read

| File | What it is |
|---|---|
| `replication/REPORT.md` | Redoing *Buffett's Alpha* with free data: one row per paper result, with a verdict. |
| `screeners/REPORT.md` | Can a simple levered screen match Berkshire? Joint report of the two builders, ending with the sceptic's sign-off. |
| `screeners/A/FINDINGS.md` | All thirteen portfolio-level screens, every window, leverage, financing and margin table. |
| `screeners/A/PRE-REGISTRATION.md`, `screeners/B/PRE-REGISTRATION.md` | The screens and pass marks, written before anything was run. |
| `screeners/A/REVIEW-OF-B.md`, `screeners/B/REVIEW-OF-A.md` | Each builder's objections to the other. |
| `screeners/BOARD.md` | The shared message board, including builder B's findings. |

## Data collected by hand from Berkshire's letters and reports

| File | Contents |
|---|---|
| `float.csv` | Insurance float, underwriting result and cost of float, 1967-2025, with a source for each row. |
| `debt.csv` | Borrowings, interest expense, deferred taxes, derivative liabilities, Treasury bills and share counts, 1995-2025. |
| `leverage_cost.csv` | Leverage and blended cost of borrowing by year, built by `lev.py`. |

## Scripts

| File | What it does |
|---|---|
| `build_post_data.py` | Builds `assets/js/buffetts-leverage/data.js` from the CSVs and `screeners/series.csv`. Also holds the two illustrative estimates (cost of borrowing and asset returns before 1996) and the 2.2x synthetic series. |
| `sharpe_chart.py` | Draws the opening illustration into `_includes/buffetts-leverage/sharpe-distribution.svg`. |
| `sharpe.py`, `fetch.py` | Sharpe ratios for long-lived S&P 1500 members, 1976-2025 (`sharpes.json`). |
| `lev.py`, `bt.py` | First-pass leverage and backtest scripts. Superseded by `replication/` and `screeners/`; they still read some inputs from a temporary folder and will not rerun as they stand. |

## Known gaps

- Monthly Berkshire prices are only free from April 1980. Earlier years use the annual figures in the shareholder letters.
- The paper's 13F stock portfolio, private holdings and ranking against all stocks need CRSP and Thomson data and were not rebuilt.
- Interest cost for 1999-2001 is overstated (the finance businesses' interest includes repos that the debt figure leaves out).
- The virtualenvs the agents used were in a temporary folder. The replication and screener scripts need numpy, pandas, statsmodels and openpyxl.
- The downloaded market data (`replication/data/`, `screeners/*/data/`) and the bulk outputs built from it (`screeners/*/out/`) are not in the repository. The fetch scripts in each folder rebuild them.

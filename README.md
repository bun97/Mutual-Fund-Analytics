# Bluestock Mutual Fund Analytics Platform

I built this project to understand the Indian mutual fund landscape better — which funds are actually worth investing in, who the typical investor is, and what the data says about risk vs return.

## What I was trying to figure out

- Which funds give the best returns after accounting for risk?
- Are there investors who are about to stop their SIPs?
- If someone tells me their risk appetite, which fund should I recommend?

## What I found

- Large Cap funds hold 31% of total AUM — most Indian investors play it safe
- ICICI Pru Liquid Fund has the best risk-adjusted returns with a Sharpe of 7.68
- ABSL Small Cap gave the highest raw return — 24.93% in just 1 year
- Found 38 investors whose SIP gaps crossed 35 days — potential dropout risk
- 26-35 age group makes up 41% of all investors — young professionals are driving MF growth
- Kolkata and Hyderabad surprisingly outperform metros like Mumbai in SIP amounts

## How the project is structured

MUTUAL FUND ANALYTICS/
├── data/
│   ├── raw/                  # original files, untouched
│   ├── processed/            # cleaned data and computed metrics
│   └── db/                   # SQLite database
├── notebooks/
│   ├── 01_data_ingestion.ipynb       # loading and exploring raw data
│   ├── 02_data_cleaning.ipynb        # fixing dates, nulls, duplicates
│   ├── 03_eda_analysis.ipynb         # visualizations and patterns
│   ├── 04_performance_analytics.ipynb # Sharpe, CAGR, Alpha, Beta etc
│   └── 05_advanced_analytics.ipynb   # VaR, cohort analysis, recommender
├── scripts/
│   ├── etl_pipeline.py       # runs the full cleaning pipeline in one go
│   ├── live_nav_fetch.py     # pulls live NAV data from mfapi.in
│   ├── compute_metrics.py    # calculates all risk and return metrics
│   └── recommender.py        # suggests top 3 funds based on risk appetite
├── sql/
│   ├── schema.sql            # star schema with 6 tables
│   └── queries.sql           # 10 business queries I wrote
├── dashboard/
│   └── bluestock_mf.pbix     # Power BI dashboard with 4 pages
├── reports/
│   ├── Final_Report.pdf
│   └── Presentation.pptx
└── README.md

## How to run it

```bash
# clone the repo
git clone https://github.com/bun97/mutual-fund-analytics
cd mutual-fund-analytics

# install everything you need
pip install -r requirements.txt

# run the cleaning pipeline
python scripts/etl_pipeline.py

# compute the metrics
python scripts/compute_metrics.py

# then open the notebooks from 01 to 05 in order
```

## Tools I used

Python, Pandas, NumPy, SciPy, Plotly, Seaborn, SQLite, SQLAlchemy, Power BI, Jupyter, Git

## Data

NAV data came from AMFI India via the mfapi.in API. Transaction and performance data was sourced from AMFI datasets.

---

Made by **Khushee Yadav**  
[LinkedIn](https://linkedin.com/in/khushee-yadav) • [GitHub](https://github.com/bun97)
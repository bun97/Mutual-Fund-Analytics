import os
import pandas as pd
from sqlalchemy import create_engine

# setting up the base directory and db connection
os.chdir('E:/Mutual Fund Analytics')
engine = create_engine('sqlite:///data/db/bluestock_mf.db')

def run_etl():
    
    # --- NAV HISTORY ---
    nav = pd.read_csv('data/raw/02_nav_history.csv')
    
    nav['date'] = pd.to_datetime(nav['date'], dayfirst=True, errors='coerce')
    nav = nav.sort_values(['amfi_code', 'date'])
    nav = nav.drop_duplicates(subset=['amfi_code', 'date'])
    nav = nav[nav['nav'] > 0]  # removing invalid nav values
    
    nav.to_csv('data/processed/clean_nav_history.csv', index=False)
    print(f"nav done - {len(nav)} rows")

    # --- INVESTOR TRANSACTIONS ---
    txn = pd.read_csv('data/raw/08_investor_transactions.csv')
    
    txn['transaction_date'] = pd.to_datetime(txn['transaction_date'], dayfirst=True, errors='coerce')
    txn['transaction_type'] = txn['transaction_type'].str.strip()
    txn = txn[txn['amount_inr'] > 0]
    txn = txn[txn['kyc_status'].isin(['Verified', 'Pending'])]
    
    txn.to_csv('data/processed/clean_investor_transactions.csv', index=False)
    print(f"transactions done - {len(txn)} rows")

    # --- SCHEME PERFORMANCE ---
    perf = pd.read_csv('data/raw/07_scheme_performance.csv')
    
    # making sure return columns are numeric
    for col in ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct']:
        perf[col] = pd.to_numeric(perf[col], errors='coerce')
    
    # dropping cleaning flags before saving
    cols_to_drop = [c for c in perf.columns if '_anomaly' in c or c == 'expense_ratio_valid']
    perf = perf.drop(columns=cols_to_drop, errors='ignore')
    
    perf.to_csv('data/processed/clean_schema_performance.csv', index=False)
    print(f"performance done - {len(perf)} rows")

    # loading everything into sqlite
    nav.to_sql('nav_history', engine, if_exists='replace', index=False)
    txn.to_sql('investor_transactions', engine, if_exists='replace', index=False)
    perf.to_sql('scheme_performance', engine, if_exists='replace', index=False)
    
    print("all done, data loaded into db")


if __name__ == "__main__":
    run_etl()
import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

os.chdir('E:/Mutual Fund Analytics')
engine = create_engine('sqlite:///data/db/bluestock_mf.db')

# using rbi repo rate as risk free rate
RF_DAILY = 0.065 / 252

def compute_all_metrics():
    
    nav = pd.read_csv('data/processed/clean_nav_history.csv')
    nav['date'] = pd.to_datetime(nav['date'])
    nav = nav.sort_values(['amfi_code', 'date'])
    
    # daily return for each fund
    nav['daily_return'] = nav.groupby('amfi_code')['nav'].pct_change()

    results = []

    for code, group in nav.groupby('amfi_code'):
        returns = group['daily_return'].dropna()
        
        if len(returns) < 30:  # skip if not enough data
            continue

        # sharpe - return per unit of total risk
        excess = returns - RF_DAILY
        sharpe = (excess.mean() / returns.std()) * np.sqrt(252)

        # sortino - only penalizes downside risk
        downside_std = returns[returns < 0].std()
        sortino = (excess.mean() / downside_std) * np.sqrt(252) if downside_std > 0 else None

        # var and cvar - worst case loss estimates
        var_95 = np.percentile(returns, 5)
        cvar_95 = returns[returns <= var_95].mean()

        # max drawdown - worst peak to trough loss
        group = group.copy().sort_values('date')
        group['peak'] = group['nav'].cummax()
        group['drawdown'] = group['nav'] / group['peak'] - 1
        max_dd = group['drawdown'].min()
        max_dd_date = group.loc[group['drawdown'].idxmin(), 'date']

        # 3 year cagr
        end_date = group['date'].max()
        start_date = end_date - pd.DateOffset(years=3)
        three_yr = group[group['date'] >= start_date]
        
        if len(three_yr) >= 2:
            cagr_3yr = (three_yr.iloc[-1]['nav'] / three_yr.iloc[0]['nav']) ** (1/3) - 1
        else:
            cagr_3yr = None

        results.append({
            'amfi_code': code,
            'sharpe_ratio': round(sharpe, 4),
            'sortino_ratio': round(sortino, 4) if sortino else None,
            'var_95': round(var_95, 4),
            'cvar_95': round(cvar_95, 4),
            'max_drawdown': round(max_dd, 4),
            'max_drawdown_date': str(max_dd_date.date()),
            'cagr_3yr': round(cagr_3yr, 4) if cagr_3yr else None
        })

    metrics_df = pd.DataFrame(results)
    
    # save to csv and db both
    metrics_df.to_csv('data/processed/computed_metrics.csv', index=False)
    metrics_df.to_sql('computed_metrics', engine, if_exists='replace', index=False)
    
    print(f"done - computed metrics for {len(metrics_df)} funds")
    print(metrics_df.head(10))
    
    return metrics_df

if __name__ == "__main__":
    compute_all_metrics()
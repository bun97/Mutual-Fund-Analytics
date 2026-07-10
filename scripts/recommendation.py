import os
import pandas as pd

os.chdir('E:/Mutual Fund Analytics')

perf = pd.read_csv('data/processed/clean_schema_performance.csv')

def recommend_funds(risk_appetite):
    risk_appetite = risk_appetite.strip().capitalize()
    
    risk_map = {
        'Low': ['Low'],
        'Moderate': ['Moderate', 'Moderately High'],
        'High': ['High', 'Very High', 'Moderately High']
    }
    
    if risk_appetite not in risk_map:
        print("Invalid input. Please enter Low, Moderate or High.")
        return None
    
    grades = risk_map.get(risk_appetite)
    filtered = perf[perf['risk_grade'].isin(grades)]
    
    top3 = filtered.nlargest(3, 'sharpe_ratio')[
        ['amfi_code', 'schema_name', 'risk_grade',
         'sharpe_ratio', 'return_1yr_pct', 'expense_ratio_pct']
    ]
    
    print(f"\nTop 3 funds for {risk_appetite} risk appetite:")
    print(top3.to_string(index=False))
    return top3

if __name__ == "__main__":
    risk = input("Enter risk appetite (Low / Moderate / / High): ")
    recommend_funds(risk)
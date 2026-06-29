import pandas as pd
df = pd.read_csv("data/raw/08_investor_transactions.csv")

# Check exact values first
print(df['transaction_type'].unique())
print(df['kyc_status'].unique())

# Standardise transaction_type
type_map = {
    'SIP': 'SIP',               # add exact match
    'sip': 'SIP', 'Sip': 'SIP',
    'Lumpsum': 'Lumpsum',       # add exact match
    'lumpsum': 'Lumpsum', 'Lump Sum': 'Lumpsum', 'LUMPSUM': 'Lumpsum',
    'Redemption': 'Redemption', # add exact match
    'redemption': 'Redemption', 'REDEMPTION': 'Redemption', 'redeem': 'Redemption'
}
df['transaction_type'] = df['transaction_type'].str.strip().map(type_map)

# Validate amount > 0
df = df[df['amount_inr'] > 0]

# Fix date formats
df['transaction_date'] = pd.to_datetime(df['transaction_date'], dayfirst=True, errors='coerce')

# Validate KYC status
valid_kyc = ['Verified', 'Pending']
df = df[df['kyc_status'].isin(valid_kyc)]

df.to_csv('data/processed/clean_investor_transactions.csv', index=False)
print("Cleaned and saved:", len(df), "rows")
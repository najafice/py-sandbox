import pandas as pd
import pytz

# Input and output files
csv_file = "DAT_ASCII_NSXUSD_M1_202510.csv"
xlsx_file = "NDXUSDDATA.xlsx"

# Read CSV with semicolon separator, skip the last column
df = pd.read_csv(csv_file, sep=';', header=None, usecols=[0, 1, 2, 3, 4])

# Rename columns
df.columns = ['DateTime', 'Open', 'High', 'Low', 'Close']

# Convert DateTime column to proper datetime format
df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y%m%d %H%M%S')

# -----------------------------
# Convert from EST (no DST) to New York time
# -----------------------------
est_no_dst = pytz.FixedOffset(-300)  # EST without DST
new_york_tz = pytz.timezone('America/New_York')  # New York time with DST

# Localize to EST (no DST)
df['DateTime'] = df['DateTime'].dt.tz_localize(est_no_dst)

# Convert to New York time
df['DateTime'] = df['DateTime'].dt.tz_convert(new_york_tz)

# Make timezone-naive (drop tz info) so Excel can handle it
df['DateTime'] = df['DateTime'].dt.tz_localize(None)

# Write to Excel
df.to_excel(xlsx_file, index=False)

print(f"CSV has been successfully converted to {xlsx_file} with DateTime in New York time!")

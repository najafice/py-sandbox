import pandas as pd
import mplfinance as mpf
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# -----------------------------
# Step 1: Load Excel
# -----------------------------
excel_file = "NDXUSDDATA.xlsx"
df = pd.read_excel(excel_file)

# Ensure DateTime is datetime type
df['DateTime'] = pd.to_datetime(df['DateTime'])
df.set_index('DateTime', inplace=True)

# -----------------------------
# Step 2: Ask user for number of last days
# -----------------------------
n_days = int(input("Enter the number of last trading days to plot: "))

# Filter last n days
last_date = df.index.max().date()
first_date = last_date - pd.Timedelta(days=n_days-1)
df_last = df[df.index.date >= first_date]

# -----------------------------
# Step 3: Define custom style (white background, inverted colors)
# -----------------------------
mc = mpf.make_marketcolors(
    up='white', down='black', edge='black', wick='black', volume='gray'
)
s = mpf.make_mpf_style(
    marketcolors=mc,
    facecolor='white',   # background
    gridstyle='',        # no grid
    gridcolor='white'    # effectively removes grid
)

# -----------------------------
# 4: Create PDF to save all charts
# -----------------------------
pdf_filename = "nasdaq_first_hour_charts.pdf"
pdf = PdfPages(pdf_filename)

for date, day_data in df_last.groupby(df_last.index.date):
    df_first_hour = day_data.between_time('10:30', '11:30')
    if df_first_hour.empty:
        continue

    # First candle
    first_candle = df_first_hour.iloc[0]
    first_high = first_candle['High']
    first_low = first_candle['Low']

    # Horizontal lines for first candle high/low
    hlines_dict = dict(
        hlines=[first_high, first_low],
        colors=['red', 'red'],
        linestyle=['-', '-'],
        linewidths=[1, 1],
        alpha=[0.5, 0.5]
    )

    # Plot chart and return figure
    fig, axlist = mpf.plot(
        df_first_hour,
        type='candle',
        style=s,
        title=f'NASDAQ {date} First Hour Candlestick Chart (1-min)',
        ylabel='Price',
        volume=False,
        hlines=hlines_dict,
        figsize=(8, 4.5),
        returnfig=True
    )

    # Add thousand separator to y-axis
    ax = axlist[0]  # main price axis
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

    # Save figure to PDF
    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)  # <-- Correct way to close figure

# Close PDF
pdf.close()

print(f"All candlestick charts saved to {pdf_filename} with thousand separators on price axis!")

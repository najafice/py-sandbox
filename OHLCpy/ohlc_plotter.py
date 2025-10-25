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

df['DateTime'] = pd.to_datetime(df['DateTime'])
df.set_index('DateTime', inplace=True)

# -----------------------------
# Step 2: Ask user for number of last days
# -----------------------------
n_days = int(input("Enter the number of last trading days to plot: "))
last_date = df.index.max().date()
first_date = last_date - pd.Timedelta(days=n_days - 1)
df_last = df[df.index.date >= first_date]

# -----------------------------
# Step 3: Custom style
# -----------------------------
mc = mpf.make_marketcolors(up='white', down='black', edge='black', wick='black', volume='gray')
s = mpf.make_mpf_style(marketcolors=mc, facecolor='white', gridstyle='', gridcolor='white')

# -----------------------------
# Step 4: Create PDF
# -----------------------------
pdf_filename = "nasdaq_first_hour_charts.pdf"
pdf = PdfPages(pdf_filename)

for date, day_data in df_last.groupby(df_last.index.date):
    df_first_hour = day_data.between_time('10:30', '11:30')
    if df_first_hour.empty:
        continue

    first_candle = df_first_hour.iloc[0]
    first_high = first_candle['High']
    first_low = first_candle['Low']

    # Horizontal lines
    hlines_y = [first_high, first_low]
    hlines_colors = ['red', 'red']
    hlines_styles = ['-', '-']
    hlines_widths = [1, 1]
    hlines_alpha = [0.5, 0.5]

    # Breakout variables
    tp_line = None
    rrr_value = None
    tp_direction = None
    breakout_close = None
    breakout_index = None

    for i in range(1, len(df_first_hour)):
        close_price = df_first_hour.iloc[i]['Close']

        # Bullish breakout
        if close_price > first_high:
            breakout_close = close_price
            breakout_index = i
            tp_level = close_price * 1.001
            stop_loss = first_low
            if df_first_hour.iloc[i:]['High'].max() >= tp_level:
                tp_line = tp_level
                # Correct reward-to-risk
                rrr_value = (tp_line - close_price) / (close_price - stop_loss)
                tp_direction = "bull"
                hlines_y.append(tp_line)
                hlines_colors.append('blue')
                hlines_styles.append('--')
                hlines_widths.append(1)
                hlines_alpha.append(0.8)
            break

        # Bearish breakout (short)
        elif close_price < first_low:
            breakout_close = close_price
            breakout_index = i
            tp_level = close_price * 0.999
            stop_loss = first_high
            if df_first_hour.iloc[i:]['Low'].min() <= tp_level:
                tp_line = tp_level
                # Correct reward-to-risk for short: inverse
                rrr_value = (close_price - tp_line) / (stop_loss - close_price)
                tp_direction = "bear"
                hlines_y.append(tp_line)
                hlines_colors.append('blue')
                hlines_styles.append('--')
                hlines_widths.append(1)
                hlines_alpha.append(0.8)
            break

    hlines_dict = dict(
        hlines=hlines_y,
        colors=hlines_colors,
        linestyle=hlines_styles,
        linewidths=hlines_widths,
        alpha=hlines_alpha
    )

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

    ax = axlist[0]
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

    # -----------------
    # Text labels right side
    # -----------------
    x_right = len(df_first_hour) + 1

    ax.text(x_right, first_high, f"High: {first_high:,.0f}",
            color='red', fontsize=7, ha='right', va='center', backgroundcolor='white')
    ax.text(x_right, first_low, f"Low: {first_low:,.0f}",
            color='red', fontsize=7, ha='right', va='center', backgroundcolor='white')

    if tp_line is not None:
        ax.text(x_right, tp_line, f"TP: {tp_line:,.0f} – RRR: {rrr_value:.2f}",
                color='blue', fontsize=7, ha='right', va='center', backgroundcolor='white')

    # -----------------
    # Red dot for breakout
    # -----------------
    if breakout_close is not None and breakout_index is not None:
        ax.plot(breakout_index, breakout_close, 'o', color='red', markersize=5, zorder=10)
        ax.text(0.98, 0.02, f"Entry: {breakout_close:,.0f}",
                transform=ax.transAxes, fontsize=7, color='black',
                ha='right', va='bottom', backgroundcolor='white')

    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)

pdf.close()
print(f"✅ Charts saved to {pdf_filename} with correct reward-to-risk ratio for shorts.")

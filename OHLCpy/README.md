# NASDAQ First Hour Candlestick Chart Plotter

This Python project reads NASDAQ minute-level OHLC data from an Excel file and generates **candlestick charts for the first hour of each trading day**. All charts are saved into a single PDF file, formatted for compact A5 landscape printing.  

---

## Features

- Reads OHLC data from an Excel file (`DateTime, Open, High, Low, Close`).  
- Filters the **first hour of the market (10:30–11:30 local time in the dataset)**.  
- Plots **1-minute candlestick charts**.  
- White background with **white bullish bars** and **black bearish bars**.  
- Highlights **first candle high and low** with red horizontal lines.  
- Detects **breakouts** above or below the first candle:  
  - Marks **entry price** with a red dot.  
  - Calculates **take-profit (TP)** level ±0.1% of breakout close.  
  - Computes **reward-to-risk ratio (RRR)** for each trade.  
  - Displays **TP label** on chart (`TP: {price} – RRR: {value}`).  
- Labels first candle levels on the right side of chart:  
  - `High: {price}`  
  - `Low: {price}`  
- Adds **Entry price** in the bottom-right corner.  
- Supports multiple days: user can choose how many **last trading days** to plot.  
- Saves all charts into a **single PDF**.  
- Price axis formatted with **thousand separators** for readability.  
- Compact layout optimized for A5 landscape printing. 

---

## Requirements

- Python 3.10+  
- `pandas`  
- `mplfinance`  
- `matplotlib`  

Install dependencies with:

```bash
pip install pandas mplfinance matplotlib
```

## Usage

1. Place your Excel file containing OHLC data in the same folder as the script. The Excel file should have the following columns:

```bash
DateTime Open High Low Close
YYYYMMDD HHMMSS ...
```

2. Run the script:

```bash
python ohlc_plotter.py
```

3. When prompted, enter the number of last trading days you want to plot:

```bash
Enter the number of last trading days to plot: 5
```

4. The script will generate a PDF file named nasdaq_first_hour_charts.pdf in the same folder containing all charts.

## Output

- Each page of the PDF represents one trading day.
- Red horizontal lines indicate the first candle’s high and low.
- Blue dashed lines indicate TP levels if the breakout reached the target.
- Red dots mark breakout candle closes.
- Right-side labels show high/low of the first candle and TP with RRR.
- Entry price displayed in the bottom-right corner of each chart.
- Price values on the y-axis have thousand separators for readability.

## Notes

- The script assumes the data is in Eastern Standard Time (EST) without daylight saving adjustment.
- Only the first hour of the market is plotted.
- TP lines are plotted only if the price actually reached the target within the first hour.
- Reward-to-risk ratio for short positions is correctly calculated (inverted).

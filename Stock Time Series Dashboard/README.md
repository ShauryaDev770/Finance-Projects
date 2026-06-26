# 📈 Live Stock Time Series Analysis Dashboard

A Streamlit-based interactive dashboard for visualising stock price history, returns, and volatility — with an automated data pipeline to keep the CSV up to date.

---

## Project Structure

```
├── stock_dashboard.py              # Streamlit dashboard
├── stock_data_pipeline.py         # Data fetch & update script
└── Stock_data.csv      # Auto-generated local data store
```

---

## Features

- **Candlestick + Volume chart** — interactive price history with range slider
- **20-Day Moving Average** — toggleable overlay on the candlestick chart
- **Log Returns** — time series line chart and distribution histogram, side by side
- **Rolling Volatility** — 10-day rolling window, annualised (×√252)
- **Live metrics** — current price, day change, and 52-week high shown as cards
- **Tickers supported** — AAPL, TSLA, ^NSEI (Nifty 50)

---

## Data Pipeline (`stock_data_pipeline.py`)

The `update_stock_csv()` function manages a local `Stock_data.csv`:

- If the file **doesn't exist** → downloads 1 year of daily data via `yfinance` and creates it
- If the file **exists but is empty** → re-downloads full history
- If the file **exists with data** → fetches only rows newer than the last recorded date and appends them

This means you only pull new data on each run rather than re-downloading everything.

**Run it before launching the dashboard to ensure fresh data:**
```bash
python stock_data_pipeline.py
```

---

## Setup

**Requirements**
```
streamlit
pandas
numpy
plotly
yfinance
```

Install with:
```bash
pip install streamlit pandas numpy plotly yfinance
```

**Run the dashboard**
```bash
python -m streamlit run stock_dashboard.py
```

---

## How It Works

| Section | What it shows |
|---|---|
| Sidebar | Ticker selector |
| Metric cards | Current price · Day change · 52-week high |
| Candlestick chart | OHLC price + volume bars, optional 20-day MA |
| Returns Analysis | Log returns over time + return distribution |
| Rolling Volatility | Annualised volatility using a 10-day rolling window |

---

## Notes

- Data is stored locally in `Stock_data.csv` — re-run `stock_data_pipeline.py` any time you want to sync the latest prices.
- The dashboard reads from the CSV only; it does not make live API calls at render time.
- Nifty 50 volume data may appear as zero — this is a known `yfinance` limitation for `^NSEI`.

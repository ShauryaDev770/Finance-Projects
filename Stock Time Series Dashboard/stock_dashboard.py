import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import plotly.subplots as ms
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Live Stock Data Dashboard", page_icon='📈', layout="wide")

# ── Global dark theme constants ───────────────────────────────────────────────
BG       = "#0e1117"
CARD_BG  = "#161b22"
ACCENT   = "#00BFFF"
ACCENT2  = "#7B68EE"
GRID_CLR = "#21262d"

# ── Inject custom CSS ─────────────────────────────────────────────────────────
st.markdown(f"""
    <style>
        /* Page background */
        .stApp {{ background-color: {BG}; }}

        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {CARD_BG};
            border-right: 1px solid {GRID_CLR};
        }}

        /* All markdown text */
        .stMarkdown, .stMarkdown p {{ color: #c9d1d9; }}

        /* Section headers */
        h1, h2, h3 {{ color: #e6edf3 !important; letter-spacing: 0.03em; }}

        /* Metric cards */
        [data-testid="stMetric"] {{
            background-color: {CARD_BG};
            border: 1px solid {GRID_CLR};
            border-radius: 10px;
            padding: 16px 20px;
        }}
        [data-testid="stMetricLabel"] {{ color: #8b949e !important; font-size: 0.82rem; }}
        [data-testid="stMetricValue"] {{ color: {ACCENT} !important; font-size: 1.6rem; font-weight: 700; }}

        /* Selectbox */
        [data-testid="stSelectbox"] label {{ color: #c9d1d9 !important; }}

        /* Checkbox */
        [data-testid="stCheckbox"] label {{ color: #c9d1d9 !important; }}

        /* Divider */
        hr {{ border-color: {GRID_CLR} !important; margin: 1.5rem 0; }}

        /* Plotly chart containers — subtle card feel */
        [data-testid="stPlotlyChart"] {{
            background-color: {CARD_BG};
            border: 1px solid {GRID_CLR};
            border-radius: 10px;
            padding: 8px;
        }}
    </style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📈 Dashboard")
    st.markdown("---")
    ticker = ["AAPL", "TSLA", "^NSEI"]
    choice = st.selectbox("Select Ticker", ticker)
    st.markdown("---")
    st.markdown(
        "<span style='color:#8b949e; font-size:0.78rem;'>Data sourced from local CSV.<br>Charts powered by Plotly.</span>",
        unsafe_allow_html=True
    )

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("# 📈 Stock Time Series Analysis Dashboard")
st.markdown("---")


# ─────────────────────────────────────────────────────────────────────────────
#  FUNCTIONS  (logic untouched — only chart styling & layout changed)
# ─────────────────────────────────────────────────────────────────────────────

def Rolling_Volitility():
    df = pd.read_csv("Stock_data.csv", parse_dates=['Date'])
    df["Date"] = pd.to_datetime(df["Date"], utc=True)

    df['Log_Returns'] = np.log1p(df[f"{choice}.Close"] / df[f"{choice}.Close"].shift(1))
    df.dropna(inplace=True)
    df_clean = df.dropna()
    trading_window = 10

    df['Rolling_Daily_Vol'] = df['Log_Returns'].rolling(window=trading_window).std()
    annualization_factor = np.sqrt(252)
    df['Rolling_Annual_Vol'] = df['Rolling_Daily_Vol'] * annualization_factor
    df.dropna(subset=['Log_Returns', 'Rolling_Annual_Vol'], inplace=True)

    plot = px.line(
        title="🔀 Rolling Volatility (Annualized)",
        x=df["Date"],
        y=df['Rolling_Annual_Vol'],
        labels={'x': 'Time', 'y': "Annualized Volatility"},
        template="plotly_dark",
        color_discrete_sequence=[ACCENT2]
    )
    plot.update_layout(
        plot_bgcolor=BG,
        paper_bgcolor=CARD_BG,
        font_color="#c9d1d9",
        hovermode="x unified",
        margin=dict(t=55, b=40, l=50, r=20),
        xaxis=dict(gridcolor=GRID_CLR, zeroline=False),
        yaxis=dict(gridcolor=GRID_CLR, zeroline=False),
    )
    plot.update_traces(line_width=1.8)
    return st.plotly_chart(plot, use_container_width=True)


def Moving_Average(df, choice, figure):
    option = st.checkbox("Apply 20-Day Moving Average")
    if option:
        df = pd.read_csv("Stock_data.csv", parse_dates=["Date"])
        df["Date"] = pd.to_datetime(df["Date"], utc=True)

        column_name = f"{choice}.Close"
        df.dropna(subset=[column_name], inplace=True)

        Close_prices = df[column_name].to_numpy()
        n = 20
        weights = np.ones(n) / n

        ma_values = np.convolve(Close_prices, weights, mode="valid")
        padding = np.full(n - 1, np.nan)

        df["ma20"] = np.concatenate((padding, ma_values))

        figure.add_trace(go.Scatter(
            x=df["Date"],
            y=df["ma20"],
            mode="lines",
            name="20-Day MA",
            line=dict(color="blue", width=2)
        ), row=1, col=1)
        figure.update_layout(
            title=f"{choice} 20-Day MA",
            xaxis_rangeslider_visible=False,
            template="plotly_white"
        )

        return figure


def Log_returns(choice):
    df = pd.read_csv("Stock_data.csv", parse_dates=['Date'])
    df["Date"] = pd.to_datetime(df["Date"], utc=True)
    Log_Returns = np.log1p(df[f"{choice}.Close"] / df[f"{choice}.Close"].shift(1))

    graph = px.line(
        x=df["Date"],
        y=Log_Returns,
        title="📉 Log Returns Over Time",
        labels={"x": "Time", "y": "Log Return"},
        template="plotly_dark",
        color_discrete_sequence=[ACCENT]
    )
    graph.update_layout(
        plot_bgcolor=BG,
        paper_bgcolor=CARD_BG,
        font_color="#c9d1d9",
        hovermode="x unified",
        margin=dict(t=55, b=40, l=50, r=20),
        xaxis=dict(gridcolor=GRID_CLR, zeroline=False),
        yaxis=dict(gridcolor=GRID_CLR, zeroline=False),
    )
    graph.update_traces(line_width=1.5)

    cleaned_returns = Log_Returns.dropna()
    fig = px.histogram(
        x=cleaned_returns,
        title="📊 Log Returns Distribution",
        labels={'x': 'Log Returns'},
        nbins=50,
        template="plotly_dark",
        color_discrete_sequence=[ACCENT2]
    )
    fig.update_traces(
        marker_line_color='white',
        marker_line_width=1.5,
    )
    fig.update_layout(
        plot_bgcolor=BG,
        paper_bgcolor=CARD_BG,
        font_color="#c9d1d9",
        margin=dict(t=55, b=40, l=50, r=20),
        xaxis=dict(gridcolor=GRID_CLR, zeroline=False),
        yaxis=dict(gridcolor=GRID_CLR, zeroline=False),
    )

    st.markdown("### 📐 Returns Analysis")
    left_column, right_column = st.columns(2)
    with left_column:
        st.plotly_chart(graph, use_container_width=True)
    with right_column:
        st.plotly_chart(fig, use_container_width=True)


def build_candlestick(df, choice):
    figure = ms.make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        row_heights=[0.7, 0.3]
    )

    figure.add_trace(go.Candlestick(
        x=df["Date"],
        open=df[f'{choice}.Open'],
        high=df[f'{choice}.High'],
        close=df[f'{choice}.Close'],
        low=df[f'{choice}.Low'],
        increasing_line_color="green",
        decreasing_line_color="red"
    ), row=1, col=1)

    Moving_Average(df, choice, figure)

    figure.add_trace(go.Bar(
        x=df.index,
        y=df[f"{choice}.Volume"],
        marker_color="#4A90D9",
        opacity=0.7
    ), row=2, col=1)

    figure.update_layout(
        title="🕯️ Interactive Candlestick Chart",
        yaxis1_title="Stock Price",
        yaxis2_title="Volume (M)",
        xaxis2_title="Time",
        xaxis1_rangeslider_visible=False,
        xaxis2_rangeslider_visible=True,
        template="plotly_dark",
        plot_bgcolor=BG,
        paper_bgcolor=CARD_BG,
        font_color="#c9d1d9",
        hovermode="x unified",
        legend_visible=False,
        margin=dict(t=60, b=40, l=50, r=20),
        xaxis=dict(gridcolor=GRID_CLR),
        yaxis=dict(gridcolor=GRID_CLR),
    )
    return st.plotly_chart(figure, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN RENDER
# ─────────────────────────────────────────────────────────────────────────────

df = pd.read_csv("Stock_data.csv", parse_dates=['Date'])
df = df.set_index(pd.DatetimeIndex(df["Date"].values))

TICKER_META = {
    "AAPL":  {"label": "🍎 AAPL — Current Price",     "prefix": "$",  "currency": "USD"},
    "TSLA":  {"label": "⚡ TSLA — Current Price",      "prefix": "$",  "currency": "USD"},
    "^NSEI": {"label": "🇮🇳 NIFTY 50 — Current Price", "prefix": "₹", "currency": "INR"},
}

meta         = TICKER_META[choice]
close_col    = f"{choice}.Close"
current_price = df[close_col].iloc[-1]

# ── Metric row ────────────────────────────────────────────────────────────────
m1, m2, m3 = st.columns(3)
with m1:
    st.metric(label=meta["label"], value=f"{meta['prefix']}{current_price:,.2f}")
with m2:
    daily_chg = df[close_col].iloc[-1] - df[close_col].iloc[-2]
    pct_chg   = (daily_chg / df[close_col].iloc[-2]) * 100
    st.metric(label="Day Change", value=f"{meta['prefix']}{daily_chg:+.2f}", delta=f"{pct_chg:+.2f}%")
with m3:
    st.metric(label="52-Week High", value=f"{meta['prefix']}{df[close_col].tail(252).max():,.2f}")

st.markdown("---")

# ── Candlestick section ───────────────────────────────────────────────────────
st.markdown("### 🕯️ Price & Volume")
build_candlestick(df, choice)
st.markdown("---")

# ── Returns section ───────────────────────────────────────────────────────────
Log_returns(choice)
st.markdown("---")

# ── Volatility section ────────────────────────────────────────────────────────
st.markdown("### 🔀 Rolling Volatility")
Rolling_Volitility()
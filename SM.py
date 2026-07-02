import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="Global Stock Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------
# CUSTOM CSS
# ----------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.metric-card{
    background:#161B22;
    padding:20px;
    border-radius:12px;
    text-align:center;
    box-shadow:0px 0px 10px rgba(255,255,255,0.05);
}

.metric-title{
    font-size:15px;
    color:#AAAAAA;
}

.metric-value{
    font-size:28px;
    font-weight:bold;
    color:white;
}

.big-font{
    font-size:42px;
    font-weight:bold;
}

.small-font{
    color:#00C853;
    font-size:18px;
}

footer{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# TITLE
# ----------------------------------------------------

st.title("📈 Global Stock Dashboard")
st.caption("Powered by Yahoo Finance")

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

st.sidebar.header("Search Stock")

suggestions = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Tesla": "TSLA",
    "Amazon": "AMZN",
    "Google": "GOOGL",
    "NVIDIA": "NVDA",
    "Meta": "META",
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS"
}

company = st.sidebar.selectbox(
    "Suggested Stocks",
    list(suggestions.keys())
)

default_symbol = suggestions[company]

symbol = st.sidebar.text_input(
    "Or Enter Symbol",
    value=default_symbol
).upper()

# ----------------------------------------------------
# TIME PERIOD
# ----------------------------------------------------

period = st.sidebar.radio(
    "Time Period",
    [
        "1d",
        "5d",
        "1mo",
        "6mo",
        "1y",
        "5y",
        "max"
    ]
)

# ----------------------------------------------------
# CACHE DATA
# ----------------------------------------------------

@st.cache_data(ttl=300)
def load_stock(symbol):

    ticker = yf.Ticker(symbol)

    info = ticker.info

    history = ticker.history(period=period)

    return ticker, info, history

# ----------------------------------------------------
# FORMAT LARGE NUMBERS
# ----------------------------------------------------

def human_format(num):

    if num is None:
        return "N/A"

    num = float(num)

    magnitude = 0

    while abs(num) >= 1000:

        magnitude += 1

        num /= 1000.0

    return "%.2f%s" % (
        num,
        ['', 'K', 'M', 'B', 'T'][magnitude]
    )

# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------

with st.spinner("Fetching data from Yahoo Finance..."):

    try:

        ticker, info, history = load_stock(symbol)

    except Exception:

        st.error("Unable to fetch stock data.")

        st.stop()

if history.empty:

    st.error("Invalid stock symbol.")

    st.stop()
  # ----------------------------------------------------
# COMPANY INFORMATION
# ----------------------------------------------------

company_name = info.get("longName", symbol)
sector = info.get("sector", "N/A")
industry = info.get("industry", "N/A")
website = info.get("website", "N/A")

current_price = info.get(
    "currentPrice",
    info.get("regularMarketPrice", 0)
)

previous_close = info.get("previousClose", 0)
open_price = info.get("open", 0)
day_high = info.get("dayHigh", 0)
day_low = info.get("dayLow", 0)
volume = info.get("volume", 0)
market_cap = info.get("marketCap", 0)

# ----------------------------------------------------
# PRICE CHANGE
# ----------------------------------------------------

change = current_price - previous_close

if previous_close:
    percent_change = (change / previous_close) * 100
else:
    percent_change = 0

if change >= 0:
    arrow = "▲"
    color = "#00C853"
else:
    arrow = "▼"
    color = "#FF5252"

# ----------------------------------------------------
# HEADER
# ----------------------------------------------------

st.markdown(f"## {company_name}")

col1, col2 = st.columns([3, 1])

with col1:

    st.markdown(
        f"""
        <div class="big-font">
            ${current_price:.2f}
        </div>

        <div style="font-size:20px;color:{color};">
            {arrow} {change:.2f} ({percent_change:.2f}%)
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.metric(
        label="Symbol",
        value=symbol
    )

# ----------------------------------------------------
# COMPANY DETAILS
# ----------------------------------------------------

st.write(f"**Sector:** {sector}")
st.write(f"**Industry:** {industry}")

if website != "N/A":
    st.markdown(f"🌐 {website}")

st.divider()

# ----------------------------------------------------
# METRIC CARDS
# ----------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Previous Close",
        f"${previous_close:.2f}"
    )

with c2:
    st.metric(
        "Open",
        f"${open_price:.2f}"
    )

with c3:
    st.metric(
        "Day High",
        f"${day_high:.2f}"
    )

with c4:
    st.metric(
        "Day Low",
        f"${day_low:.2f}"
    )

st.write("")

c5, c6, c7 = st.columns(3)

with c5:
    st.metric(
        "Volume",
        human_format(volume)
    )

with c6:
    st.metric(
        "Market Cap",
        human_format(market_cap)
    )

with c7:

    avg_volume = info.get("averageVolume", None)

    if avg_volume:
        st.metric(
            "Avg Volume",
            human_format(avg_volume)
        )
    else:
        st.metric(
            "Avg Volume",
            "N/A"
        )

st.divider()

# ----------------------------------------------------
# COMPANY DESCRIPTION
# ----------------------------------------------------

description = info.get("longBusinessSummary", "")

if description:

    st.subheader("About the Company")

    st.write(description)

st.divider()
# ----------------------------------------------------
# COMPANY INFORMATION
# ----------------------------------------------------

company_name = info.get("longName", symbol)
sector = info.get("sector", "N/A")
industry = info.get("industry", "N/A")
website = info.get("website", "N/A")

current_price = info.get(
    "currentPrice",
    info.get("regularMarketPrice", 0)
)

previous_close = info.get("previousClose", 0)
open_price = info.get("open", 0)
day_high = info.get("dayHigh", 0)
day_low = info.get("dayLow", 0)
volume = info.get("volume", 0)
market_cap = info.get("marketCap", 0)

# ----------------------------------------------------
# PRICE CHANGE
# ----------------------------------------------------

change = current_price - previous_close

if previous_close:
    percent_change = (change / previous_close) * 100
else:
    percent_change = 0

if change >= 0:
    arrow = "▲"
    color = "#00C853"
else:
    arrow = "▼"
    color = "#FF5252"

# ----------------------------------------------------
# HEADER
# ----------------------------------------------------

st.markdown(f"## {company_name}")

col1, col2 = st.columns([3, 1])

with col1:

    st.markdown(
        f"""
        <div class="big-font">
            ${current_price:.2f}
        </div>

        <div style="font-size:20px;color:{color};">
            {arrow} {change:.2f} ({percent_change:.2f}%)
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.metric(
        label="Symbol",
        value=symbol
    )

# ----------------------------------------------------
# COMPANY DETAILS
# ----------------------------------------------------

st.write(f"**Sector:** {sector}")
st.write(f"**Industry:** {industry}")

if website != "N/A":
    st.markdown(f"🌐 {website}")

st.divider()

# ----------------------------------------------------
# METRIC CARDS
# ----------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Previous Close",
        f"${previous_close:.2f}"
    )

with c2:
    st.metric(
        "Open",
        f"${open_price:.2f}"
    )

with c3:
    st.metric(
        "Day High",
        f"${day_high:.2f}"
    )

with c4:
    st.metric(
        "Day Low",
        f"${day_low:.2f}"
    )

st.write("")

c5, c6, c7 = st.columns(3)

with c5:
    st.metric(
        "Volume",
        human_format(volume)
    )

with c6:
    st.metric(
        "Market Cap",
        human_format(market_cap)
    )

with c7:

    avg_volume = info.get("averageVolume", None)

    if avg_volume:
        st.metric(
            "Avg Volume",
            human_format(avg_volume)
        )
    else:
        st.metric(
            "Avg Volume",
            "N/A"
        )

st.divider()

# ----------------------------------------------------
# COMPANY DESCRIPTION
# ----------------------------------------------------

description = info.get("longBusinessSummary", "")

if description:

    st.subheader("About the Company")

    st.write(description)

st.divider()

import streamlit as st
import requests

# Page Configuration
st.set_page_config(page_title="Live Crypto Momentum Hub", page_icon="📈", layout="wide")

# Custom CSS for Professional Styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .ticker-container {
        background-color: #1f2937;
        color: #10b981;
        padding: 10px;
        font-weight: bold;
        border-radius: 5px;
        margin-bottom: 20px;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        background-color: #3b82f6;
        color: white;
        font-weight: bold;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Live Ticker Header
st.markdown("""
    <div class="ticker-container">
        🚀 <b>Live Market Tracker:</b> Real-time cryptocurrency momentum updating continuously... | 📈 Top Gainers & 📉 Top Losers live view.
    </div>
""", unsafe_allow_html=True)

st.title("📈 Live Crypto Momentum Hub")
st.write("Welcome! This dashboard automatically tracks and sorts the top 10 upward and downward moving cryptocurrencies in real-time.")

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(["🏠 Home (Top Gainers & Losers)", "🪙 All Coins Market", "📰 Latest News"])

# Fetching Live Data from Binance API
try:
    url_24hr = "https://api.binance.com/api/v3/ticker/24hr"
    res_24hr = requests.get(url_24hr)
    stats_data = res_24hr.json() if res_24hr.status_code == 200 else []
except:
    stats_data = []

with tab1:
    # Search Bar at Top Left
    col_search, col_space = st.columns([1, 2])
    with col_search:
        st.subheader("🔍 Search Coin")
        search_query = st.text_input("Search any coin symbol (e.g., BTC, ETH):", "").upper()

    if search_query and stats_data:
        filtered = [c for c in stats_data if search_query in c['symbol']]
        if filtered:
            st.write(f"Search Results ({len(filtered)}):")
            for c in filtered[:10]:
                change_val = float(c.get('priceChangePercent', 0))
                trend_icon = "📈" if change_val >= 0 else "📉"
                st.info(f"{trend_icon} **{c['symbol']}** : ${float(c['price']):,.4f} ({change_val:+.2f}%)")
        else:
            st.warning("No matching coin found.")

    st.divider()
    st.subheader("📊 Real-Time Market Momentum Analysis")
    
    # Timeframe selection (UI feature)
    time_frame = st.selectbox(
        "⏱️ Select Time Frame:",
        ["1 Minute (1m)", "3 Minutes (3m)", "5 Minutes (5m)", "12 Hours (12h)", "24 Hours (24h)", "All Time"]
    )

    if stats_data:
        # Separate coins into Gainers (Up) and Losers (Down) based on priceChangePercent
        gainers = sorted([c for c in stats_data if float(c.get('priceChangePercent', 0)) >= 0], 
                         key=lambda x: float(x.get('priceChangePercent', 0)), reverse=True)
        
        losers = sorted([c for c in stats_data if float(c.get('priceChangePercent', 0)) < 0], 
                        key=lambda x: float(x.get('priceChangePercent', 0)))

        # Take Top 10 Gainers and Top 10 Losers
        top_10_gainers = gainers[:10]
        top_10_losers = losers[:10]

        col_up, col_down = st.columns(2)

        with col_up:
            st.markdown("### 🚀 Top 10 Gainers (Up Momentum)")
            gainers_list = []
            for idx, coin in enumerate(top_10_gainers, 1):
                sym = coin['symbol']
                price = float(coin['price'])
                change_percent = float(coin['priceChangePercent'])
                short_name = sym.replace('USDT', '')
                
                gainers_list.append({
                    "No.": idx,
                    "Coin": short_name,
                    "Status": "📈 Up",
                    "Change (%)": f"{change_percent:+.2f}%",
                    "Price ($)": f"${price:,.4f}"
                })
            st.table(gainers_list)

        with col_down:
            st.markdown("### 📉 Top 10 Losers (Down Momentum)")
            losers_list = []
            for idx, coin in enumerate(top_10_losers, 1):
                sym = coin['symbol']
                price = float(coin['price'])
                change_percent = float(coin['priceChangePercent'])
                short_name = sym.replace('USDT', '')
                
                losers_list.append({
                    "No.": idx,
                    "Coin": short_name,
                    "Status": "📉 Down",
                    "Change (%)": f"{change_percent:+.2f}%",
                    "Price ($)": f"${price:,.4f}"
                })
            st.table(losers_list)

with tab2:
    st.subheader("🪙 All Coins Market Overview")
    if stats_data:
        all_market_list = []
        for idx, c in enumerate(stats_data[:30], 1):
            change_val = float(c.get('priceChangePercent', 0))
            status = "📈 Up" if change_val >= 0 else "📉 Down"
            all_market_list.append({
                "No.": idx,
                "Symbol": c['symbol'],
                "Price ($)": f"${float(c['price']):,.4f}",
                "24h Change": f"{change_val:+.2f}%",
                "Trend": status
            })
        st.table(all_market_list)

with tab3:
    st.subheader("📰 Latest Crypto News & Updates")
    st.markdown("""
    * **1. Bitcoin Bull Run Continues:** Institutional demand pushes BTC higher as market momentum accelerates.
    * **2. Ethereum Ecosystem Upgrades:** Layer 2 scaling solutions drive down transaction costs significantly.
    * **3. Solana Network Activity:** High transaction volumes maintain strong upward pressure on SOL market performance.
    """)

st.divider()
if st.button("🔄 Refresh Data"):
    st.rerun()

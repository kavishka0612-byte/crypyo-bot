import streamlit as st
import requests

# පිටුවේ මූලික සැකසුම්
st.set_page_config(page_title="Crypto Pulse & Market Hub", page_icon="🌐", layout="wide")

# CSS මඟින් ලස්සන මෝස්තර එකතු කිරීම
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

# උඩින් දිගට යන ප්‍රවෘත්ති ටිකක් (Ticker)
st.markdown("""
    <div class="ticker-container">
        🔥 <b>Live Crypto Market:</b> Real-time tracking updated continuously. | 📈 Monitor top momentum coins instantly!
    </div>
""", unsafe_allow_html=True)

st.title("🌐 Crypto Pulse & Market Hub")
st.write("වෙබ් අඩවියට සාදරයෙන් පිළිගනිමු! මෙහි ලයිව් ක්‍රිප්ටෝ මිල ගණන් සහ මෝමන්ට් බලාගත හැක.")

# ටැබ් මඟින් අංශ වෙන් කිරීම
tab1, tab2, tab3 = st.tabs(["🏠 Home", "🪙 Coins", "📰 Latest News"])

# Binance API මඟින් දත්ත ලබා ගැනීම
try:
    url_24hr = "https://api.binance.com/api/v3/ticker/24hr"
    res_24hr = requests.get(url_24hr)
    stats_data = res_24hr.json() if res_24hr.status_code == 200 else []
except:
    stats_data = []

with tab1:
    col_search, col_space = st.columns([1, 2])
    with col_search:
        st.subheader("🔍 Search Coin")
        search_query = st.text_input("කොයින් එකක් සර්ච් කරන්න:", "").upper()

    if search_query and stats_data:
        filtered = [c for c in stats_data if search_query in c['symbol']]
        if filtered:
            st.write(f"සැලකිය යුතු ප්‍රතිඵල ({len(filtered)}):")
            for c in filtered[:10]:
                change_val = float(c.get('priceChangePercent', 0))
                trend_icon = "📈" if change_val > 0.5 else ("📉" if change_val < -0.5 else "⚖️")
                st.info(f"{trend_icon} **{c['symbol']}** : ${float(c['price']):,.4f} ({change_val:+.2f}%)")
        else:
            st.warning("අදාළ නමින් කොයින් එකක් හමු නොවීය.")

    st.divider()
    st.subheader("🔥 Home - වෙළඳපොළේ වැඩිම මෝමන්ට් ඇති ප්‍රධාන කොයින් 10")
    
    # කාල රාමුව (Time Frame) තෝරාගැනීමේ පහසුකම
    time_frame = st.selectbox(
        "⏱️ කාල රාමුව (Time Frame) තෝරන්න:",
        ["විනාඩිය (1m)", "විනාඩි 3 (3m)", "විනාඩි 5 (5m)", "පැය 12 (12h)", "පැය 24 (24h)", "සියලු කාලසීමා (All Time)"],
        key="home_timeframe"
    )

    if stats_data:
        # මිල වෙනස්වීමේ ප්‍රතිශතය මත වැඩිම මෝමන්ට් එකක් ඇති කොයින් 10 තෝරා ගැනීම
        sorted_coins = sorted(stats_data, key=lambda x: abs(float(x.get('priceChangePercent', 0))), reverse=True)
        top_10_momentum = sorted_coins[:10]

        momentum_list = []
        idx = 1
        for coin in top_10_momentum:
            sym = coin['symbol']
            price = float(coin['price'])
            change_percent = float(coin['priceChangePercent'])
            
            # මෝමන්ට් තත්ත්වය තීරණය කිරීම (Up, Down හෝ Ranging)
            if change_percent > 0.5:
                status_trend = "📈 අප් (Up)"
            elif change_percent < -0.5:
                status_trend = "📉 ඩවුන් (Down)"
            else:
                status_trend = "⚖️ රේන්ජින් (Ranging)"
                
            short_name = sym.replace('USDT', '')
            full_name = f"{short_name} Token"
            
            momentum_list.append({
                "No.": idx,
                "Coin Name": full_name,
                "Short Name": short_name,
                "Market Momentum": status_trend,
                "Current Price ($)": f"${price:,.4f}"
            })
            idx += 1

        st.table(momentum_list)

with tab2:
    st.subheader("🪙 Coins - සියලුම ක්‍රිප්ටෝ කොයින් ලැයිස්තුව")
    if stats_data:
        basic_list = []
        for idx, c in enumerate(stats_data[:20], 1):
            basic_list.append({
                "No.": idx,
                "Symbol": c['symbol'],
                "Price ($)": f"${float(c['price']):,.4f}"
            })
        st.table(basic_list)

with tab3:
    st.subheader("📰 Latest Crypto News & Updates")
    st.markdown("""
    * **1. Bitcoin Bull Run Continues:** Institutional investors are heavily accumulating BTC.
    * **2. Ethereum Layer 2 Scaling:** Gas fees reach historical lows following upgrades.
    * **3. Solana DeFi Volume Surges:** Decentralized exchanges record massive volumes.
    """)

st.divider()
if st.button("🔄 දත්ත නැවුම් කරන්න (Refresh)"):
    st.rerun()

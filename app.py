import streamlit as st
import requests

# පිටුවේ මූලික සැකසුම්
st.set_page_config(page_title="Crypto Pulse & Market Hub", page_icon="🌐", layout="wide")

# රහස් කී එක (Secret Key)
VALID_ACCESS_KEY = "my_secret_key_123"

# CSS මඟින් ලස්සන මෝස්තර සහ Ticker එකතු කිරීම
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
        🔥 <b>Breaking News:</b> Bitcoin hits new milestones! | 🚀 Solana ecosystem expands rapidly! | 💡 Ethereum gas fees drop significantly! | 📈 Crypto market shows strong bullish momentum today!
    </div>
""", unsafe_allow_html=True)

st.title("🌐 Crypto Pulse & Market Hub")
st.write("වෙබ් අඩවියට පිවිසීමට කරුණාකර ඔබගේ ප්‍රවේශ කී (Access Key) ඇතුළත් කරන්න.")

user_key = st.text_input("Access Key ඇතුළත් කරන්න:", type="password")

if user_key:
    if user_key == VALID_ACCESS_KEY:
        st.success("සාර්ථකයි! ඔබට දැන් වෙබ් අඩවියේ සියලුම අංශ වෙත පිවිසිය හැක.")
        
        # ටැබ් මඟින් අංශ වෙන් කිරීම
        tab1, tab2, tab3 = st.tabs(["🏠 Home", "🪙 Coins", "📰 Latest News"])

        # Binance API මඟින් දත්ත ලබා ගැනීම
        try:
            url_price = "https://api.binance.com/api/v3/ticker/price"
            res_price = requests.get(url_price)
            prices_data = res_price.json() if res_price.status_code == 200 else []

            url_24hr = "https://api.binance.com/api/v3/ticker/24hr"
            res_24hr = requests.get(url_24hr)
            stats_data = res_24hr.json() if res_24hr.status_code == 200 else []
            
            # 24hr දත්ත ඩික්ෂනරි එකකට හැරවීම
            stats_dict = {item['symbol']: item for item in stats_data}
        except:
            prices_data = []
            stats_dict = {}

        with tab1:
            # සර්ච් බාර් එක වම් පැත්තේ උඩ කෙළවරට සකස් කිරීම
            col_search, col_space = st.columns([1, 2])
            with col_search:
                st.subheader("🔍 Search Coin")
                search_query = st.text_input("කොයින් එකක් සර්ච් කරන්න:", "").upper()

            if search_query and prices_data:
                filtered = [c for c in prices_data if search_query in c['symbol']]
                if filtered:
                    st.write(f"සැලකිය යුතු ප්‍රතිඵල ({len(filtered)}):")
                    for c in filtered[:10]:
                        st.info(f"🪙 **{c['symbol']}** : ${float(c['price']):,.4f}")
                else:
                    st.warning("අදාළ නමින් කොයින් එකක් හමු නොවීය.")

            st.divider()
            st.subheader("🏠 ප්‍රධාන ජනප්‍රිය කොයින් මිල ගණන්")
            if prices_data:
                c1, c2, c3 = st.columns(3)
                targets = {'BTCUSDT': 'Bitcoin (BTC)', 'ETHUSDT': 'Ethereum (ETH)', 'SOLUSDT': 'Solana (SOL)'}
                cols = [c1, c2, c3]
                i = 0
                for coin in prices_data:
                    if coin['symbol'] in targets and i < 3:
                        with cols[i]:
                            st.metric(label=targets[coin['symbol']], value=f"${float(coin['price']):,.2f}")
                        i += 1

        with tab2:
            st.subheader("🪙 Coins - සියලුම ක්‍රිප්ටෝ කොයින් ලැයිස්තුව")
            
            # ටයිම් ෆ්‍රේම් (Time Frame) තෝරාගැනීමේ පහසුකම
            time_frame = st.selectbox(
                "⏱️ කාල රාමුව (Time Frame) තෝරන්න:",
                ["විනාඩිය (1m)", "විනාඩි 3 (3m)", "විනාඩි 5 (5m)", "පැය 12 (12h)", "පැය 24 (24h)", "සියලු කාලසීමා (All Time)"]
            )
            st.write(selectedValue := f"নির্বাচিত කාල රාමුව: **{time_frame}** යටතේ දත්ත පෙන්වයි.")

            if prices_data and stats_dict:
                # අංක පෝලිමට පෙන්වීම සඳහා ටේබල් හෝ ලැයිස්තු සැකසුම
                coin_list = []
                idx = 1
                for item in prices_data[:30]: # ප්‍රධාන කොයින් 30ක් පෙන්වීම
                    sym = item['symbol']
                    price = float(item['price'])
                    stat = stats_dict.get(sym, {})
                    
                    high_price = float(stat.get('highPrice', price))
                    low_price = float(stat.get('lowPrice', price))
                    price_change = float(stat.get('priceChangePercent', 0))
                    
                    status_trend = "📈 අප් (Up)" if price_change >= 0 else "📉 ඩවුන් (Down)"
                    
                    # ෂෝට් නේම් සහ ෆුල් නේම් ලෙස සකස් කිරීම
                    short_name = sym.replace('USDT', '')
                    full_name = f"{short_name} Network / Token" # ආසන්න නාමකරණයක්
                    
                    coin_list.append({
                        "No.": idx,
                        "Full Name": full_name,
                        "Short Name": short_name,
                        "Current Price ($)": f"${price:,.4f}",
                        "High Price ($)": f"${high_price:,.4f}",
                        "Low Price ($)": f"${low_price:,.4f}",
                        "Market Trend": status_trend
                    })
                    idx += 1

                st.table(coin_list)

        with tab3:
            st.subheader("📰 Latest Crypto News & Updates")
            st.markdown("""
            * **1. Bitcoin Bull Run Continues:** Institutional investors are heavily accumulating BTC as market sentiment turns extremely positive.
            * **2. Ethereum Layer 2 Scaling:** Gas fees reach historical lows following major network upgrades this quarter.
            * **3. Solana DeFi Volume Surges:** Decentralized exchanges on Solana record massive daily transaction volumes.
            * **4. Global Crypto Regulations Evolve:** Major economies introduce clearer frameworks for digital asset trading.
            * **5. Web3 Gaming Growth:** New blockchain-based gaming ecosystems attract millions of active monthly users.
            """)

        st.divider()
        if st.button("🔄 දත්ත නැවුම් කරන්න (Refresh)"):
            st.rerun()

    else:
        st.error("⚠️ වැරදි Access Key එකක්! කරුණාකර නිවැරදි කී එකක් ලබා දෙන්න.")
else:
    st.info("ℹ️ කරුණාකර ඇතුළු වීමට ඉහත කොටුවට Access Key එකක් ලබා දෙන්න.")

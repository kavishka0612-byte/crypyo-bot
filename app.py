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

# උඩින් දිගට යන ප්‍රවෘත්ති/මාකට් විශේෂ නිව්ස් ටිකක් (Ticker)
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
        
        # සයිඩ්බාර් (Sidebar) හෝ ටැබ් හරහා මෙනු සැකසීම
        tab1, tab2, tab3 = st.tabs(["🏠 Home & Search", "📊 Market Coins", "📰 Latest News"])

        # Binance API මඟින් දත්ත ලබා ගැනීම
        try:
            url = "https://api.binance.com/api/v3/ticker/price"
            response = requests.get(url)
            all_coins = response.json() if response.status_code == 200 else []
        except:
            all_coins = []

        with tab1:
            st.subheader("🏠 Home - සර්ච් සහ ප්‍රධාන කොයින් මිල ගණන්")
            
            # සර්ච් බාර් එක (Search Bar)
            search_query = st.text_input("🔍 කොයින් එකක් සර්ච් කරන්න (උදා: BTC, ETH, SOL, ADA):", "").upper()

            if search_query and all_coins:
                filtered_coins = [c for c in all_coins if search_query in c['symbol']]
                if filtered_coins:
                    st.write(f"සැලකිය යුතු ප්‍රතිඵල ({len(filtered_coins)}):")
                    for coin in filtered_coins[:10]: # මුල් ප්‍රතිඵල 10ක් පෙන්වීම
                        st.info(f"🪙 **{coin['symbol']}** : ${float(coin['price']):,.4f}")
                else:
                    st.warning("අදාළ නමින් කොයින් එකක් හමු නොවීය.")
            
            st.divider()
            st.markdown("### ප්‍රධාන ජනප්‍රිය කොයින්")
            if all_coins:
                col1, col2, col3 = st.columns(3)
                target_coins = {'BTCUSDT': 'Bitcoin (BTC)', 'ETHUSDT': 'Ethereum (ETH)', 'SOLUSDT': 'Solana (SOL)'}
                
                cols = [col1, col2, col3]
                i = 0
                for coin in all_coins:
                    if coin['symbol'] in target_coins and i < 3:
                        with cols[i]:
                            st.metric(label=target_coins[coin['symbol']], value=f"${float(coin['price']):,.2f}")
                        i += 1

        with tab2:
            st.subheader("📊 Market Coins - සම්පූර්ණ වෙළඳපොළ ලැයිස්තුව")
            st.write("වෙළඳපොළේ පවතින ප්‍රධාන ටෝකන සහ ඒවායේ වත්මන් මිල ගණන්:")
            
            if all_coins:
                # දත්ත ලැයිස්තුවක් ලෙස පෙන්වීම
                market_data = []
                for c in all_coins[:20]: # මුල් කොයින් 20 පෙන්වන්න
                    market_data.append({"Symbol": c['symbol'], "Price (USD)": f"${float(c['price']):,.4f}"})
                st.table(market_data)

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
        if st.button("🔄 සියලු දත්ත නැවුම් කරන්න (Refresh)"):
            st.rerun()

    else:
        st.error("⚠️ වැරදි Access Key එකක්! කරුණාකර නිවැරදි කී එකක් ලබා දෙන්න.")
else:
    st.info("ℹ️ කරුණාකර ඇතුළු වීමට ඉහත කොටුවට Access Key එකක් ලබා දෙන්න.")

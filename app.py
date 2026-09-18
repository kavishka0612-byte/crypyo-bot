import streamlit as st
import requests

# පිටුවේ මූලික සැකසුම්
st.set_page_config(page_title="Crypto Price Tracker", page_icon="🪙", layout="centered")

# රහස් කී එක (Secret Key)
VALID_ACCESS_KEY = "my_secret_key_123"

st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🪙 Live Crypto Price Tracker")
st.write("මෙම වෙබ් අඩවිය භාවිතා කිරීමට කරුණාකර ඔබගේ ප්‍රවේශ කී (Access Key) ඇතුළත් කරන්න.")

user_key = st.text_input("Access Key ඇතුළත් කරන්න:", type="password")

if user_key:
    if user_key == VALID_ACCESS_KEY:
        st.success("සාර්ථකයි! ඔබට දැන් දත්ත බලාගත හැක.")
        
        st.divider()
        st.subheader("📊 ජීවී (Live) ක්‍රිප්ටෝ මිල ගණන් (Binance)")

        try:
            # Binance API මඟින් මිල ගණන් ලබා ගැනීම (BTC, ETH, SOL)
            url = "https://api.binance.com/api/v3/ticker/price?symbols=[\"BTCUSDT\",\"ETHUSDT\",\"SOLUSDT\"]"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                prices = {}
                for item in data:
                    prices[item['symbol']] = float(item['price'])

                col1, col2, col3 = st.columns(3)
                
                with col1:
                    btc_price = prices.get('BTCUSDT', 'N/A')
                    st.metric(label="Bitcoin (BTC)", value=f"${btc_price:,.2f}" if isinstance(btc_price, (int, float)) else btc_price)
                
                with col2:
                    eth_price = prices.get('ETHUSDT', 'N/A')
                    st.metric(label="Ethereum (ETH)", value=f"${eth_price:,.2f}" if isinstance(eth_price, (int, float)) else eth_price)
                
                with col3:
                    sol_price = prices.get('SOLUSDT', 'N/A')
                    st.metric(label="Solana (SOL)", value=f"${sol_price:,.2f}" if isinstance(sol_price, (int, float)) else sol_price)
                
                if st.button("මිල ගණන් නැවත අලුත් කරන්න (Refresh)"):
                    st.rerun()
            else:
                st.error("දත්ත ලබාගැනීමේදී දෝෂයක් මතු විය.")
        except Exception as e:
            st.error(f"අන්තර්ජාල සම්බන්ධතාවය පරීක්ෂා කරන්න: {e}")

    else:
        st.error("⚠️ වැරදි Access Key එකක්! කරුණාකර නිවැරදි කී එකක් ලබා දෙන්න.")
else:
    st.info("ℹ️ කරුණාකර ඇතුළු වීමට ඉහත කොටුවට Access Key එකක් ලබා දෙන්න.")

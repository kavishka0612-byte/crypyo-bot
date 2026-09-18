import streamlit as st
import requests

# පිටුවේ මූලික සැකසුම්
st.set_page_config(page_title="Crypto Price Tracker", page_icon="🪙", layout="centered")

# රහස් කී එක (Secret Key) මෙතැනින් වෙනස් කරගත හැක
VALID_ACCESS_KEY = "my_secret_key_123"

# CSS මඟින් ස්වල්ප මෝස්තරයක් එකතු කිරීම
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

# පරිශීලකයාගෙන් Key එක ඉල්ලීම
user_key = st.text_input("Access Key ඇතුළත් කරන්න:", type="password")

# Key එක නිවැරදි දැයි පරික්ෂා කිරීම
if user_key:
    if user_key == VALID_ACCESS_KEY:
        st.success("සාර්ථකයි! ඔබට දැන් දත්ත බලාගත හැක.")
        
        st.divider()
        st.subheader("📊ජීවී (Live) ක්‍රිප්ටෝ මිල ගණන්")

        # API එක හරහා ක්‍රිප්ටෝ මිල ලබා ගැනීම (උදාහරණයක් ලෙස Bitcoin සහ Ethereum)
        try:
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    btc_price = data.get('bitcoin', {}).get('usd', 'N/A')
                    st.metric(label="Bitcoin (BTC)", value=f"${btc_price:,.2f}" if isinstance(btc_price, (int, float)) else btc_price)
                
                with col2:
                    eth_price = data.get('ethereum', {}).get('usd', 'N/A')
                    st.metric(label="Ethereum (ETH)", value=f"${eth_price:,.2f}" if isinstance(eth_price, (int, float)) else eth_price)
                
                with col3:
                    sol_price = data.get('solana', {}).get('usd', 'N/A')
                    st.metric(label="Solana (SOL)", value=f"${sol_price:,.2f}" if isinstance(sol_price, (int, float)) else sol_price)
                
                # දත්ත නැවුම් කිරීමට (Refresh) බටන් එකක්
                if st.button("මිල ගණන් නැවත අලුත් කරන්න (Refresh)"):
                    st.rerun()
            else:
                st.error("දත්ත ලබාගැනීමේදී දෝෂයක් මතු විය.")
        except Exception as e:
            st.error(11, f"අන්තර්ජාල සම්බන්ධතාවය පරීක්ෂා කරන්න: {e}")

    else:
        st.error("⚠️ වැරදි Access Key එකක්! කරුණාකර නිවැරදි කී එකක් ලබා දෙන්න.")
else:
    st.info("ℹ️ කරුණාකර ඇතුළු වීමට ඉහත කොටුවට Access Key එකක් ලබා දෙන්න.")

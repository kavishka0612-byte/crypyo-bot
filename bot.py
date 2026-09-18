import requests

TELEGRAM_TOKEN = "8807605834:AAHPG4tvXNSiSeCwRN0-rl_rX4uQaGkx_xQ"
CHAT_ID = "7786354971"

def get_crypto_prices():
    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
    message = "🚀 *Top Crypto Market Update* 🚀\n\n"
    
    try:
        print("බිනෑන්ස් වෙතින් ඩේටා ලබාගනිමින් පවතී...")
        for symbol in symbols:
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
            res = requests.get(url).json()
            price = float(res["price"])
            coin_name = symbol.replace("USDT", "")
            
            message += f"• **{coin_name}**: ${price:,.2f}\n"
            
        print("ଟෙලිග්‍රෑම් වෙත මැසේජ් එක යවමින් පවතී...")
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(telegram_url, json=payload)
        
        print(f"Telegram API Response: {response.text}")
        
        if response.status_code == 200:
            print("මැසේජ් එක සාර්ථකව යවන ලදී!")
        else:
            print(f"මැසේජ් යැවීමේ දෝෂයක්: {response.text}")
            
    except Exception as e:
        print(f"දෝෂයක් සිදු විය: {e}")

if __name__ == "__main__":
    get_crypto_prices()

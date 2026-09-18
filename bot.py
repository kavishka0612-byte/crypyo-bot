import os
import requests
import time

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

def send_telegram_message(chat_id, message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram යැවීමේ දෝෂයක් සිදු විය: {e}")

def get_top_coins():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 3,
        "page": 1,
        "sparkline": "false"
    }
    try:
        response = requests.get(url, params=params)
        coins = response.json()
        
        message = "🚀 *Top Crypto Market Update (GitHub)* 🚀\n\n"
        for coin in coins:
            name = coin["name"]
            symbol = coin["symbol"].upper()
            price = coin["current_price"]
            change = coin["price_change_percentage_24h"]
            
            change_emoji = "🟢" if change and change > 0 else "🔴"
            message += f"• **{name} ({symbol})**: ${price:,.2f} {change_emoji} ({change:,.2f}%)\n"
            
        return message
    except Exception as e:
        return "ဒත්ත ලබාගැනීමේ දෝෂයක් සිදු විය!"

if __name__ == "__main__":
    print("ಬොට් එක ක්‍රියාත්මක වේ...")
    # ඔබගේ චැට් අයිඩී එක හෝ ඔබ මීට පෙර මැසේජ් එවූ කෙනෙකුට යැවීමට මෙහි කෝඩ් එක වැදගත් වේ.
    # ඔබගේ Telegram username එකට හෝ Chat ID එකට යැවීම සඳහා පරීක්ෂා කරමු.

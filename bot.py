import requests
import time

TELEGRAM_TOKEN = "8807605834:AAHPG4tvXNSiSeCwRN0-rl_rX4uQaGkx_xQ"

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
        print("දෝෂයක්:", e)

def get_top_coins():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": "false"
    }
    try:
        response = requests.get(url, params=params)
        coins = response.json()
        
        message = "📊 *Top 10 Crypto Market Update (On-Demand)*\n\n"
        for coin in coins:
            name = coin['name']
            symbol = coin['symbol'].upper()
            price = coin['current_price']
            change = coin['price_change_percentage_24h']
            
            change_emoji = "🟢" if change and change > 0 else "🔴"
            message += f"🪙 **{name} ({symbol})**: ${price:,.2f}  {change_emoji} ({change:.2f}%)\n"
            
        return message
    except Exception as e:
        return "දත්ත ලබාගැනීමේ දෝෂයක් සිදු විය!"

def check_telegram_updates(offset):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    params = {"offset": offset, "timeout": 30}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data.get("result", [])
    except Exception as e:
        print("Telegram පරීක්ෂා කිරීමේ දෝෂයක්:", e)
        return []

if __name__ == "__main__":
    print("ටෙලිග්‍රෑම් විධාන (Commands) බලා සිටින බොට් එක ක්‍රියාත්මක විය...")
    last_update_id = 0
    
    while True:
        updates = check_telegram_updates(last_update_id + 1)
        for update in updates:
            last_update_id = update["update_id"]
            
            if "message" in update and "text" in update["message"]:
                chat_id = update["message"]["chat"]["id"]
                text = update["message"]["text"]
                
                # පරිශීලකයා /top10 හෝ /start කමාන්ඩ් එක ගැහුවොත් පමණක් ක්‍රියාත්මක වේ
                if text.strip() in ["/top10", "/start"]:
                    print(f"විධානයක් ලැබුණි: {text} (Chat ID: {chat_id})")
                    market_data = get_top_coins()
                    send_telegram_message(chat_id, market_data)
                    
        time.sleep(2)

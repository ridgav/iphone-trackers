import requests
import time
import os

# Shopify product JSON
PRODUCT_URL = "https://www.imagineonline.store/products/iphone-15-mtp43hn-a.js"

# Telegram variables (from Railway environment variables)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Time interval in seconds
CHECK_INTERVAL = 60  # 1 minute

def send_telegram(message):
    """Send message to Telegram bot"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram send error:", e)

# Track last known stock status
last_status = None

if __name__ == "__main__":
    print("✅ iPhone 15 Tracker Started...")

    while True:
        try:
            response = requests.get(PRODUCT_URL)
            data = response.json()

            variant = data["variants"][0]
            available = variant["available"]
            price = variant["price"] / 100  # Convert paise to rupees

            # Send message every minute while in stock
            if available:
                send_telegram(f"✅ iPhone 15 is IN STOCK!\nPrice: ₹{price}")
            else:
                # Only send out-of-stock message once when status changes
                if last_status != False:
                    send_telegram("❌ iPhone 15 is OUT OF STOCK")

            last_status = available
            print(f"Checked stock | Available: {available} | Sleeping {CHECK_INTERVAL}s")
            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            print("Error:", e)
            time.sleep(30)

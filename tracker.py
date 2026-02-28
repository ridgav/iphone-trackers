import requests
import time
import os

PRODUCT_URL = "https://www.imagineonline.store/products/iphone-15-mtp43hn-a.js"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

last_status = None

while True:
    try:
        response = requests.get(PRODUCT_URL)
        data = response.json()

        variant = data["variants"][0]
        available = variant["available"]
        price = variant["price"] / 100

        if available != last_status:
            if available:
                send_telegram(f"✅ iPhone 15 is IN STOCK!\nPrice: ₹{price}")
            else:
                send_telegram("❌ iPhone 15 is OUT OF STOCK")

            last_status = available

        print("Checked...")
        time.sleep(300)

    except Exception as e:
        print("Error:", e)
        time.sleep(60)

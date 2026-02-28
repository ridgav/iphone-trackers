import requests
import time
import os

# Shopify JSON product pages (exact URLs)
PRODUCT_URLS = {
    "iPhone 15 128GB": [
        "https://www.imagineonline.store/products/iphone-15-mtp43hn-a.js",      # Blue
        "https://www.imagineonline.store/products/iphone-15-black-128gb.js",   # Black
        "https://www.imagineonline.store/products/iphone-15-pink-128gb.js",    # Pink
        "https://www.imagineonline.store/products/iphone-15-green-128gb.js",   # Green
        "https://www.imagineonline.store/products/iphone-15-yellow-128gb.js",  # Yellow
    ],
    "iPhone 16 128GB": [
        "https://www.imagineonline.store/products/iphone-16-white-128gb.js",       # White
        "https://www.imagineonline.store/products/iphone-16-black-128gb.js",       # Black
        "https://www.imagineonline.store/products/iphone-16-pink-128gb.js",        # Pink
        "https://www.imagineonline.store/products/iphone-16-ultramarine-128gb.js", # Ultramarine
        "https://www.imagineonline.store/products/iphone-16-teal-128gb.js",        # Teal
    ],
}

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHECK_INTERVAL = 60  # seconds (1 minute)

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram send error:", e)

if __name__ == "__main__":
    print("📡 Stock Tracker Started...")

    while True:
        alerts = []
        
        for model_name, urls in PRODUCT_URLS.items():
            for url in urls:
                try:
                    response = requests.get(url)
                    data = response.json()

                    # Check each colour variant inside the product
                    for variant in data.get("variants", []):
                        colour = variant.get("title", "")
                        available = variant.get("available", False)
                        price = variant.get("price", 0) / 100

                        if available:
                            alerts.append(f"{model_name} — {colour} is IN STOCK | ₹{price}")

                except Exception as e:
                    # If URL is wrong or JSON fetch fails, ignore
                    print(f"{model_name} URL fetch failed:", e)

        # Send Telegram alert only if something is in stock
        if alerts:
            message = "📢 Stock Alert – Imagine Online\n\n" + "\n".join(alerts)
            send_telegram(message)

        print("Checked, sleeping...")
        time.sleep(CHECK_INTERVAL)

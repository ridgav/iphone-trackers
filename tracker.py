import requests
import time
import os

# Shopify JSON product pages
PRODUCT_URLS = {
    "iPhone 15 128GB": [
        "https://www.imagineonline.store/products/iphone-15-mtp43hn-a.js",
        "https://www.imagineonline.store/products/iphone-15-128gb-black.js",
        "https://www.imagineonline.store/products/iphone-15-128gb-pink.js",
        "https://www.imagineonline.store/products/iphone-15-128gb-green.js",
        "https://www.imagineonline.store/products/iphone-15-128gb-yellow.js"
    ],
    "iPhone 16 128GB": [
        "https://www.imagineonline.store/products/iphone-16-myed3hn-a.js",
        "https://www.imagineonline.store/products/iphone-16-myea3hn-a.js",
        "https://www.imagineonline.store/products/iphone-16-black-128gb.js",
        "https://www.imagineonline.store/products/iphone-16-white-128gb.js",
        "https://www.imagineonline.store/products/iphone-16-ultramarine-128gb.js"
    ]
}

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHECK_INTERVAL = 60  # seconds (1 min)

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
        report_lines = []
        
        for model_name, urls in PRODUCT_URLS.items():
            for url in urls:
                try:
                    response = requests.get(url)
                    data = response.json()

                    # Loop through all variants for colour details
                    for variant in data.get("variants", []):
                        colour = variant.get("title", "")
                        available = variant.get("available", False)
                        price = variant.get("price", 0) / 100  # Convert paise to rupees
                        status = "✅ In Stock" if available else "❌ Out of Stock"
                        
                        report_lines.append(f"{model_name} — {colour}: {status} | ₹{price}")

                except Exception as e:
                    report_lines.append(f"{model_name} — {url.split('/')[-1]}: ❌ Error fetching")

        # Build and send the Telegram message
        message = "📢 Stock Update – Imagine Online\n\n" + "\n".join(report_lines)
        send_telegram(message)

        print("Checked, sleeping...")
        time.sleep(CHECK_INTERVAL)

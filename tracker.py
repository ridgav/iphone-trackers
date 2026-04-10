import requests
import time
import os

# Shopify JSON product pages (exact URLs)
PRODUCT_URLS = {
    "iPhone 15 128GB": [
        "https://www.amazon.in/OnePlus-Snapdragon-Segments-Complete-Personalized/dp/B0GRB5C1HW/ref=mp_s_a_1_1?crid=1T231NYT445SI&dib=eyJ2IjoiMSJ9.VlVSKFTUbuyegYiCNmBQw8LJGVI1vFGHQCUDD8DmL7Fkmf1a80uEEW4Z7XLqe1jCFRE0p--jLD2iv4ZThZiVDFCSCQrGr1s_jtZwRpHzcPCaymJouh7bDPWna5yyDIziEy-Ld2AqOBwG482YcTcU14VoZ6AlI6544n9Iod8XmX-2TkjkfIoWfab_g43SXtlicClFThCPkrsNvVZ2R4RzHg.hAXRvNh79DrONEPDe3zNopkkJXoib_vz0hvt86OUa5A&dib_tag=se&keywords=nord+6&qid=1775824904&sprefix=nord+%2Caps%2C420&sr=8-1.js",   # Black
        "https://www.imagineonline.store/products/iphone-15-pink-128gb.js",    # Pink
        "https://www.imagineonline.store/products/iphone-15-green-128gb.js",   # Green
        "https://www.imagineonline.store/products/iphone-15-yellow-128gb.js",  # Yellow
    ],
    "iPhone 16 128GB": [
        "https://www.amazon.in/OnePlus-Snapdragon-Segments-Complete-Personalized/dp/B0GRB5C1HW.js",       # White
        "https://www.imagineonline.store/products/iphone-16-mye73hn-a.js",       # Black
        "https://www.imagineonline.store/products/iphone-16-myea3hn-a.js",        # Pink
        "https://www.imagineonline.store/products/iphone-16-myec3hn-a.js", # Ultramarine
        "https://www.imagineonline.store/products/iphone-16-myed3hn-a.js",        # Teal
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

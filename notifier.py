
import time
import requests
from bs4 import BeautifulSoup
import os

PUSHBULLET_API_KEY = os.environ.get("PUSHBULLET_API_KEY")
PRODUCT_URL = "https://m.popmart.com/us/pop-now/set/195"

def is_labubu_available():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(PRODUCT_URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return "Add to Cart" in response.text or "In Stock" in response.text

def send_push_notification():
    data = {
        "type": "note",
        "title": "Labubu available!",
        "body": f"Check: {PRODUCT_URL}"
    }
    headers = {
        "Access-Token": PUSHBULLET_API_KEY,
        "Content-Type": "application/json"
    }
    requests.post("https://api.pushbullet.com/v2/pushes", json=data, headers=headers)

if __name__ == "__main__":
    while True:
        print("Checking Labubu availability...")
        try:
            if is_labubu_available():
                print("Labubu is available! Sending notification...")
                send_push_notification()
            else:
                print("Still not available.")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(180)  # 3 minutos

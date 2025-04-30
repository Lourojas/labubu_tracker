import requests
from bs4 import BeautifulSoup
from pushbullet import Pushbullet
import os

def notify():
    url = "https://m.popmart.com/us/pop-now/set/195"
    api_key = os.getenv("PUSHBULLET_API_KEY")  # ya lo tienes en Render

    keywords = ["Buy Multiple Boxes", "Pick One to Shake"]

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text()

        if any(keyword in page_text for keyword in keywords):
            pb = Pushbullet(api_key)
            pb.push_note("¡Labubu disponible!", f"{url}")
            print("✅ Notificación enviada")
        else:
            print("❌ Aún no disponible")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    notify()

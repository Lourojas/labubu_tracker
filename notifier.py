from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pushbullet import Pushbullet
import os
import time

def notify():
    url = "https://m.popmart.com/us/pop-now/set/195"
    api_key = os.getenv("PUSHBULLET_API_KEY")
    keywords = ["Buy Multiple Boxes", "Pick One to Shake"]

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        print("🌐 Abriendo URL...")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(6)  # Esperar a que cargue el contenido dinámico

        page_text = driver.page_source
        print("📄 Contenido cargado:", page_text[:500])  # Muestra los primeros 500 caracteres

        if any(keyword in page_text for keyword in keywords):
            pb = Pushbullet(api_key)
            pb.push_note("¡Labubu disponible!", f"{url}")
            print("✅ Notificación enviada")
        else:
            print("❌ Aún no disponible")

        driver.quit()

    except Exception as e:
        print("⚠️ Error:", e)

if __name__ == "__main__":
    notify()

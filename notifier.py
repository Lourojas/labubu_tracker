from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pushbullet import Pushbullet
import os
import time
import sys

# Redirige todos los print al archivo temporal de logs
sys.stdout = open('/tmp/log.txt', 'a')

def notify():
    url = "https://m.popmart.com/us/pop-now/set/195"
    api_key = os.getenv("PUSHBULLET_API_KEY")
    keywords = ["Buy Multiple Boxes", "Pick One to Shake"]

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(6)  # Espera para que se cargue el contenido dinámico

        page_text = driver.page_source

        if any(keyword in page_text for keyword in keywords):
            pb = Pushbullet(api_key)
            pb.push_note("¡Labubu disponible!", f"{url}")
            print("✅ Notificación enviada")
        else:
            print("❌ Aún no disponible")

        driver.quit()

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    notify()

# Cierra el archivo de log
sys.stdout.close()

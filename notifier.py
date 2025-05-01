from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pushbullet import Pushbullet
import os
import time
import chromedriver_autoinstaller

def notify():
    url = "https://m.popmart.com/us/pop-now/set/195"
    api_key = os.getenv("PUSHBULLET_API_KEY")
    chrome_path = os.getenv("CHROMEDRIVER_PATH")

    keywords = ["Buy Multiple Boxes", "Pick One to Shake"]

    # Instala automáticamente el chromedriver compatible
    chromedriver_autoinstaller.install()

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(executable_path=chrome_path, options=options)
        driver.get(url)
        time.sleep(6)  # Espera para que cargue el contenido dinámico
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

import requests
import os

PUSHBULLET_API_KEY = os.environ.get("PUSHBULLET_API_KEY")
PRODUCT_URL = "https://m.popmart.com/us/pop-now/set/195"

def send_push_notification():
    data = {
        "type": "note",
        "title": "¡Labubu disponible!",
        "body": f"Check: {PRODUCT_URL}"
    }
    headers = {
        "Access-Token": PUSHBULLET_API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post("https://api.pushbullet.com/v2/pushes", json=data, headers=headers)
    print("Notificación enviada." if response.ok else f"Fallo al enviar notificación: {response.text}")

if __name__ == "__main__":
    print("Forzando envío de notificación para pruebas...")
    send_push_notification()

import requests, json, pytz
from datetime import datetime

CONFIG_PATH = "beehive_config.json"
SERVER_URL = "http://localhost:5000"
santiago_tz = pytz.timezone("America/Santiago")

def send_readings():
    with open(CONFIG_PATH) as f:
        config = json.load(f)

    payload = {
        "hora": str(datetime.now(santiago_tz).strftime("%H:%M:%S")),
        "temperatura": 34.7,
        "humedad": 62,
        "peso": 12.1,
    }

    response = requests.put(f"{SERVER_URL}/sensores/actualizar-sensores/{config["colmena_id"]}", json=payload)
    if response.status_code == 200:
        print(response.json()["message"])
    elif response.status_code == 404:
        print(response.json()["message"])
    elif response.status_code == 500:
        print(response.json()["message"])
    
if __name__ == "__main__":
    send_readings()
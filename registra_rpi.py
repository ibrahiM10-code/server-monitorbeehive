from datetime import datetime
import requests, json, os, pytz, hashlib

CONFIG_PATH = "beehive_config.json"
santiago_tz = pytz.timezone("America/Santiago")
SERVER_URL = "http://localhost:5000"

def register_pi():
    now = datetime.now(santiago_tz).strftime("%Y%m%d_%H%M%S")
    hash_corto = hashlib.sha1(now.encode()).hexdigest()[:6]
    device_serial = f"RPi_{hash_corto}"
    print(device_serial)
    payload = {
        "device_serial": device_serial,
    }

    response = requests.post(f"{SERVER_URL}/rpi/registrar-placa", json=payload)
    if response.status_code == 201:
        colmena_id = response.json()["colmena_id"]
        config = {
            "colmena_id": colmena_id,
            "device_serial": device_serial,
            "registered_at": datetime.now(santiago_tz).strftime("%d-%m-%Y")
        }
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)
    elif response.status_code == 200:
        print(response.json()["message"])
    elif response.status_code == 409:
        print(response.json()["message"])

if __name__ == "__main__":
    if not os.path.exists(CONFIG_PATH):
        register_pi()
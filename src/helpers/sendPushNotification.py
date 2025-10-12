import requests

def send_push_notification(to, title, body, data=None):
    if not to or not title or not body:
        print('Missing required push notification fields')
        return None
    print(f"To: {to}, Titulo: {title}, Body: {body}")
    message = {
        "to": to,  # Expo push token
        "sound": "default",
        "title": title,
        "body": body,
    }

    try:
        response = requests.post(
            "https://exp.host/--/api/v2/push/send",
            headers={
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate",
                "Content-Type": "application/json"
            },
            json=message
        )
        result = response.json()
        print("Push notification result:", result)
        return result
    except Exception as error:
        print("Error sending push notification:", error)
        return None
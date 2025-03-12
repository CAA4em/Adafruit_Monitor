import paho.mqtt.client as mqtt
import requests
import os
# Gotify settings
GOTIFY_URL = "https://<https://gotify-t4xq.onrender.com/#/>/message"  # Replace with your Gotify URL
GOTIFY_TOKEN = "<AyNtgk3uP2l9sJw>"  # Replace with your Gotify app token

# Adafruit IO settings
IO_USERNAME = "<CAACONGO>"  # Replace with your Adafruit IO username
IO_KEY = "<IO_KEY = os.getenv("ADAFRUIT_IO_KEY")>"  # Replace with your Adafruit IO key
FEED_NAME = "<4em-ac-in-1>"  # Replace with the name of the feed you want to monitor
ALERT_THRESHOLD = 50  # Set your alert threshold (e.g., notify if value > 50)

# Function to send a push notification via Gotify
def send_gotify_notification(title, message, priority=5):
    url = GOTIFY_URL
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "title": title,
        "message": message,
        "priority": priority
    }
    params = {
        "token": GOTIFY_TOKEN
    }
    response = requests.post(url, json=data, headers=headers, params=params)
    if response.status_code == 200:
        print("Notification sent successfully!")
    else:
        print(f"Failed to send notification. Status code: {response.status_code}")

# MQTT callback when a message is received
def on_message(client, userdata, message):
    try:
        value = float(message.payload.decode())
        print(f"Received value: {value}")
        
        # Check if the value exceeds the alert threshold
        if value > ALERT_THRESHOLD:
            alert_message = f"ALERT: Feed '{FEED_NAME}' value is {value} (threshold: {ALERT_THRESHOLD})"
            send_gotify_notification("Adafruit Alert", alert_message)
    except ValueError:
        print("Received non-numeric value.")

# Set up MQTT client
client = mqtt.Client()
client.username_pw_set(IO_USERNAME, IO_KEY)
client.on_message = on_message

# Connect to Adafruit IO
client.connect("io.adafruit.com", 1883, 60)
client.subscribe(f"{IO_USERNAME}/feeds/{FEED_NAME}")

# Start listening
print(f"Monitoring feed '{FEED_NAME}' for alerts...")
client.loop_forever()



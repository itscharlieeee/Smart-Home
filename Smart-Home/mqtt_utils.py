import os
import ssl
import json
import paho.mqtt.client as mqtt

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

TOPIC_STATUS = "smarthome/status"
TOPIC_CONTROL = "smarthome/control"

# ---- Conexión ----
def connect_mqtt():
    client = mqtt.Client()

    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    
    client.tls_set()
    client.tls_insecure_set(True)

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    return client

# ---- Publicar comandos ----
def publish_message(message: str):
    client = connect_mqtt()
    client.publish(TOPIC_CONTROL, message)
    client.disconnect()

# ---- Leer sensores (Dashboard) ----
def get_sensor_data():
    """
    Devuelve un diccionario con los sensores:
    {"temp": 22, "humedad": 50, "luz": 400}
    """
    data = {}

    def on_message(client, userdata, msg):
        nonlocal data
        try:
            data = json.loads(msg.payload.decode())
        except:
            data = {}

    client = connect_mqtt()
    client.subscribe(TOPIC_STATUS)
    client.on_message = on_message

    client.loop(timeout=2.0)
    client.loop_stop()
    client.disconnect()

    return data

    client.tls_set()
    client.tls_insecure_set(True)

    try:
        client.connect(MQTT_BROKER, MQTT_PORT)
        print("Conectado a MQTT")
    except Exception as e:
        print("Error al conectar:", e)

    return client


mqtt_client = None

def init_mqtt():
    global mqtt_client
    if mqtt_client is None:
        mqtt_client = connect_mqtt()

def get_status():
    init_mqtt()
    return last_message["status"]

def send_command(command):
    init_mqtt()
    mqtt_client.publish(TOPIC_CONTROL, command)

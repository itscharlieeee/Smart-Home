# mqtt_utils.py
import paho.mqtt.client as mqtt
import ssl

# Variables globales donde guardamos datos
SENSORES = {}
DISPOSITIVOS = {}

BROKER = "fe16ebafff14607be01bf00bd32f334.s1.eu.hivemq.cloud"
PORT = 8883
USERNAME = "marivs912"
PASSWORD = "Nanisdciembre9*"


# ---------------------------
#  CALLBACKS
# ---------------------------
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Conectado al broker MQTT")
        client.subscribe("casa/#")
    else:
        print("❌ Error al conectar:", rc)


def on_message(client, userdata, msg):
    global SENSORES, DISPOSITIVOS
    
    topic = msg.topic
    payload = msg.payload.decode()

    if topic.startswith("casa/sensores/"):
        nombre = topic.split("/")[-1]
        SENSORES[nombre] = payload
    else:
        DISPOSITIVOS[topic] = payload


# ---------------------------
#   CONECTAR
# ---------------------------
def connect_mqtt():
    client = mqtt.Client()

    client.tls_set(cert_reqs=ssl.CERT_NONE)
    client.tls_insecure_set(True)

    client.username_pw_set(USERNAME, PASSWORD)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT)
    client.loop_start()

    return client


# ---------------------------
#     PUBLICAR
# ---------------------------
def publish_message(topic, payload):
    DISPOSITIVOS[topic] = payload
    client = mqtt.Client()
    client.username_pw_set(USERNAME, PASSWORD)
    client.tls_set(cert_reqs=ssl.CERT_NONE)
    client.tls_insecure_set(True)
    client.connect(BROKER, PORT)
    client.publish(topic, payload)
    client.disconnect()


# ---------------------------
#   OBTENER DATOS
# ---------------------------
def get_sensor_data(sensor):
    return SENSORES.get(sensor, "N/A")


def get_device_status(topic):
    return DISPOSITIVOS.get(topic, "OFF")

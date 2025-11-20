# mqtt_utils.py
import paho.mqtt.client as mqtt
import ssl
import streamlit as st

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
        client.subscribe("casa/#")  # nos suscribimos a todo
    else:
        print("❌ Error al conectar:", rc)


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()

    # Sensores
    if topic.startswith("casa/sensores/"):
        st.session_state.setdefault("sensores", {})
        nombre = topic.split("/")[-1]
        st.session_state["sensores"][nombre] = payload

    # Dispositivos
    else:
        st.session_state.setdefault("dispositivos", {})
        st.session_state["dispositivos"][topic] = payload


# ---------------------------
#   CONECTAR MQTT (SEGURO Y ESTABLE)
# ---------------------------
def connect_mqtt():
    if "mqtt_client" in st.session_state:
        return st.session_state.mqtt_client

    client = mqtt.Client()

    # seguridad TLS obligatoria para HiveMQ Cloud
    client.tls_set(cert_reqs=ssl.CERT_NONE)
    client.tls_insecure_set(True)

    client.username_pw_set(USERNAME, PASSWORD)

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(BROKER, PORT)
        client.loop_start()
    except Exception as e:
        print("⚠ No se pudo conectar al broker:", e)

    st.session_state.mqtt_client = client
    return client


# ---------------------------
#     PUBLICAR
# ---------------------------
def publish_message(topic, payload):
    client = st.session_state.get("mqtt_client")
    if client:
        client.publish(topic, payload)

    # Actualizar estado local
    st.session_state.setdefault("dispositivos", {})
    st.session_state["dispositivos"][topic] = payload


# ---------------------------
#   OBTENER DATOS
# ---------------------------
def get_sensor_data(sensor):
    return st.session_state.get("sensores", {}).get(sensor, "N/A")


def get_device_status(topic):
    return st.session_state.get("dispositivos", {}).get(topic, "OFF")


import paho.mqtt.client as mqtt
import ssl
import streamlit as st
from collections import deque

# Inicializar variables en session_state
if "mqtt_client" not in st.session_state:
    st.session_state.mqtt_client = None
if "device_status" not in st.session_state:
    st.session_state.device_status = {}
if "sensor_data" not in st.session_state:
    st.session_state.sensor_data = {
        "casa/sensores/temperatura": deque(maxlen=50),
        "casa/sensores/luminosidad": deque(maxlen=50)
    }

# Callbacks MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT exitosamente.")
        client.subscribe("casa/luces/#")
        client.subscribe("casa/enchufe/#")
        client.subscribe("casa/ventanas")
        client.subscribe("casa/sensores/#")
    else:
        print(f"Error al conectar, código: {rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    topic = msg.topic

    # Guardar estado de dispositivos
    if topic.startswith("casa/luces/") or topic.startswith("casa/enchufe/") or topic.startswith("casa/ventanas"):
        st.session_state.device_status[topic] = payload

    # Guardar datos de sensores
    if topic in st.session_state.sensor_data:
        st.session_state.sensor_data[topic].append(f"{topic}: {payload}")

# Conexión segura MQTT
def connect_mqtt(broker="TU_BROKER", port=8883, username=None, password=None):
    if st.session_state.mqtt_client is None:
        client = mqtt.Client()
        client.tls_set(cert_reqs=ssl.CERT_NONE)

        if username and password:
            client.username_pw_set(username, password)

        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(broker, port)
        client.loop_start()

        st.session_state.mqtt_client = client

    return st.session_state.mqtt_client

# Función para publicar mensajes
def publish_message(topic, payload):
    client = st.session_state.get("mqtt_client")
    if client:
        client.publish(topic, payload)

# Función para obtener estado de dispositivos
def get_device_status(topic):
    return st.session_state.device_status.get(topic, "off")

# Función para obtener datos de sensores
def get_sensor_data(topic):
    return list(st.session_state.sensor_data.get(topic, []))

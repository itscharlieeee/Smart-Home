# mqtt_utils.py
import paho.mqtt.client as mqtt
import ssl
import streamlit as st

# Callbacks MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT exitosamente.")
    else:
        print(f"Error al conectar, código: {rc}")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    # Guardamos estado de sensores y dispositivos en session_state
    if topic.startswith("casa/sensores/"):
        st.session_state["sensores"] = st.session_state.get("sensores", {})
        st.session_state["sensores"][topic.split("/")[-1]] = payload
    else:
        st.session_state["dispositivos"] = st.session_state.get("dispositivos", {})
        st.session_state["dispositivos"][topic] = payload

def connect_mqtt(broker="test.mosquitto.org", port=1883, username=None, password=None):
    if "mqtt_client" not in st.session_state:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        if username and password:
            client.username_pw_set(username, password)

        try:
            client.connect(broker, port)
            client.loop_start()
        except Exception as e:
            st.error(f"No se pudo conectar al broker MQTT: {e}")
        
        st.session_state.mqtt_client = client
    return st.session_state.mqtt_client

def publish_message(topic, payload):
    client = st.session_state.get("mqtt_client")
    if client:
        client.publish(topic, payload)
        # Guardamos el estado inmediatamente para reflejarlo en UI
        st.session_state["dispositivos"] = st.session_state.get("dispositivos", {})
        st.session_state["dispositivos"][topic] = payload

def subscribe(topic):
    client = st.session_state.get("mqtt_client")
    if client:
        client.subscribe(topic)

def get_sensor_data(sensor):
    return st.session_state.get("sensores", {}).get(sensor, "N/A")

def get_device_status(topic):
    return st.session_state.get("dispositivos", {}).get(topic, "OFF")

import paho.mqtt.client as mqtt
import json
import streamlit as st

# ------------ CONFIG PERSONAL DE CARLOS ------------
BROKER = "broker.hivemq.com"
PORT = 1883
CLIENT_ID = "streamlit_carlos_app"          # CLIENT ID ÚNICO
TOPIC_SUBSCRIBE = "carloshome/#"            # TU TOPIC PRIVADO
# ---------------------------------------------------

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("MQTT: Conectado")
        client.subscribe(TOPIC_SUBSCRIBE)
        st.session_state['mqtt_connected'] = True
    else:
        print("MQTT: Error de conexión")
        st.session_state['mqtt_connected'] = False

def on_message(client, userdata, msg):
    try:
        sensor_name = msg.topic.split("/")[-1]
        try:
            payload = json.loads(msg.payload.decode())
        except:
            payload = msg.payload.decode()

        st.session_state['sensores'][sensor_name] = payload
    except Exception as e:
        print(f"Error MQTT: {e}")

@st.cache_resource
def connect_mqtt():
    try:
        client = mqtt.Client(client_id=CLIENT_ID, clean_session=True)
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(BROKER, PORT, 60)
        client.loop_start()

        st.session_state['mqtt_client'] = client
        st.session_state['mqtt_connected'] = False

        return True
    except Exception as e:
        print(f"MQTT Error: {e}")
        return False

def get_sensor_data(sensor_name):
    return st.session_state['sensores'].get(sensor_name, "Esperando...")

def send_mqtt_command(topic, command):
    client = st.session_state.get("mqtt_client")
    if client is None:
        return {"error": "Cliente MQTT no inicializado"}

    try:
        payload = json.dumps(command)
        client.publish(topic, payload)
        return True
    except Exception as e:
        return {"error": str(e)}

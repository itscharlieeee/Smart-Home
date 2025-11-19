import paho.mqtt.client as mqtt
import ssl

# -----------------------------
# CONFIGURACIÓN MQTT FIJA
# -----------------------------
MQTT_BROKER = "tu_broker.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "tu_usuario"
MQTT_PASSWORD = "tu_password"

TOPIC_SENSORES = "casa/sensores/#"
TOPIC_CONTROL = "casa/control"

# Diccionario donde guardaremos los datos recibidos
sensor_data = {
    "temp": None,
    "humedad": None,
    "luz": None
}

client = mqtt.Client(protocol=mqtt.MQTTv311)


# -----------------------------
# CALLBACKS MQTT
# -----------------------------
def on_connect(client, userdata, flags, rc):
    print("Conectado con código:", rc)
    if rc == 0:
        client.subscribe(TOPIC_SENSORES)
    else:
        print("Error en conexión MQTT:", rc)


def on_message(client, userdata, msg):
    global sensor_data
    topic = msg.topic
    payload = msg.payload.decode()

    if "temperatura" in topic:
        sensor_data["temp"] = payload

    elif "humedad" in topic:
        sensor_data["humedad"] = payload

    elif "luz" in topic:
        sensor_data["luz"] = payload


# -----------------------------
# INICIAR MQTT
# -----------------------------
def connect_mqtt():
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

    client.tls_set(cert_reqs=ssl.CERT_NONE)
    client.tls_insecure_set(True)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()


# -----------------------------
# ENVIAR MENSAJE
# -----------------------------
def publish_message(message):
    client.publish(TOPIC_CONTROL, message)


# -----------------------------
# OBTENER DATOS
# -----------------------------
def get_sensor_data():
    return sensor_data

if "mqtt_started" not in st.session_state:
    connect_mqtt()
    st.session_state.mqtt_started = True


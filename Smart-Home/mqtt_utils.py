import paho.mqtt.client as mqtt
import json
import time
import streamlit as st

# --- CONFIGURACIÓN GLOBAL Y ESTADO ---
# Usamos st.session_state para mantener el cliente MQTT y los datos a través de los reruns de Streamlit.

# Definir las constantes de conexión (Asegúrate de cambiar esto por tus valores reales)
BROKER = "broker.hivemq.com" # Broker público de ejemplo
PORT = 1883
CLIENT_ID = "streamlit_smart_home_app"
TOPIC_SUBSCRIBE = "smartmec-home/#" # Suscripción a todos los tópicos bajo smart-home

# --- CALLBACKS MQTT ---

def on_connect(client, userdata, flags, rc):
    """Callback que se llama cuando el cliente recibe una respuesta de conexión del broker."""
    if rc == 0:
        print("MQTT: Conexión exitosa al broker.")
        client.subscribe(TOPIC_SUBSCRIBE)
        # Puedes usar st.session_state si estás en el contexto de Streamlit:
        if 'mqtt_connected' in st.session_state:
            st.session_state['mqtt_connected'] = True
    else:
        print(f"MQTT: Fallo al conectar, código {rc}")
        if 'mqtt_connected' in st.session_state:
            st.session_state['mqtt_connected'] = False

def on_message(client, userdata, msg):
    """Callback que se llama cuando se recibe un mensaje del broker."""
    try:
        topic_parts = msg.topic.split('/')
        # El nombre del sensor será la última parte del tópico
        sensor_name = topic_parts[-1] 
        
        # Intentar parsear el payload como JSON
        try:
            payload = json.loads(msg.payload.decode())
        except json.JSONDecodeError:
            payload = msg.payload.decode() # Si no es JSON, es una cadena simple

        # Guardar el dato en el estado de sesión de Streamlit
        if 'sensores' in st.session_state:
            st.session_state['sensores'][sensor_name] = payload
            # Imprimir para depuración (visible en la consola de Streamlit)
            # print(f"Dato recibido: {sensor_name} -> {payload}")
            
    except Exception as e:
        print(f"MQTT Error al procesar mensaje: {e}")

# --- FUNCIONES REQUERIDAS POR homestatus.py ---

# Usamos st.cache_resource para asegurar que el cliente MQTT se inicialice solo una vez, 
# incluso a través de múltiples reruns de Streamlit.
@st.cache_resource
def connect_mqtt():
    """Inicializa y conecta el cliente MQTT de forma persistente."""
    try:
        client = mqtt.Client(client_id=CLIENT_ID, clean_session=True)
        client.on_connect = on_connect
        client.on_message = on_message
        
        client.connect(BROKER, PORT, 60)
        client.loop_start() # Ejecutar el bucle de red en segundo plano
        
        st.session_state['mqtt_client'] = client
        st.session_state['mqtt_connected'] = False # Estado inicial, se actualiza en on_connect
        
        return True
    except Exception as e:
        print(f"Error al iniciar conexión MQTT: {e}")
        return False

def get_sensor_data(sensor_name):
    """
    Devuelve el último valor conocido del sensor desde st.session_state.
    En este modelo, los datos se actualizan automáticamente en on_message.
    """
    # Inicializar sensores en session_state si no existe
    if 'sensores' not in st.session_state:
         st.session_state['sensores'] = {}
         
    return st.session_state['sensores'].get(sensor_name, "Esperando...")

# --- FUNCIÓN DE COMANDO (Basada en tu función original, pero sin crear un cliente nuevo) ---

def send_mqtt_command(topic, command):
    """Función para enviar comando MQTT (actuadores) usando el cliente cacheado."""
    client = st.session_state.get('mqtt_client')
    if not client:
        return {"error": "Cliente MQTT no inicializado."}
        
    try:
        payload = json.dumps(command)
        # Publicar el comando
        client.publish(topic, payload)
        return True
    except Exception as e:
        return {"error": str(e)}
    
    client.loop_stop()
    client.disconnect()
    return message_received["payload"]

except Exception as e:
    return {"error": str(e)}
```

def send_mqtt_command(broker, port, topic, client_id, command):
"""Función para enviar comando MQTT (actuadores)"""
try:
    client = mqtt.Client(client_id=client_id)
    client.connect(broker, port, 60)
    client.loop_start()
    payload = json.dumps(command)
    client.publish(topic, payload)
    client.loop_stop()client.disconnect()
return True
except Exception as e:
return {"error": str(e)}

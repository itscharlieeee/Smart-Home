import streamlit as st
# Importamos directamente ya que están en la misma carpeta raíz
from mqtt_utils import connect_mqtt

st.set_page_config(page_title="Smart-Home", page_icon="🏠", layout="centered")

# --- INICIALIZACIÓN DE ESTADO ---
if 'sensores' not in st.session_state:
    st.session_state['sensores'] = {
        "Temp": 0, "Hum": 0, "Gas": 0, "Luminosidad": 0
    }

# Conectar al iniciar la app principal
connect_mqtt()

st.title("Smart Home Dashboard 🏠")

st.write("### Bienvenido al panel de control")
st.info("Navega usando el menú de la izquierda para ver el Estado o controlar dispositivos.")

# Sidebar Informativo
with st.sidebar:
    st.subheader("📡 Estado de Conexión")
    if st.session_state.get('mqtt_connected'):
        st.success("Conectado a HiveMQ")
    else:
        st.warning("Desconectado / Conectando...")
        
    st.markdown("---")
    st.caption("Broker: broker.hivemq.com")
    st.caption("Topic Sensores: smart-home/sensores")

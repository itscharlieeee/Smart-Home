import streamlit as st
from mqtt_utils import connect_mqtt

st.set_page_config(page_title="Smart-Home", page_icon="🏠", layout="centered")

# Estado inicial
if 'sensores' not in st.session_state:
    st.session_state['sensores'] = {
        "Temp": 0,
        "Hum": 0,
        "Gas": 0,
        "Luminosidad": 0
    }

connect_mqtt()

st.title("Smart Home Dashboard 🏠")
st.write("### Bienvenido a tu panel personalizado")
st.info("Usa el menú lateral para ver el estado o enviar comandos.")

with st.sidebar:
    st.subheader("📡 Estado de Conexión")
    if st.session_state.get("mqtt_connected"):
        st.success("Conectado ✔")
    else:
        st.warning("Desconectado…")

    st.markdown("---")
    st.caption("Broker: broker.hivemq.com")
    st.caption("Topic Sensores: carloshome/sensores")

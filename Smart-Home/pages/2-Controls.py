# pages/controls.py
import streamlit as st
from mqtt_utils import publish_message, get_device_status

st.header("Controles de la Casa")

modo = st.radio("Modo de control:", ["Botones", "Texto", "Voz"])

dispositivos = ["casa/luz/sala", "casa/luz/habitacion", "casa/enchufe/televisor", "casa/enchufe/lampara"]

for dev in dispositivos:
    estado = get_device_status(dev)
    col1, col2 = st.columns([2,1])
    with col1:
        st.write(f"{dev.split('/')[-1].capitalize()}: {estado}")
    with col2:
        if st.button("ON", key=f"{dev}_on", help="Encender", use_container_width=True):
            publish_message(dev, "ON")
        if st.button("OFF", key=f"{dev}_off", help="Apagar", use_container_width=True):
            publish_message(dev, "OFF")

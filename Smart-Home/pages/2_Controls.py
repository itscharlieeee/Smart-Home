import streamlit as st
from mqtt_utils import publish_message, connect_mqtt

# Conectar al broker si no lo está
connect_mqtt(broker="TU_BROKER", port=8883, username="TU_USUARIO", password="TU_PASSWORD")

st.header("Controles - Dispositivos")

# Luces
if st.button("Encender luz sala"):
    publish_message("casa/luz/sala", "ON")
if st.button("Apagar luz sala"):
    publish_message("casa/luz/sala", "OFF")

if st.button("Encender luz habitación"):
    publish_message("casa/luz/habitacion", "ON")
if st.button("Apagar luz habitación"):
    publish_message("casa/luz/habitacion", "OFF")

# Enchufes
if st.button("Encender enchufe televisor"):
    publish_message("casa/enchufe/televisor", "ON")
if st.button("Apagar enchufe televisor"):
    publish_message("casa/enchufe/televisor", "OFF")

if st.button("Encender enchufe lámpara"):
    publish_message("casa/enchufe/lampara", "ON")
if st.button("Apagar enchufe lámpara"):
    publish_message("casa/enchufe/lampara", "OFF")

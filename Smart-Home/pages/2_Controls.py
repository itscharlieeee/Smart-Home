import streamlit as st
from mqtt_utils import connect_mqtt, publish_message

st.header("Controles - Dispositivos")
connect_mqtt()

# Luces
if st.button("Encender luz sala"):
    publish_message("casa/luces/sala", "on")
    st.success("Mensaje enviado: luz sala ON")

if st.button("Apagar luz sala"):
    publish_message("casa/luces/sala", "off")
    st.success("Mensaje enviado: luz sala OFF")

if st.button("Encender luz habitación"):
    publish_message("casa/luces/habitacion", "on")
    st.success("Mensaje enviado: luz habitación ON")

if st.button("Apagar luz habitación"):
    publish_message("casa/luces/habitacion", "off")
    st.success("Mensaje enviado: luz habitación OFF")

# Enchufes
if st.button("Encender enchufe televisor"):
    publish_message("casa/enchufe/televisor", "on")
    st.success("Mensaje enviado: enchufe televisor ON")

if st.button("Apagar enchufe televisor"):
    publish_message("casa/enchufe/televisor", "off")
    st.success("Mensaje enviado: enchufe televisor OFF")

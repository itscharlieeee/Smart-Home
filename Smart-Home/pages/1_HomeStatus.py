import streamlit as st
from mqtt_utils import publish_message, connect_mqtt

st.header("Controles de la casa")

# Luces
st.subheader("Luces")
col1, col2 = st.columns(2)
with col1:
    if st.button("Encender sala"):
        publish_message("casa/luces/sala", "on")
    if st.button("Encender habitación"):
        publish_message("casa/luces/habitacion", "on")
with col2:
    if st.button("Apagar sala"):
        publish_message("casa/luces/sala", "off")
    if st.button("Apagar habitación"):
        publish_message("casa/luces/habitacion", "off")

# Enchufes
st.subheader("Enchufes")
col3, col4 = st.columns(2)
with col3:
    if st.button("Encender televisor"):
        publish_message("casa/enchufe/televisor", "on")
with col4:
    if st.button("Apagar televisor"):
        publish_message("casa/enchufe/televisor", "off")

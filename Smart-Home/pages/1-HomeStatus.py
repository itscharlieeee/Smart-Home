# pages/home_status.py
import streamlit as st
from mqtt_utils import get_sensor_data, get_device_status, publish_message

st.header("Estado de la Casa")

habitaciones = {
    "Sala": [
        "casa/luces/sala",
        "casa/enchufe/televisor"
    ],
    "Cocina": [
        "casa/luces/cocina"
    ],
    "Habitación": [
        "casa/luces/habitacion",
        "casa/enchufe/lampara"
    ]
}

for hab, dispositivos in habitaciones.items():
    with st.expander(hab):
        for dev in dispositivos:
            estado = get_device_status(dev)
            st.write(f"{dev.split('/')[-1].capitalize()}: {estado}")

            if st.button(f"Tog {dev}", key=f"{dev}_toggle"):
                nuevo_estado = "OFF" if estado == "ON" else "ON"
                publish_message(dev, nuevo_estado)

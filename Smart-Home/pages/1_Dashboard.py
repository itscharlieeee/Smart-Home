import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from mqtt_utils import get_sensor_data
import streamlit as st


st.title("📊 Dashboard de Sensores")

data = get_sensor_data()

col1, col2 = st.columns(2)

with col1:
    st.metric("Temperatura (°C)", data["temperature"])

with col2:
    st.metric("Luminosidad (lx)", data["light"])

st.write("---")
st.write("Los datos se actualizan automáticamente desde Wokwi mediante MQTT.")


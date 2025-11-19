import streamlit as st
from mqtt_utils import connect_mqtt, get_sensor_data
import pandas as pd

st.header("Dashboard - Sensores")
connect_mqtt()

temperatura_msgs = get_sensor_data("casa/sensores/temperatura")
luminosidad_msgs = get_sensor_data("casa/sensores/luminosidad")

# Convertir a números si vienen en string
temperatura = [int(msg.split(":")[-1]) for msg in temperatura_msgs[-10:]]
luminosidad = [int(msg.split(":")[-1]) for msg in luminosidad_msgs[-10:]]

st.subheader("Temperatura (°C)")
st.line_chart(pd.DataFrame(temperatura, columns=["Temperatura"]))

st.subheader("Luminosidad (lux)")
st.line_chart(pd.DataFrame(luminosidad, columns=["Luminosidad"]))

st.write("Últimos mensajes de sensores:")
for msg in temperatura_msgs[-5:] + luminosidad_msgs[-5:]:
    st.write(msg)

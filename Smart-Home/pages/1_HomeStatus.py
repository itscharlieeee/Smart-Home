import streamlit as st
import streamlit as st
from mqtt_utils import connect_mqtt, get_device_status, get_sensor_data

st.set_page_config(page_title="Smart-Home - Estado", page_icon="🏡")
st.title("Estado de tu casa inteligente")

# Conectar al broker si no está conectado
connect_mqtt()

st.subheader("Sensores de la casa")

# Obtener últimos valores de sensores
temperatura_msgs = get_sensor_data("casa/sensores/temperatura")[-1:]
luminosidad_msgs = get_sensor_data("casa/sensores/luminosidad")[-1:]

temperatura = int(temperatura_msgs[0].split(":")[-1]) if temperatura_msgs else "-"
luminosidad = int(luminosidad_msgs[0].split(":")[-1]) if luminosidad_msgs else "-"

col1, col2 = st.columns(2)
col1.metric("Temperatura (°C)", temperatura)
col2.metric("Luminosidad (lux)", luminosidad)

st.subheader("Estado de los dispositivos")

# Obtener estado de luces y enchufes
luces = {
    "Sala": get_device_status("casa/luces/sala"),
    "Habitación": get_device_status("casa/luces/habitacion"),
    "Cocina": get_device_status("casa/luces/cocina")
}

enchufes = {
    "Televisor": get_device_status("casa/enchufe/televisor"),
    "Lámpara": get_device_status("casa/enchufe/lampara")
}

ventanas = {
    "Ventana principal": get_device_status("casa/ventanas")  # valor del servo
}

st.write("### Luces")
for nombre, estado in luces.items():
    st.write(f"{nombre}: {'💡 Encendida' if estado=='on' else '🔌 Apagada'}")

st.write("### Enchufes")
for nombre, estado in enchufes.items():
    st.write(f"{nombre}: {'🔌 Encendido' if estado=='on' else '❌ Apagado'}")

st.write("### Ventanas")
for nombre, valor in ventanas.items():
    st.write(f"{nombre}: {valor}° abierto" if valor else "❌ Cerrada")

st.subheader("Últimos mensajes del broker")
ultimo_temp = temperatura_msgs[-5:] if temperatura_msgs else []
ultimo_luz = luminosidad_msgs[-5:] if luminosidad_msgs else []

for msg in ultimo_temp + ultimo_luz:
    st.write(msg)

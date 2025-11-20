import streamlit as st
import sys
import os
import time

# --- IMPORTACIÓN ROBUSTA DE MQTT_UTILS ---
try:
    from mqtt_utils import get_sensor_data, connect_mqtt
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    try:
        from mqtt_utils import get_sensor_data, connect_mqtt
    except Exception as e:
        st.error(f"Error importando módulos: {e}")

def app():
    st.title("📊 Estado de Sensores")
    
    # Asegurar conexión
    connect_mqtt()

    # Botón de refresco manual (Streamlit no se actualiza solo en tiempo real sin triggers)
    if st.button("🔄 Actualizar Datos"):
        st.rerun()

    # Obtener datos del estado (actualizados por el hilo MQTT en background)
    temp = get_sensor_data("Temp")
    hum = get_sensor_data("Hum")
    gas = get_sensor_data("Gas")
    luz = get_sensor_data("Luminosidad")

    # Layout de Columnas
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        st.metric("Temperatura", f"{temp} °C")
    with col2:
        st.metric("Humedad", f"{hum} %")
    with col3:
        st.metric("Gas (PPM)", f"{gas}")
    with col4:
        st.metric("Luminosidad", f"{luz}")

    # Auto-refresh experimental (Opcional)
    # time.sleep(2)
    # st.rerun()
    
app() # Ejecutar función si se llama directamente

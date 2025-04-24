import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from googletrans import Translator

# Título de la app
st.title("Welcome to your Interactive Diccionary!🌍")

# Traductor
translator = Translator()

# Crear el mapa centrado en el mundo
world_map = folium.Map(location=[0, 0], zoom_start=2)

# Agregar un marcador de ejemplo
folium.Marker(
    location=[40.4168, -3.7038],  # Coordenadas de Madrid
    popup="España: Hola",
    tooltip="Haz hover para ver"
).add_to(world_map)

# Mostrar el mapa en Streamlit
st.subheader("Mapa Interactivo:")
folium_static(world_map)

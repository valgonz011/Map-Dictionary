import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from googletrans import Translator

# Título
st.title("Diccionario Mundial 🌍")

# Entrada de palabra
word = st.text_input("Escribe una palabra para traducirla:")

# Lista simple de países con idiomas (puedes expandir esto después)
countries = [
    {"name": "España", "lat": 40.4168, "lon": -3.7038, "lang": "es"},
    {"name": "Francia", "lat": 48.8566, "lon": 2.3522, "lang": "fr"},
    {"name": "Alemania", "lat": 52.52, "lon": 13.4050, "lang": "de"},
    {"name": "Brasil", "lat": -15.793889, "lon": -47.882778, "lang": "pt"},
    {"name": "Japón", "lat": 35.6895, "lon": 139.6917, "lang": "ja"},
    {"name": "Estados Unidos", "lat": 38.9072, "lon": -77.0369, "lang": "en"},
    {"name": "China", "lat": 39.9042, "lon": 116.4074, "lang": "zh-cn"},
]

# Mapa
world_map = folium.Map(location=[0, 0], zoom_start=2)

# Traductor
translator = Translator()

# Si el usuario escribió una palabra
if word:
    for country in countries:
        translated = translator.translate(word, dest=country["lang"]).text
        folium.Marker(
            location=[country["lat"], country["lon"]],
            tooltip=f"{country['name']}: {translated}",
            popup=f"{country['name']}: {translated}"
        ).add_to(world_map)

# Mostrar el mapa
st.subheader("Traducciones en el Mapa:")
folium_static(world_map)
